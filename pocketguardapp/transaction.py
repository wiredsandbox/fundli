from fastapi import APIRouter, Depends, HTTPException

from .middlewares.middleware import authenticate
from .models.account_models import Account, account_info_from_account
from .schemas.transaction_schemas import (
    TransactionCreateRequest,
    transaction_response_serializer,
    transaction_paginate_response_serializer,
)
from .services import transaction as transaction_service

transaction_router = APIRouter(prefix="/transaction")


@transaction_router.post("")
async def create_transaction(
    request: TransactionCreateRequest, activeAccount: Account = Depends(authenticate)
):
    """Create a new transaction"""
    transaction, error = transaction_service.create_transaction(
        name=request.name,
        amount=request.amount,
        timestamp=request.timestamp,
        kind=request.kind,
        account_info=account_info_from_account(activeAccount),
    )
    if error:
        raise HTTPException(status_code=error.code, detail=error.msg)

    if not transaction:
        raise HTTPException(status_code=500, detail="failed to create transaction")

    return transaction_response_serializer(transaction)


@transaction_router.get("/{id}")
async def get_transaction(id: str, activeAccount: Account = Depends(authenticate)):
    transaction, error = transaction_service.get_transaction(
        id, account_info_from_account(activeAccount)
    )

    if error:
        raise HTTPException(status_code=error.code, detail=error.msg)

    if not transaction:
        raise HTTPException(status_code=404, detail="transaction not found")

    return transaction_response_serializer(transaction)


@transaction_router.get("")
async def list_transactions(activeAccount: Account = Depends(authenticate)):
    transactions, paginator, error = transaction_service.list_transactions(
        page=1, per_page=30, account_info=account_info_from_account(activeAccount)
    )

    if error:
        raise HTTPException(status_code=error.code, detail=error.msg)

    if not transactions:
        raise HTTPException(status_code=404, detail="no transactions found")

    return transaction_paginate_response_serializer(transactions, paginator)
