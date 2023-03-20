from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel

from pocketguardapp.models.transaction_models import Transaction

from .account_schemas import AccountInfoResponse


class TransactionKind(str, Enum):
    INCOME: str = "INCOME"
    EXPENSE: str = "EXPENSE"


class TransactionCreateRequest(BaseModel):
    name: str
    amount: float
    timestamp: str
    kind: TransactionKind


class TransactionResponse(BaseModel):
    id: str
    createdAt: datetime
    updatedAt: datetime
    name: str
    amount: float
    kind: str
    accountInfo: AccountInfoResponse


class TransactionGetAllResponse(BaseModel):
    transactions: List[TransactionResponse]


# ---------------------------------------------------------------------------------------------------------------
#                                             Serializers
# ---------------------------------------------------------------------------------------------------------------


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


def transaction_get_all_response_serializer(transactions: List[Transaction]):
    return TransactionGetAllResponse(
        transactions=[
            transaction_response_serializer(transaction) for transaction in transactions
        ]
    )
