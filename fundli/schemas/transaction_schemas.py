from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel

from fundli.database.paginator import Paginator
from fundli.models.transaction_models import Transaction
from fundli.schemas.shared import PaginatorResponse, paginator_response_serializer

from .account_schemas import AccountInfoResponse


class TransactionKind(str, Enum):
    INCOME: str = "INCOME"
    EXPENSE: str = "EXPENSE"


class TransactionCreateRequest(BaseModel):
    name: Optional[str]
    amount: float
    timestamp: str
    kind: TransactionKind
    wallet_id: str
    tags: Optional[List[str]]


class TransactionUpdateRequest(BaseModel):
    name: str = None
    amount: float = None
    timestamp: str = None
    kind: TransactionKind = None
    tags: List[str] = None
    wallet_id: str


class TransactionResponse(BaseModel):
    id: str
    createdAt: datetime
    updatedAt: datetime
    name: str
    amount: float
    kind: str
    tags: List[str]
    accountInfo: AccountInfoResponse
    wallet_id: str


class TransactionPaginateResponse(BaseModel):
    transactions: List[TransactionResponse]
    paginator: Union[PaginatorResponse, None]


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
        tags=transaction.tags or [],
        accountInfo=AccountInfoResponse(
            id=str(transaction.account_info.id),
            email=transaction.account_info.email,
            firstName=transaction.account_info.first_name,
            lastName=transaction.account_info.last_name,
        ),
        wallet_id=str(transaction.wallet_id),
    )


def transaction_paginate_response_serializer(
    transactions: List[Transaction], paginator: Union[Paginator, None]
):
    return TransactionPaginateResponse(
        transactions=[
            transaction_response_serializer(transaction) for transaction in transactions
        ],
        paginator=paginator_response_serializer(paginator) if paginator else None,
    )
