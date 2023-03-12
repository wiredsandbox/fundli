from datetime import datetime


class Account:
    id: str
    created_at: datetime
    updated_at: datetime

    email: str
    password: str
    first_name: str
    last_name: str

    # don't write these fields to the database
    used_projection: bool

    def to_dict(self):
        """to_dict returns a dict representation of the Account"""
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "email": self.email,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
