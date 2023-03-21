from pydantic import BaseModel

from pocketguardapp.database.paginator import Paginator


class PaginatorResponse(BaseModel):
    current_page: int
    next_page: int
    prev_page: int
    total_pages: int
    total_rows: int
    per_page: int
    offset: int


def paginator_response_serializer(paginator: Paginator):
    return PaginatorResponse(
        current_page=paginator.current_page,
        next_page=paginator.next_page,
        prev_page=paginator.prev_page,
        total_pages=paginator.total_pages,
        total_rows=paginator.total_rows,
        per_page=paginator.per_page,
        offset=paginator.offset,
    )
