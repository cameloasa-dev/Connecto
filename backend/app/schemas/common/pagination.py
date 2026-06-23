""" "
Social feature schemas for Connecto
Pagination
"""

from typing import Any

from pydantic import BaseModel


# ======================================================
# PAGINATION SCHEMAS
# ======================================================
class PaginatedResponse(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool
    items: list[Any]
