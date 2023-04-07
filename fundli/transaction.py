from fastapi import APIRouter, Depends, HTTPException

from .middlewares.middleware import authenticate, pagination_options
from .models.account_models import Account, account_info_from_account
from .schemas.transaction_schemas import (
    TransactionCreateRequest,
    TransactionUpdateRequest,
    transaction_paginate_response_serializer,
    transaction_response_serializer,
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
        tags=request.tags,
        account_info=account_info_from_account(activeAccount),
        wallet_id=request.wallet_id,
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
async def list_transactions(
    activeAccount: Account = Depends(authenticate),
    pagination=Depends(pagination_options),
):
    transactions, paginator, error = transaction_service.list_transactions(
        page=pagination["page"],
        per_page=pagination["per_page"],
        account_info=account_info_from_account(activeAccount),
    )

    if error:
        raise HTTPException(status_code=error.code, detail=error.msg)

    if not transactions:
        raise HTTPException(status_code=404, detail="no transactions found")

    return transaction_paginate_response_serializer(transactions, paginator)


@transaction_router.put("/{id}")
async def update_transaction(
    id: str,
    request: TransactionUpdateRequest,
    activeAccount: Account = Depends(authenticate),
):
    account = account_info_from_account(activeAccount)

    transaction_acc, error = transaction_service.get_transaction(id, account)

    if error:
        return None, error

    transaction, error = transaction_service.update_transaction(
        name=request.name,
        amount=request.amount,
        timestamp=request.timestamp,
        kind=request.kind,
        tags=request.tags,
        transaction=transaction_acc,
        wallet_id=request.wallet_id,
    )

    if error:
        raise HTTPException(status_code=error.code, detail=error.msg)

    if not transaction:
        raise HTTPException(status_code=404, detail="transaction not found")

    return transaction_response_serializer(transaction)
