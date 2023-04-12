from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel

from fundli.models.wallet_models import Wallet
from fundli.database.paginator import Paginator
from fundli.schemas.shared import PaginatorResponse, paginator_response_serializer

from .account_schemas import AccountInfoResponse


class WalletCreateRequest(BaseModel):
    name: str


class WalletResponse(BaseModel):
    id: str
    createdAt: datetime
    updatedAt: datetime
    name: str
    accountInfo: AccountInfoResponse


class WalletPaginateResponse(BaseModel):
    wallets: List[WalletResponse]
    paginator: Union[PaginatorResponse, None]


# ---------------------------------------------------------------------------------------------------------------
#                                             Serializers
# ---------------------------------------------------------------------------------------------------------------


def wallet_response_serializer(wallet: Wallet):
    return WalletResponse(
        id=str(wallet.id),
        createdAt=wallet.created_at,
        updatedAt=wallet.updated_at,
        name=wallet.name,
        accountInfo=AccountInfoResponse(
            id=str(wallet.account_info.id),
            email=wallet.account_info.email,
            firstName=wallet.account_info.first_name,
            lastName=wallet.account_info.last_name,
        ),
    )


def wallet_paginate_response_serializer(
    wallets: List[Wallet], paginator: Union[Paginator, None]
):
    return WalletPaginateResponse(
        wallets=[wallet_response_serializer(wallet) for wallet in wallets],
        paginator=paginator_response_serializer(paginator) if paginator else None,
    )
