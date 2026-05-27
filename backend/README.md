# Backend

## Backend Installation / Stack

Core Framework
FastAPI — framework principal, rapid, modern

Uvicorn — server ASGI pentru FastAPI

Database Layer
SQLAlchemy — ORM modern

SQLite + aiosqlite — baza de date mică, locală, perfectă pentru dev



Config & Models
Pydantic v2 — validare modele

Pydantic Settings — citire .env

Security
Argon2 — hashing parole

PyJWT — tokenizare JWT

email-validator — validare email

Testing (simplu, curat)
pytest

pytest-asyncio

httpx — testare API async

Tooling
Ruff — linting + formatting

Mypy — type checking

## Backend stucture

```text

backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── auth.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # settings + env
│   │   ├── security.py      # JWT, hashing
│   │   └── database.py      # SQLite engine
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py
│   │
│   └── services/
│       ├── __init__.py
│       └── user_service.py
│
├── tests/
│   ├── __init__.py
│   └── test_users.py
│
├── dev.db                  # SQLite DB (gitignored)
├── .env                    # config local (gitignored)
├── pyproject.toml
└── README.md
```
