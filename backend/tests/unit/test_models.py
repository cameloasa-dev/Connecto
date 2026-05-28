"""
Unit tests for SQLAlchemy models in app/db/models.py

STRUCTURE:
    1. User model
    2. Circle model
    3. CircleMember model
    4. Post model
    5. Role model
    6. UserSession model
    7. Shared constraints (inheritance, timestamps)

"""

import pytest
from sqlalchemy import inspect

from app.db.models import (
    Base,
    Circle,
    CircleMember,
    Post,
    Role,
    User,
    UserSession,
)

# ============================================================
# 1. USER MODEL
# ============================================================


def test_user_tablename():
    assert User.__tablename__ == "users"


def test_user_columns():
    mapper = inspect(User)
    cols = mapper.columns.keys()

    expected = {
        "id",
        "username",
        "email",
        "hashed_password",
        "full_name",
        "is_active",
        "created_at",
        "updated_at",
    }
    assert expected.issubset(cols)


def test_user_unique_constraints():
    mapper = inspect(User)
    assert mapper.columns["username"].unique is True
    assert mapper.columns["email"].unique is True


def test_user_nullable_fields():
    mapper = inspect(User)
    assert mapper.columns["full_name"].nullable is True
    assert mapper.columns["updated_at"].nullable is True


def test_user_non_nullable_fields():
    mapper = inspect(User)
    for col in ["id", "username", "email", "hashed_password"]:
        assert mapper.columns[col].nullable is False


def test_user_relationships():
    mapper = inspect(User)
    rels = mapper.relationships.keys()
    assert {"owned_circles", "circle_memberships", "posts"}.issubset(rels)


# ============================================================
# 2. CIRCLE MODEL
# ============================================================


def test_circle_tablename():
    assert Circle.__tablename__ == "circles"


def test_circle_columns():
    mapper = inspect(Circle)
    cols = mapper.columns.keys()
    assert {"id", "name", "description", "owner_id", "created_at"}.issubset(cols)


def test_circle_owner_fk():
    mapper = inspect(Circle)
    fk = list(mapper.columns["owner_id"].foreign_keys)[0]
    assert "users.id" in str(fk.target_fullname)


def test_circle_relationships():
    mapper = inspect(Circle)
    rels = mapper.relationships.keys()
    assert {"owner", "members", "posts"}.issubset(rels)


def test_circle_description_nullable():
    mapper = inspect(Circle)
    assert mapper.columns["description"].nullable is True


# ============================================================
# 3. CIRCLEMEMBER MODEL
# ============================================================


def test_circlemember_tablename():
    assert CircleMember.__tablename__ == "circle_members"


def test_circlemember_composite_pk():
    mapper = inspect(CircleMember)
    pk = {col.name for col in mapper.primary_key}
    assert pk == {"circle_id", "user_id"}


def test_circlemember_foreign_keys():
    mapper = inspect(CircleMember)
    assert "circles.id" in str(list(mapper.columns["circle_id"].foreign_keys)[0].target_fullname)
    assert "users.id" in str(list(mapper.columns["user_id"].foreign_keys)[0].target_fullname)


def test_circlemember_role_default():
    mapper = inspect(CircleMember)
    col = mapper.columns["role"]
    assert col.default is not None or col.server_default is not None


def test_circlemember_relationships():
    mapper = inspect(CircleMember)
    rels = mapper.relationships.keys()
    assert {"circle", "user"}.issubset(rels)


# ============================================================
# 4. POST MODEL
# ============================================================


def test_post_tablename():
    assert Post.__tablename__ == "posts"


def test_post_columns():
    mapper = inspect(Post)
    cols = mapper.columns.keys()
    expected = {"id", "title", "content", "author_id", "circle_id", "created_at", "updated_at"}
    assert expected.issubset(cols)


def test_post_author_fk():
    mapper = inspect(Post)
    fk = list(mapper.columns["author_id"].foreign_keys)[0]
    assert "users.id" in str(fk.target_fullname)


def test_post_circle_fk():
    mapper = inspect(Post)
    fk = list(mapper.columns["circle_id"].foreign_keys)[0]
    assert "circles.id" in str(fk.target_fullname)
    assert mapper.columns["circle_id"].nullable is True


def test_post_relationships():
    mapper = inspect(Post)
    rels = mapper.relationships.keys()
    assert {"author", "circle"}.issubset(rels)


def test_post_required_fields():
    mapper = inspect(Post)
    assert mapper.columns["title"].nullable is False
    assert mapper.columns["content"].nullable is False


# ============================================================
# 5. ROLE MODEL
# ============================================================


def test_role_tablename():
    assert Role.__tablename__ == "roles"


def test_role_columns():
    mapper = inspect(Role)
    cols = mapper.columns.keys()
    assert {"id", "name", "description"}.issubset(cols)


def test_role_constraints():
    mapper = inspect(Role)
    assert mapper.columns["name"].unique is True
    assert mapper.columns["name"].index is True


# ============================================================
# 6. USERSESSION MODEL
# ============================================================


def test_usersession_tablename():
    assert UserSession.__tablename__ == "user_sessions"


def test_usersession_columns():
    mapper = inspect(UserSession)
    cols = mapper.columns.keys()
    expected = {
        "id",
        "session_token",
        "user_id",
        "created_at",
        "expires_at",
        "ip_address",
        "user_agent",
    }
    assert expected.issubset(cols)


def test_usersession_constraints():
    mapper = inspect(UserSession)
    col = mapper.columns["session_token"]
    assert col.unique is True
    assert col.index is True


def test_usersession_nullable_fields():
    mapper = inspect(UserSession)
    assert mapper.columns["ip_address"].nullable is True
    assert mapper.columns["user_agent"].nullable is True


def test_usersession_required_fields():
    mapper = inspect(UserSession)
    for col in ["session_token", "user_id", "created_at", "expires_at"]:
        assert mapper.columns[col].nullable is False


# ============================================================
# 7. SHARED MODEL CONSTRAINTS
# ============================================================


@pytest.mark.parametrize("model", [User, Circle, CircleMember, Post, Role, UserSession])
def test_all_models_inherit_base(model):
    assert issubclass(model, Base)


def test_base_is_declarative():
    from sqlalchemy.orm import DeclarativeBase

    assert issubclass(Base, DeclarativeBase)


def test_timestamp_fields():
    """Check created_at and updated_at defaults across models."""
    for model in [User, Circle, Post, CircleMember]:
        mapper = inspect(model)
        assert mapper.columns["created_at"].server_default is not None

    # updated_at exists only on some models
    for model in [User, Post]:
        mapper = inspect(model)
        assert (
            mapper.columns["updated_at"].onupdate is not None
            or mapper.columns["updated_at"].server_onupdate is not None
        )
