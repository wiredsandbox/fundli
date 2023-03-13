from datetime import datetime

from bson.objectid import ObjectId


class Account:
    def __init__(
        self,
        id: ObjectId,
        created_at: datetime,
        updated_at: datetime,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
    ):
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

        # don't write these fields to the database
        self.used_projection = False

    def to_dict(self):
        """to_dict returns a dict representation of the Account"""
        data = {
            "_id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "email": self.email,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
        return data