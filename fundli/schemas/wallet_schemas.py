from datetime import datetime
from pydantic import BaseModel

from fundli.models.wallet_models import Wallet

from .account_schemas import AccountInfoResponse


class WalletCreateRequest(BaseModel):
    name: str


class WalletResponse(BaseModel):
    id: str
    createdAt: datetime
    updatedAt: datetime
    name: str
    accountInfo: AccountInfoResponse


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
