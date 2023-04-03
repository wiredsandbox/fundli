from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class EmailTemplate(str, Enum):
    welcome = "welcome.html"
    password_reset = "password_reset.html"
    email_verification = "email_verification.html"
    success = "success.html"


class EmailSchema(BaseModel):
    email_template: Optional[EmailTemplate] = None
    subject: Optional[str]
    sender_name: Optional[str] = None
    sender_email: str = None
    recipients: List[EmailStr]
    title: Optional[str]
    first_name: Optional[str]
    body: Optional[str] = None
    description: Optional[str] = None


class EmailResponse(BaseModel):
    message: str
