from fundli.models.account_models import AccountInfo
from fundli.models.transaction_models import Transaction

from .database import Database


class TransactionDatabase(Database):
    def __init__(self):
        super().__init__("transactions")

    def find_one(self, query_filter):
        data = super().find_one(query_filter)
        if data:
            return Transaction(
                id=data.get("_id"),
                created_at=data.get("created_at"),
                updated_at=data.get("updated_at"),
                name=data.get("name"),
                amount=data.get("amount"),
                kind=data.get("kind"),
                tags=data.get("tags"),
                account_info=AccountInfo(
                    id=data.get("account_info").get("id"),
                    email=data.get("account_info").get("email"),
                    first_name=data.get("account_info").get("first_name"),
                    last_name=data.get("account_info").get("last_name"),
                ),
            )
        return None

    def paginate(self, query_filter, page, per_page):
        transactions = []
        res = super().find_paginated(query_filter, page, per_page)

        for data in res.cursor:
            transaction = Transaction(
                id=data.get("_id"),
                created_at=data.get("created_at"),
                updated_at=data.get("updated_at"),
                name=data.get("name"),
                amount=data.get("amount"),
                kind=data.get("kind"),
                tags=data.get("tags"),
                account_info=AccountInfo(
                    id=data.get("account_info", {}).get("id"),
                    email=data.get("account_info", {}).get("email"),
                    first_name=data.get("account_info", {}).get("first_name"),
                    last_name=data.get("account_info", {}).get("last_name"),
                ),
            )
            transactions.append(transaction)

        res.cursor.close()
        return transactions, res.paginator, None


transaction_database = TransactionDatabase()
