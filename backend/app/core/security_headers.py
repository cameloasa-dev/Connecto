f"""
Security headers middleware for Connecto backend
Adds CSP, HSTS, and modern security headers
"""

from typing import Any
from starlette.types import Scope, Receive, Send
from app.core.config import settings


class SecurityHeadersMiddleware:
    def __init__(self, app: Any) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

        async def send_wrapper(message: dict[str, Any]) -> None:
            if message.get("type") == "http.response.start":
                headers = message.setdefault("headers", [])

                # Basic security headers
                headers.append((b"x-frame-options", b"DENY"))
                headers.append((b"x-content-type-options", b"nosniff"))
                headers.append((b"referrer-policy", b"strict-origin-when-cross-origin"))
                headers.append((b"permissions-policy", b"geolocation=()"))

                # Modern security headers
                headers.append((b"cross-origin-opener-policy", b"same-origin"))
                headers.append((b"cross-origin-embedder-policy", b"require-corp"))
                headers.append((b"cross-origin-resource-policy", b"same-origin"))

                # Cache control
                headers.append((b"cache-control", b"no-store"))

                # Content Security Policy (CSP)
                csp = (
                    "default-src 'self'; "
                    "script-src 'self'; "
                    "style-src 'self' 'unsafe-inline'; "
                    "img-src 'self' data:; "
                    "connect-src 'self'; "
                    "frame-ancestors 'none';"
                )
                headers.append((b"content-security-policy", csp.encode()))

                # HSTS only in production
                if settings.ENVIRONMENT == "production":
                    headers.append(
                        (
                            b"strict-transport-security",
                            b"max-age=63072000; includeSubDomains; preload",
                        )
                    )

            await send(message)

        await self.app(scope, receive, send_wrapper)
