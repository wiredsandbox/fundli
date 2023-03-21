from pymongo.cursor import Cursor
from math import ceil


default_page_number = 1
default_per_page = 30


class Paginator:
    current_page: int
    next_page: int
    prev_page: int
    total_pages: int
    total_rows: int
    per_page: int
    offset: int

    def __init__(self, page, per_page):
        self.offset = 0

        self.current_page = page
        if page < 1:
            self.current_page = default_page_number

        self.per_page = per_page
        if per_page < 1:
            self.per_page = default_per_page

    def set_offset(self):
        if self.current_page == 1:
            self.offset = 0
        else:
            self.offset = (self.current_page - 1) * self.per_page

    def set_total_pages(self):
        if self.total_rows == 0:
            self.total_pages = 0
        else:
            self.total_pages = ceil(self.total_rows / self.per_page)

    def set_prev_page(self):
        # call set_total_pages to be safe
        self.set_total_pages()

        if self.current_page == 1:
            self.prev_page = 0
        else:
            self.prev_page = self.current_page - 1

    def set_next_page(self):
        # call set_total_pages to be safe
        self.set_total_pages()

        if self.current_page == self.total_pages:
            self.next_page = self.current_page
        else:
            self.next_page = self.current_page + 1


class PaginatedResult:
    paginator: Paginator
    cursor: Cursor

    def __init__(self, paginator: Paginator, cursor: Cursor):
        self.paginator = paginator
        self.cursor = cursor
