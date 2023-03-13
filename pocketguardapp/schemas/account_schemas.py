from pydantic import BaseModel


class AccountRequest(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
