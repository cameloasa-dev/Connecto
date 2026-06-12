"""
Post management endpoints
Clean, organized, session-based authentication
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.auth import get_current_user_from_session
from app.db.database import get_db
from app.db.models import Circle, CircleMember, Post, User
from app.schemas import CircleRole, PostCreate, PostResponse

router = APIRouter(prefix="/posts", tags=["posts"])


# ======================================================
# HELPERS
# ======================================================


async def ensure_circle_member(db: AsyncSession, circle_id: int, user_id: int) -> None:
    """Ensure user is a member of the circle."""
    membership = await db.execute(
        select(CircleMember).where(
            CircleMember.circle_id == circle_id,
            CircleMember.user_id == user_id,
        )
    )
    member = membership.scalar_one_or_none()

    if member is None:
        raise HTTPException(status_code=403, detail="Not a member of this circle")


def build_post_response(
    post: Post,
    author_name: str,
    circle_name: str | None,
) -> PostResponse:
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        author_id=post.author_id,
        author_name=author_name,
        circle_id=post.circle_id,
        circle_name=circle_name,
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


# ======================================================
# Update Post
# ======================================================
@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_data: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
) -> PostResponse:

    post = await db.get(Post, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    post.title = post_data.title
    post.content = post_data.content

    await db.commit()
    await db.refresh(post)

    return build_post_response(
        post, current_user.username, post.circle.name if post.circle else None
    )


# ======================================================
# CREATE POST
# ======================================================
@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
) -> PostResponse:

    circle_name = None

    if post_data.circle_id:
        await ensure_circle_member(db, post_data.circle_id, current_user.id)
        circle = await db.get(Circle, post_data.circle_id)
        circle_name = circle.name if circle else None

    new_post = Post(
        title=post_data.title,
        content=post_data.content,
        author_id=current_user.id,
        circle_id=post_data.circle_id,
    )

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    return build_post_response(
        new_post,
        current_user.username,
        circle_name,
    )


# ======================================================
# GET POST BY ID
# ======================================================
@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
) -> PostResponse:

    result = await db.execute(
        select(Post, User.username, Circle.name)
        .join(User, Post.author_id == User.id)
        .join(Circle, Post.circle_id == Circle.id, isouter=True)
        .where(Post.id == post_id)
    )

    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail="Post not found")

    post, author_name, circle_name = row

    if post.circle_id:
        await ensure_circle_member(db, post.circle_id, current_user.id)

    return build_post_response(post, author_name, circle_name)


# ======================================================
# DELETE POST
# ======================================================
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
) -> None:

    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    can_delete = False

    if post.author_id == current_user.id:
        can_delete = True
    elif post.circle_id:
        membership = await db.execute(
            select(CircleMember).where(
                CircleMember.circle_id == post.circle_id,
                CircleMember.user_id == current_user.id,
            )
        )
        member = membership.scalar_one_or_none()
        if member and member.role in (CircleRole.OWNER, CircleRole.MODERATOR):
            can_delete = True

    if not can_delete:
        raise HTTPException(status_code=403, detail="You don't have permission to delete this post")

    await db.delete(post)
    await db.commit()


# ======================================================
# GET POSTS FROM A CIRCLE
# ======================================================
@router.get("/circle/{circle_id}", response_model=list[PostResponse])
async def get_circle_posts(
    circle_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_session),
    limit: int = 50,
    offset: int = 0,
) -> list[PostResponse]:

    await ensure_circle_member(db, circle_id, current_user.id)

    circle = await db.get(Circle, circle_id)

    posts_result = await db.execute(
        select(Post, User.username)
        .join(User, Post.author_id == User.id)
        .where(Post.circle_id == circle_id)
        .order_by(desc(Post.created_at))
        .offset(offset)
        .limit(limit)
    )

    posts = []
    for post, author_name in posts_result:
        posts.append(
            build_post_response(
                post,
                author_name,
                circle.name if circle else None,
            )
        )

    return posts
