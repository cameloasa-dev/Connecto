"""
Authentication endpoints (SESSION-BASED)
Production-ready version
"""

import logging
import traceback
from datetime import datetime
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.limiter import limiter
from app.core.security import (
    create_session_expiry,
    create_session_token,
    hash_password,
    verify_password,
)
from app.db.database import get_db
from app.db.models import User, UserSession
from app.schemas import (
    SessionResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)

# ---------------------------------------------------------
# LOGGER
# ---------------------------------------------------------
logger = logging.getLogger("auth")

# ---------------------------------------------------------
# ROUTER
# ---------------------------------------------------------
router = APIRouter(prefix="/auth", tags=["auth"])


# =========================================================
# REGISTER
# =========================================================
@router.post("/register", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)) -> SessionResponse:

    # Check username
    existing_username = await db.execute(
        select(User).where(User.username == user_data.username)
    )
    if existing_username.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already taken")

    # Check email
    existing_email = await db.execute(
        select(User).where(func.lower(User.email) == func.lower(user_data.email))
    )
    if existing_email.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already taken")

    # Create user
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
        is_active=True,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    logger.info({
        "event": "user_registered",
        "username": new_user.username,
        "user_id": new_user.id
    })

    return SessionResponse(
        success=True,
        username=new_user.username,
        session_token=None,
        user=UserResponse.model_validate(new_user)
    )


# =========================================================
# LOGIN
# =========================================================
@router.post("/login", response_model=SessionResponse)
@limiter.limit("5/minute")
async def login(
    credentials: UserLogin,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
) -> SessionResponse:

    try:
        # Find user
        result = await db.execute(
            select(User).where(User.username == credentials.username)
        )
        user = result.scalar_one_or_none()

        if not user or not verify_password(credentials.password, user.hashed_password):
            logger.warning({
                "event": "auth_failed",
                "username": credentials.username,
                "ip": request.client.host if request.client else "unknown",
            })
            raise HTTPException(status_code=401, detail="Invalid username or password")

        if not user.is_active:
            raise HTTPException(status_code=403, detail="Account is inactive")

        # Create session
        session_token = create_session_token()
        expires_at = create_session_expiry(hours=settings.SESSION_EXPIRE_HOURS)

        new_session = UserSession(
            session_token=session_token,
            user_id=user.id,
            created_at=datetime.now(),
            expires_at=expires_at,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )

        db.add(new_session)
        await db.commit()

        # Cookie settings
        secure_flag = settings.ENVIRONMENT == "production"
        samesite_value: Literal["lax", "none"] = "none" if secure_flag else "lax"

        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            secure=secure_flag,
            samesite=samesite_value,
            max_age=settings.SESSION_EXPIRE_HOURS * 3600,
            path="/",
        )

        return SessionResponse(
            success=True,
            username=user.username,
            session_token=session_token,
            user=UserResponse.model_validate(user)
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error({
            "event": "auth_error",
            "error": str(e),
            "trace": traceback.format_exc()
        })
        raise HTTPException(
            status_code=500,
            detail="Login failed due to server error"
            ) from e


# =========================================================
# CURRENT USER
# =========================================================
async def get_current_user_from_session(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> User:

    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session_result = await db.execute(
        select(UserSession)
        .where(UserSession.session_token == session_token)
        .where(UserSession.expires_at > datetime.now())
    )
    session = session_result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    user_result = await db.execute(select(User).where(User.id == session.user_id))
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user_endpoint(
    current_user: User = Depends(get_current_user_from_session)
) -> UserResponse:
    return UserResponse.model_validate(current_user)


# =========================================================
# LOGOUT
# =========================================================
@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
) -> dict[str, Any]:

    session_token = request.cookies.get("session_token")

    if session_token:
        result = await db.execute(
            select(UserSession).where(UserSession.session_token == session_token)
        )
        session = result.scalar_one_or_none()

        if session:
            await db.delete(session)
            await db.commit()

        secure_flag = settings.ENVIRONMENT == "production"
        samesite_value: Literal["lax", "none"] = "none" if secure_flag else "lax"

        response.delete_cookie(
            "session_token",
            path="/",
            secure=secure_flag,
            samesite=samesite_value
        )

    return {"success": True, "message": "Logged out successfully"}
