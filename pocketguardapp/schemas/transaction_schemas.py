from datetime import datetime
from pydantic import BaseModel

from pocketguardapp.models.account_models import Account, AccountInfo
from pocketguardapp.models.transaction_models import Transaction
from .account_schemas import AccountInfoResponse


class TransactionCreateRequest(BaseModel):
    name: str
    amount: float
    timestamp: str
    kind: str


class TransactionResponse(BaseModel):
    id: str
    createdAt: datetime
    updatedAt: datetime
    name: str
    amount: float
    kind: str
    accountInfo: AccountInfoResponse


def transaction_response_serializer(transaction: Transaction):
    return TransactionResponse(
        id=str(transaction.id),
        createdAt=transaction.created_at,
        updatedAt=transaction.updated_at,
        name=transaction.name,
        amount=(transaction.amount / 100),
        kind=transaction.kind,
        accountInfo=AccountInfoResponse(
            id=str(transaction.account_info.id),
            email=transaction.account_info.email,
            firstName=transaction.account_info.first_name,
            lastName=transaction.account_info.last_name,
        ),
    )
