from datetime import datetime

from fastapi import HTTPException, Request, Response

from app.core.config import settings
from app.core.security import (
    create_session_expiry,
    create_session_token,
    hash_password,
    verify_password,
)
from app.db.models import User, UserSession
from app.repositories.circle_repository import CircleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    SessionResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.schemas.circles.roles import (
    CircleRole,
    UserRoleItem,
    UserRolesResponse,
)


class UserService:
    def __init__(
        self,
        repo: UserRepository,
        circle_repo: CircleRepository,
    ):
        self.repo = repo
        self.circle_repo = circle_repo

    # --------------------------------------------------
    # AUTH
    # --------------------------------------------------

    # --------------------------------------------------
    # REGISTER
    # --------------------------------------------------

    async def register(self, user_data: UserCreate) -> SessionResponse:
        if await self.repo.get_by_username(user_data.username):
            raise HTTPException(400, "Username already taken")

        if await self.repo.get_by_email_case_insensitive(user_data.email):
            raise HTTPException(400, "Email already taken")

        user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hash_password(user_data.password),
            is_active=True,
        )

        user = await self.repo.add_user(user)

        return SessionResponse(
            success=True,
            username=user.username,
            session_token=None,
            user=UserResponse.model_validate(user),
        )

    # --------------------------------------------------
    # Login
    # --------------------------------------------------
    async def login(
        self,
        credentials: UserLogin,
        request: Request,
        response: Response,
    ) -> SessionResponse:

        user = await self.repo.get_by_username(credentials.username)

        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(401, "Invalid credentials")

        if not user.is_active:
            raise HTTPException(403, "Inactive account")

        token = create_session_token()
        expires = create_session_expiry(hours=settings.SESSION_EXPIRE_HOURS)

        session = UserSession(
            session_token=token,
            user_id=user.id,
            created_at=datetime.now(),
            expires_at=expires,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )

        await self.repo.create_session(session)

        secure = settings.ENVIRONMENT == "production"

        response.set_cookie(
            key="session_token",
            value=token,
            httponly=True,
            secure=secure,
            samesite="none" if secure else "lax",
            max_age=settings.SESSION_EXPIRE_HOURS * 3600,
            path="/",
        )

        return SessionResponse(
            success=True,
            username=user.username,
            session_token=token,
            user=UserResponse.model_validate(user),
        )

    async def get_current_user_from_session_token(self, session_token: str) -> User:
        session = await self.repo.get_valid_session(session_token)
        if not session:
            raise HTTPException(401, "Session expired or invalid")

        user = await self.repo.get_by_id(session.user_id)
        if not user:
            raise HTTPException(401, "User not found")

        return user

    # --------------------------------------------------
    # Logout
    # --------------------------------------------------
    async def logout(self, request: Request, response: Response) -> dict:
        token = request.cookies.get("session_token")

        if token:
            session = await self.repo.get_valid_session(token)
            if session:
                await self.repo.delete_session(session)

        secure = settings.ENVIRONMENT == "production"

        response.delete_cookie(
            "session_token",
            path="/",
            secure=secure,
            samesite="none" if secure else "lax",
        )

        return {"success": True, "message": "Logged out"}
    # --------------------------------------------------
    # Users
    # --------------------------------------------------
    async def list_users(
        self,
        current_user: User,
        skip: int,
        limit: int,
    ) -> list[UserResponse]:

        users = await self.repo.get_all_except(current_user.id, skip, limit)

        return [UserResponse.model_validate(u) for u in users]
    # --------------------------------------------------
    # User role
    # --------------------------------------------------
    async def get_user_roles(self, user_id: int) -> UserRolesResponse:

        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(404, "User not found")

        memberships = await self.circle_repo.get_user_circles_with_membership(user_id)

        roles = [
            UserRoleItem(
                circle_id=circle.id,
                circle_name=circle.name,
                role=CircleRole(role.role),
            )
            for circle, role in memberships
        ]

        return UserRolesResponse(
            user=UserResponse.model_validate(user),
            roles=roles,
        )
