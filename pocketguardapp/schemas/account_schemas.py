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


class AccountAuthResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    token: str

    class config:
        example = {
            "email": "example@example.com",
            "id": "5f9f1c5b9c9d4b0b8c1c1c1c",
            "first_name": "John",
            "last_name": "Doe",
        }


class AccountResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str


def account_auth_response_serializer(account: Account, token: str):
    """account_response_serializer serializes an account to an AccountResponse"""

    return AccountAuthResponse(token=token, id=str(account.id), **account.to_dict())


def single_account_response(account: Account):
    """single_account_response serializes an account to an AccountResponse"""

    return AccountResponse(id=str(account.id), **account.to_dict())
