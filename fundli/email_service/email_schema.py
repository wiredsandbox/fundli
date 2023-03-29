from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class EmailTemplate(str, Enum):
    welcome = "welcome.html"
    password_reset = "password_reset.html"


class EmailSchema(BaseModel):
    email_template: Optional[EmailTemplate] = None
    subject: Optional[str]
    sender_name: Optional[str] = None
    sender_email: str = "Uche from fundli <info@fundli.live>"
    recipients: List[EmailStr]
    title: Optional[str]
    first_name: Optional[str]
    body: Optional[str] = None
    description: Optional[str] = None
