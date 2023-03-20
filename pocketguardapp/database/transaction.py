from pocketguardapp.models.account_models import AccountInfo
from pocketguardapp.models.transaction_models import Transaction

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
                account_info=AccountInfo(
                    id=data.get("account_info").get("id"),
                    email=data.get("account_info").get("email"),
                    first_name=data.get("account_info").get("first_name"),
                    last_name=data.get("account_info").get("last_name"),
                ),
            )
        return None


transaction_database = TransactionDatabase()
