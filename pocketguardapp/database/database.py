from pymongo import MongoClient

from pocketguardapp.settings.settings import DATABASE_URI, DATABASE_NAME
from pocketguardapp.database.paginator import Paginator, PaginatedResult

client = MongoClient(host=DATABASE_URI)


class Database:
    def __init__(self, collection_name):
        self.database = client[DATABASE_NAME]
        self.collection = self.database[collection_name]

    def create(self, data):
        self.collection.insert_one(data.to_dict())

    def find_one(self, query_filter):
        return self.collection.find_one(query_filter)

    def count(self, query_filter):
        return self.collection.count_documents(query_filter)

    def find_paginated(self, query_filter, page, per_page):
        """
        find_paginated searches for documents that match the provided filters.
        It returns a cursor as a result.
        """
        paginator = Paginator(page, per_page)
        paginator.set_offset()

        total_rows = self.collection.count_documents(query_filter)
        paginator.total_rows = total_rows

        cur = self.collection.find(
            query_filter, skip=paginator.offset, limit=paginator.per_page
        )

        paginator.set_total_pages()
        paginator.set_prev_page()
        paginator.set_next_page()
        return PaginatedResult(paginator, cur)
