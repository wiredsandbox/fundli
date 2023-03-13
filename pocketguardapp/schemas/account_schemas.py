from pydantic import BaseModel




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
