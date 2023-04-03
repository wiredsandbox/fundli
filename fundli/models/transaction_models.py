from datetime import datetime

from bson.objectid import ObjectId

from .account_models import AccountInfo


class Transaction:
    def __init__(
        self,
        id: ObjectId,
        created_at: datetime,
        updated_at: datetime,
        name: str,
        amount: int,
        kind: str,
        tags: list,
        account_info: AccountInfo,
    ):
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.name = name
        self.amount = amount
        self.kind = kind
        self.tags = tags or []
        self.account_info = account_info

        # don't write these fields to the database
        self.used_projection = False

    def to_dict(self):
        return {
            "_id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "name": self.name,
            "amount": self.amount,
            "kind": self.kind,
            "account_info": self.account_info.to_dict(),
        }
