from pydantic import BaseModel
from pocketguardapp.models.account_models import Account


class AccountRequest(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class AccountLoginRequest(BaseModel):
    email: str
    password: str


class AccountResponse(BaseModel):
    email: str
    id: str
    first_name: str
    last_name: str
    token: str


def account_response_serializer(account: Account, token: str):
    """account_response_serializer serializes an account to an AccountResponse"""

    return AccountResponse(token=token, id=str(account.id), **account.to_dict())
