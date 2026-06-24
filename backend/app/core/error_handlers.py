import logging
from typing import cast

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("app")


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=cast(StarletteHTTPException, exc).status_code,
        content={
            "error": cast(StarletteHTTPException, exc).detail,
            "status": cast(StarletteHTTPException, exc).status_code,
        },
    )


async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "detail": cast(RequestValidationError, exc).errors(),
            "status": 422,
        },
    )


async def integrity_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={
            "error": "Database error",
            "detail": "Integrity constraint violated",
            "status": 400,
        },
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error({"event": "unhandled_exception", "error": str(exc)})
    return JSONResponse(
        status_code=500,
        content={
            "error": "Server error",
            "detail": "Unexpected error occurred",
            "status": 500,
        },
    )
