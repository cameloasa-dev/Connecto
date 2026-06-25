from datetime import datetime
from typing import Any, Literal

from fastapi import HTTPException, Request, Response, status

from app.core.config import settings
from app.core.security import (
    create_session_expiry,
    create_session_token,
    hash_password,
    verify_password,
)
from app.db.models import User, UserSession
from app.repositories.user_repository import UserRepository
from app.schemas.auth import SessionResponse, UserCreate, UserLogin, UserResponse
from app.schemas.circles import UserSearchResponse


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    # ---------- REGISTER ----------
    async def register(self, user_data: UserCreate) -> SessionResponse:
        if await self.repo.get_by_username(user_data.username):
            raise HTTPException(status_code=400, detail="Username already taken")

        if await self.repo.get_by_email_case_insensitive(user_data.email):
            raise HTTPException(status_code=400, detail="Email already taken")

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hash_password(user_data.password),
            is_active=True,
        )

        user = await self.repo.add_user(new_user)

        return SessionResponse(
            success=True,
            username=user.username,
            session_token=None,
            user=UserResponse.model_validate(user),
        )

    # ---------- LOGIN ----------
    async def login(
        self,
        credentials: UserLogin,
        request: Request,
        response: Response,
    ) -> SessionResponse:
        user = await self.repo.get_by_username(credentials.username)

        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        if not user.is_active:
            raise HTTPException(status_code=403, detail="Account is inactive")

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

        await self.repo.create_session(new_session)

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
            user=UserResponse.model_validate(user),
        )

    # ---------- CURRENT USER (logic) ----------
    async def get_current_user_from_session_token(self, session_token: str) -> User:
        session = await self.repo.get_valid_session(session_token)
        if not session:
            raise HTTPException(status_code=401, detail="Session expired or invalid")

        user = await self.repo.get_by_id(session.user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    # ---------- LOGOUT ----------
    async def logout(self, request: Request, response: Response) -> dict:
        session_token = request.cookies.get("session_token")
        if not session_token:
            return {"success": True, "message": "Logged out successfully"}

        session = await self.repo.get_valid_session(session_token)
        if session:
            await self.repo.delete_session(session)

        secure_flag = settings.ENVIRONMENT == "production"
        samesite_value: Literal["lax", "none"] = "none" if secure_flag else "lax"

        response.delete_cookie(
            "session_token", path="/", secure=secure_flag, samesite=samesite_value
        )

        return {"success": True, "message": "Logged out successfully"}

    # ---------- LIST USERS ----------
    async def list_users(self, current_user: User, skip: int, limit: int) -> list[UserResponse]:
        users = await self.repo.get_all_except(current_user.id, skip, limit)
        return [UserResponse.model_validate(u) for u in users]

    # ---------- SEARCH USERS ----------
    async def search_users_for_circle(
        self,
        current_user: User,
        circle_id: int,
        query: str,
    ) -> list[UserSearchResponse]:
        # 1. Permission check
        membership = await self.repo.get_user_circle_role(circle_id, current_user.id)
        if not membership or membership.role not in ("owner", "moderator"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only circle owners and moderators can search for new members",
            )

        # 2. Empty query → empty list
        if not query.strip():
            return []

        # 3. Existing members
        existing_ids = await self.repo.get_circle_member_ids(circle_id)

        # 4. Search
        users = await self.repo.search_by_username_excluding_ids(
            query=query,
            exclude_ids=existing_ids,
            current_user_id=current_user.id,
        )

        return [
            UserSearchResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                is_already_member=False,
            )
            for user in users
        ]

    # ---------- Profile USERS ----------
    async def get_profile(self, user_id: int) -> dict[str, Any]:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        posts = await self.repo.get_user_posts(user_id)
        circles = await self.repo.get_user_circles(user_id)

        return {
            "user": user,
            "posts": posts,
            "circles": circles,
        }
