from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class AccountRequest(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
