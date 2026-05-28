"""
Unit tests for security utilities in app/core/security.py

STRUCTURE:
    1. Password hashing & verification
    2. JWT token creation & decoding
    3. Session token & expiry
    4. Security integration tests

"""

import re
from datetime import UTC, datetime, timedelta

import jwt
import pytest

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_session_expiry,
    create_session_token,
    decode_token,
    get_password_hash,
    verify_password,
)

# ============================================================
# 1. PASSWORD HASHING & VERIFICATION
# ============================================================


def test_password_hash_and_verify():
    """Hash-ul trebuie să verifice parola corectă."""
    pw = "SecurePassword123!"
    hashed = get_password_hash(pw)
    assert verify_password(pw, hashed) is True


def test_password_verify_incorrect():
    """Parola greșită nu trebuie să verifice."""
    hashed = get_password_hash("Correct123!")
    assert verify_password("Wrong456!", hashed) is False


def test_password_hash_salt():
    """Hash-uri diferite pentru aceeași parolă (argon2 salt)."""
    pw = "SamePassword123!"
    h1 = get_password_hash(pw)
    h2 = get_password_hash(pw)
    assert h1 != h2
    assert verify_password(pw, h1)
    assert verify_password(pw, h2)


def test_password_hash_format():
    """Hash-ul trebuie să înceapă cu prefix Argon2."""
    hashed = get_password_hash("Test123!")
    assert hashed.startswith("$argon2")


@pytest.mark.parametrize(
    "password",
    [
        "P@ssw0rd!#$%^&*()",
        "Пароль123🔒",
        "",
        "a" * 1000,
    ],
)
def test_password_edge_cases(password):
    """Hashing funcționează pentru caractere speciale, unicode, gol, foarte lung."""
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)


def test_password_case_sensitive():
    """Verificarea trebuie să fie case-sensitive."""
    pw = "CaseSensitive123"
    hashed = get_password_hash(pw)
    assert verify_password(pw, hashed)
    assert not verify_password(pw.lower(), hashed)
    assert not verify_password(pw.upper(), hashed)


# ============================================================
# 2. JWT TOKEN CREATION & DECODING
# ============================================================


def test_jwt_custom_expiry():
    """Token cu expirare custom."""
    token = create_access_token({"sub": "test"}, timedelta(minutes=10))
    decoded = decode_token(token)
    assert decoded["sub"] == "test"
    assert "exp" in decoded


def test_jwt_default_expiry():
    """Token cu expirare default din settings."""
    token = create_access_token({"sub": "default"})
    decoded = decode_token(token)

    exp = datetime.fromtimestamp(decoded["exp"], tz=UTC)
    now = datetime.now(UTC)
    delta = (exp - now).total_seconds() / 60

    assert (
        settings.ACCESS_TOKEN_EXPIRE_MINUTES - 1
        <= delta
        <= settings.ACCESS_TOKEN_EXPIRE_MINUTES + 1
    )


def test_jwt_payload_preserved():
    """Payload-ul trebuie să fie păstrat integral."""
    data = {"sub": "user", "email": "a@a.com", "role": "admin"}
    token = create_access_token(data)
    decoded = decode_token(token)
    for k, v in data.items():
        assert decoded[k] == v


def test_jwt_unique_tokens():
    """Token-uri diferite pentru payload diferit."""
    t1 = create_access_token({"sub": "u1"})
    t2 = create_access_token({"sub": "u2"})
    assert t1 != t2


def test_jwt_decode_expired():
    """Token expirat trebuie să ridice eroare."""
    token = create_access_token({"sub": "expired"}, timedelta(seconds=-1))
    with pytest.raises(jwt.ExpiredSignatureError):
        decode_token(token)


def test_jwt_invalid_signature():
    """Token semnat cu alt secret trebuie să eșueze."""
    fake = jwt.encode(
        {"sub": "x", "exp": datetime.now(UTC) + timedelta(minutes=5)},
        "wrong-secret",
        algorithm=settings.ALGORITHM,
    )
    with pytest.raises(jwt.InvalidSignatureError):
        decode_token(fake)


def test_jwt_malformed():
    """Token invalid trebuie să ridice eroare."""
    with pytest.raises(jwt.DecodeError):
        decode_token("this.is.not.jwt")


def test_jwt_wrong_algorithm():
    """Token creat cu alt algoritm trebuie să eșueze."""
    wrong = jwt.encode(
        {"sub": "x", "exp": datetime.now(UTC) + timedelta(minutes=5)},
        settings.SECRET_KEY,
        algorithm="HS512",
    )
    with pytest.raises(jwt.InvalidAlgorithmError):
        decode_token(wrong)


def test_jwt_empty_payload():
    """Token fără payload (doar exp)."""
    token = create_access_token({})
    decoded = decode_token(token)
    assert list(decoded.keys()) == ["exp"]


# ============================================================
# 3. SESSION TOKEN & EXPIRY
# ============================================================


def test_session_token_format():
    """Token-ul de sesiune trebuie să fie hex de 64 caractere."""
    token = create_session_token()
    assert re.fullmatch(r"[0-9a-f]{64}", token)


def test_session_token_unique():
    """Token-urile trebuie să fie unice."""
    tokens = {create_session_token() for _ in range(200)}
    assert len(tokens) == 200


def test_session_expiry_default():
    """Expirarea default = 24h."""
    before = datetime.now(UTC)
    expiry = create_session_expiry()
    delta = expiry - before
    assert abs(delta.total_seconds() - 86400) < 1


def test_session_expiry_custom():
    """Expirare custom."""
    expiry = create_session_expiry(hours=48)
    delta = expiry - datetime.now(UTC)
    assert abs(delta.total_seconds() - 48 * 3600) < 1


def test_session_expiry_utc():
    """Expirarea trebuie să fie în UTC."""
    assert create_session_expiry().tzinfo == UTC


# ============================================================
# 4. SECURITY INTEGRATION TESTS
# ============================================================


def test_password_and_token_flow():
    """Workflow complet: hash → verify → token → decode."""
    pw = "UserPassword123!"
    hashed = get_password_hash(pw)
    assert verify_password(pw, hashed)

    token = create_access_token({"sub": "test", "id": 1})
    decoded = decode_token(token)

    assert decoded["sub"] == "test"
    assert decoded["id"] == 1


def test_multiple_tokens_independent():
    """Token-uri pentru utilizatori diferiți trebuie să fie independente."""
    t1 = create_access_token({"sub": "u1", "role": "user"})
    t2 = create_access_token({"sub": "u2", "role": "admin"})

    d1 = decode_token(t1)
    d2 = decode_token(t2)

    assert d1["sub"] == "u1"
    assert d2["sub"] == "u2"
    assert t1 != t2
