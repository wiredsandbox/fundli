from pydantic import BaseModel


class AccountBase(BaseModel):
    email: str

class AccountRequest(AccountBase):
    email: str
    password: str
    first_name: str
    last_name: str

class AccountLoginRequest(AccountBase):
    password: str

class AccountResponse(AccountBase):
    id: str
    first_name: str
    last_name: str
    token: str
