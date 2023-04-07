from .database import Database

from fundli.models.account_models import AccountInfo
from fundli.models.wallet_models import Wallet


class WalletDatabase(Database):
    def __init__(self):
        super().__init__("wallets")

    def find_one(self, query_filter):
        data = super().find_one(query_filter)
        if data:
            return Wallet(
                id=data.get("_id"),
                created_at=data.get("created_at"),
                updated_at=data.get("updated_at"),
                name=data.get("name"),
                account_info=AccountInfo(
                    id=data.get("account_info", {}).get("id"),
                    email=data.get("account_info", {}).get("email"),
                    first_name=data.get("account_info", {}).get("first_name"),
                    last_name=data.get("account_info", {}).get("last_name"),
                ),
            )
        return None


wallet_database = WalletDatabase()
