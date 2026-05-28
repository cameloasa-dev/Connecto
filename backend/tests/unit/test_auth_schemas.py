"""
Unit tests for Pydantic schemas in app/schemas/auth.py

STRUCTURE:
    1. UserCreate schema
    2. UserLogin schema
    3. UserResponse schema
    4. Token schema
    5. SessionResponse schema

"""

from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schemas.auth import (
    SessionResponse,
    Token,
    UserCreate,
    UserLogin,
    UserResponse,
)

# ============================================================
# 1. USERCREATE SCHEMA TESTS
# ============================================================


def test_usercreate_valid():
    """UserCreate: valid payload should pass."""
    user = UserCreate(
        username="john",
        email="john@example.com",
        password="ValidPass123!",
        full_name="John Doe",
    )
    assert user.username == "john"
    assert user.full_name == "John Doe"


@pytest.mark.parametrize(
    "email",
    [
        "notanemail",
        "missing@domain",
        "@nodomain.com",
        "spaces in@email.com",
        "double@@domain.com",
    ],
)
def test_usercreate_invalid_email(email):
    """UserCreate: invalid email formats should fail."""
    with pytest.raises(ValidationError):
        UserCreate(username="john", email=email, password="ValidPass123!")


@pytest.mark.parametrize(
    "email",
    [
        "user@example.com",
        "user.name@example.com",
        "user+tag@example.co.uk",
        "user_123@sub.example.com",
    ],
)
def test_usercreate_valid_email(email):
    """UserCreate: valid email formats should pass."""
    user = UserCreate(username="john", email=email, password="ValidPass123!")
    assert user.email == email


@pytest.mark.parametrize("username", ["ab"])
def test_usercreate_username_too_short(username):
    """UserCreate: username must be >= 3 chars."""
    with pytest.raises(ValidationError):
        UserCreate(username=username, email="a@a.com", password="ValidPass123!")


def test_usercreate_username_min_ok():
    """UserCreate: username of length 3 should pass."""
    user = UserCreate(username="abc", email="a@a.com", password="ValidPass123!")
    assert user.username == "abc"


def test_usercreate_username_max_length():
    """UserCreate: username max length = 50."""
    valid = "a" * 50
    user = UserCreate(username=valid, email="a@a.com", password="ValidPass123!")
    assert user.username == valid

    with pytest.raises(ValidationError):
        UserCreate(username="a" * 51, email="a@a.com", password="ValidPass123!")


@pytest.mark.parametrize("password", ["short1!", "1234567"])
def test_usercreate_password_too_short(password):
    """UserCreate: password must be >= 8 chars."""
    with pytest.raises(ValidationError):
        UserCreate(username="john", email="a@a.com", password=password)


@pytest.mark.parametrize(
    "password",
    [
        "lowercase123!",  # no uppercase
    ],
)
def test_usercreate_password_missing_uppercase(password):
    with pytest.raises(ValidationError):
        UserCreate(username="john", email="a@a.com", password=password)


@pytest.mark.parametrize(
    "password",
    [
        "UPPERCASE123!",  # no lowercase
    ],
)
def test_usercreate_password_missing_lowercase(password):
    with pytest.raises(ValidationError):
        UserCreate(username="john", email="a@a.com", password=password)


@pytest.mark.parametrize(
    "password",
    [
        "NoNumbers!",  # no digits
    ],
)
def test_usercreate_password_missing_number(password):
    with pytest.raises(ValidationError):
        UserCreate(username="john", email="a@a.com", password=password)


@pytest.mark.parametrize(
    "password",
    [
        "NoSpecial123",  # no special char
    ],
)
def test_usercreate_password_missing_special(password):
    with pytest.raises(ValidationError):
        UserCreate(username="john", email="a@a.com", password=password)


@pytest.mark.parametrize(
    "password",
    [
        "SecurePass123!",
        "MyP@ssw0rd",
        "C0mpl3x#Pass",
        "Valid$Password1",
    ],
)
def test_usercreate_password_valid(password):
    """UserCreate: valid complex passwords should pass."""
    user = UserCreate(username="john", email="a@a.com", password=password)
    assert user.password == password


def test_usercreate_fullname_max_length():
    """UserCreate: full_name max length = 100."""
    valid = "A" * 100
    user = UserCreate(username="john", email="a@a.com", password="ValidPass123!", full_name=valid)
    assert user.full_name == valid

    with pytest.raises(ValidationError):
        UserCreate(username="john", email="a@a.com", password="ValidPass123!", full_name="A" * 101)


# ============================================================
# 2. USERLOGIN SCHEMA TESTS
# ============================================================


def test_userlogin_valid():
    login = UserLogin(username="john", password="pass")
    assert login.username == "john"


def test_userlogin_missing_username():
    with pytest.raises(ValidationError):
        UserLogin(password="pass")


def test_userlogin_missing_password():
    with pytest.raises(ValidationError):
        UserLogin(username="john")


# ============================================================
# 3. USERRESPONSE SCHEMA TESTS
# ============================================================


def test_userresponse_valid():
    now = datetime.now()
    user = UserResponse(
        id=1,
        username="john",
        email="john@example.com",
        full_name="John Doe",
        is_active=True,
        created_at=now,
        updated_at=now,
    )
    assert user.id == 1
    assert user.is_active is True


def test_userresponse_optional_fields():
    now = datetime.now()
    user = UserResponse(
        id=2,
        username="jane",
        email="jane@example.com",
        full_name=None,
        is_active=True,
        created_at=now,
        updated_at=None,
    )
    assert user.full_name is None
    assert user.updated_at is None


@pytest.mark.parametrize("missing_field", ["id", "username"])
def test_userresponse_missing_required(missing_field):
    now = datetime.now()
    data = {
        "id": 1,
        "username": "john",
        "email": "john@example.com",
        "full_name": None,
        "is_active": True,
        "created_at": now,
        "updated_at": None,
    }
    data.pop(missing_field)

    with pytest.raises(ValidationError):
        UserResponse(**data)


# ============================================================
# 4. TOKEN SCHEMA TESTS
# ============================================================


def test_token_valid():
    token = Token(access_token="abc", token_type="bearer")
    assert token.token_type == "bearer"


def test_token_default_type():
    token = Token(access_token="abc")
    assert token.token_type == "bearer"


def test_token_missing_access_token():
    with pytest.raises(ValidationError):
        Token(token_type="bearer")


# ============================================================
# 5. SESSIONRESPONSE SCHEMA TESTS
# ============================================================


def test_sessionresponse_valid():
    session = SessionResponse(success=True, username="john", session_token="xyz")
    assert session.success is True


def test_sessionresponse_minimal():
    """SessionResponse: only required fields should pass."""
    session = SessionResponse(success=True)
    assert session.success is True
