from fundli.models.account_models import Account

from .database import Database


class AccountDatabase(Database):
    def __init__(self):
        super().__init__("accounts")

    def find_one(self, query_filter):
        data = super().find_one(query_filter)
        if data:
            return Account(
                id=data.get("_id"),
                created_at=data.get("created_at"),
                updated_at=data.get("updated_at"),
                email=data.get("email"),
                password=data.get("password"),
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                verification_code=data.get("verification_code"),
            )
        return None


account_database = AccountDatabase()
