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

    class config:
        orm_mode = True
        example = {
            "email": "example@example.com",
            "id": "5f9f1c5b9c9d4b0b8c1c1c1c",
            "first_name": "John",
            "last_name": "Doe",
        }


def account_auth_response_serializer(account: Account, token: str):
    """account_response_serializer serializes an account to an AccountResponse"""

    return AccountResponse(token=token, id=str(account.id), **account.to_dict())
