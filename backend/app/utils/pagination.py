# backend/utils/pagination
from math import ceil


def paginate(page: int, page_size: int, total: int) -> dict[str, int | bool]:
    total_pages = ceil(total / page_size) if page_size > 0 else 1

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }
