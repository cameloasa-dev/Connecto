"""
Main FastAPI application (ASYNC + SQLite)
Initializes the API with authentication, circles, members, posts, users,
CORS, security headers, logging middleware and rate limiting.
"""

import logging
import time
from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from app.api.endpoints import auth, circle_members, circles, dashboard, posts, users
from app.core.config import settings
from app.core.limiter import limiter
from app.core.security_headers import SecurityHeadersMiddleware
from app.db.database import Base, engine

# -----------------------------
# LOGGING CONFIG
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")


# -----------------------------
# LIFESPAN (startup + shutdown)
# -----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Create tables automatically for SQLite
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


# -----------------------------
# INITIALIZE APP
# -----------------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Social App backend (FastAPI + SQLite)",
    lifespan=lifespan,
)

app.state.limiter = limiter


# -----------------------------
# RATE LIMIT HANDLER
# -----------------------------
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    client_ip = request.client.host if request.client else "unknown"
    logger.warning({"event": "rate_limit_exceeded", "ip": client_ip, "path": request.url.path})
    print(f"⚠️ RATE LIMIT: {client_ip} - {request.url.path}")
    return JSONResponse(status_code=429, content={"detail": "Too many requests. Try again later."})


# -----------------------------
# LOGGING MIDDLEWARE
# -----------------------------
@app.middleware("http")
async def log_requests(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)
    ip = request.client.host if request.client else "unknown"

    logger.info(
        {
            "event": "http_request",
            "method": request.method,
            "url": request.url.path,
            "status": response.status_code,
            "duration_ms": duration,
            "ip": ip,
        }
    )

    print(f"📡 {request.method} {request.url.path} - {response.status_code} - {duration}ms - {ip}")
    return response


# -----------------------------
# CORS + SECURITY HEADERS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SecurityHeadersMiddleware)


# -----------------------------
# ROUTERS
# -----------------------------
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(circles.router)
app.include_router(circle_members.router)
app.include_router(posts.router)
app.include_router(dashboard.router)


# -----------------------------
# HEALTH ENDPOINTS
# -----------------------------
@app.get("/")
async def root() -> dict[str, Any]:
    return {
        "message": "Social App API",
        "version": settings.VERSION,
        "status": "running",
        "database": "SQLite",
    }


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy", "database": "SQLite"}
