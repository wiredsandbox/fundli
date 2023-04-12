from fastapi import APIRouter, Depends, HTTPException

from .middlewares.middleware import authenticate, pagination_options
from .models.account_models import Account, account_info_from_account
from .schemas.wallet_schemas import (
    WalletCreateRequest,
    wallet_response_serializer,
    wallet_paginate_response_serializer,
)
from .services import wallet as wallet_service


wallet_router = APIRouter(prefix="/wallet")


@wallet_router.post("")
async def create_wallet(
    request: WalletCreateRequest, activeAccount: Account = Depends(authenticate)
):
    """Create a new wallet"""
    wallet, error = wallet_service.create_wallet(
        name=request.name,
        account_info=account_info_from_account(activeAccount),
    )
    if error:
        raise HTTPException(status_code=error.code, detail=error.msg)

    if not wallet:
        raise HTTPException(status_code=500, detail="failed to create wallet")

    return wallet_response_serializer(wallet)


@wallet_router.get("/{idOrName}")
async def get_wallet(idOrName: str, activeAccount: Account = Depends(authenticate)):
    wallet, error = wallet_service.get_wallet(
        idOrName, account_info_from_account(activeAccount)
    )
    if error:
        raise HTTPException(status_code=error.code, detail=error.msg)

    if not wallet:
        raise HTTPException(status_code=404, detail="wallet not found")

    return wallet_response_serializer(wallet)


@wallet_router.get("")
async def list_wallets(
    activeAccount: Account = Depends(authenticate),
    pagination=Depends(pagination_options),
):
    wallets, paginator, error = wallet_service.list_wallets(
        page=pagination["page"],
        per_page=pagination["per_page"],
        account_info=account_info_from_account(activeAccount),
    )

    if error:
        raise HTTPException(status_code=error.code, detail=error.msg)

    if not wallets:
        raise HTTPException(status_code=404, detail="no wallets found")

    return wallet_paginate_response_serializer(wallets, paginator)
