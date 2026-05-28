# backend/scripts/seed.py

import asyncio

from sqlalchemy import select

from app.core.config import settings
from app.core.security import hash_password
from app.db.database import SessionLocal
from app.db.models import Circle, CircleMember, Post, User
from app.schemas.social import CircleRole


async def create_test_data() -> None:
    """Create test users, circles, and posts for development ."""

    async with SessionLocal() as session:
        # Load test user data from .env
        email = settings.TEST_USER_EMAIL
        username = settings.TEST_USER_USERNAME
        password = settings.TEST_USER_PASSWORD

        # Check if test user exists
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user:
            print(f"Creating test user: {email}")

            # 1. Create main test user
            user = User(
                username=username,
                email=email,
                full_name="Test User",
                hashed_password=hash_password(password),
                is_active=True,
            )
            session.add(user)
            await session.flush()

            # 2. Create circles owned by test user
            circle_specs = [
                ("Family", "My family circle"),
                ("Friends", "Best friends forever"),
                ("Work", "Work colleagues"),
            ]

            circles = []
            for name, description in circle_specs:
                circle = Circle(
                    name=name,
                    description=description,
                    owner_id=user.id,
                )
                session.add(circle)
                await session.flush()

                # Add owner as member
                session.add(
                    CircleMember(
                        circle_id=circle.id,
                        user_id=user.id,
                        role=CircleRole.OWNER,
                    )
                )

                # Add welcome post
                session.add(
                    Post(
                        title=f"Welcome to {name}",
                        content=f"This is the first post in {name} circle",
                        author_id=user.id,
                        circle_id=circle.id,
                    )
                )

                circles.append(circle)

            # 3. Public post
            session.add(
                Post(
                    title="Hello World",
                    content="This is my first public post",
                    author_id=user.id,
                    circle_id=None,
                )
            )

            # 4. Create second test user
            email2 = settings.TEST_USER2_EMAIL
            username2 = settings.TEST_USER2_USERNAME
            password2 = settings.TEST_USER2_PASSWORD

            result2 = await session.execute(select(User).where(User.email == email2))
            user2 = result2.scalar_one_or_none()

            if not user2:
                user2 = User(
                    username=username2,
                    email=email2,
                    full_name="John Doe",
                    hashed_password=hash_password(password2),
                    is_active=True,
                )
                session.add(user2)
                await session.flush()

                # Add user2 to circles with roles
                roles = [CircleRole.MEMBER, CircleRole.MODERATOR, CircleRole.MEMBER]

                for circle, role in zip(circles, roles, strict=False):
                    session.add(
                        CircleMember(
                            circle_id=circle.id,
                            user_id=user2.id,
                            role=role,
                        )
                    )

            await session.commit()
            print("Test data created successfully!")

        else:
            print("Test user already exists — skipping creation.")


if __name__ == "__main__":
    asyncio.run(create_test_data())
