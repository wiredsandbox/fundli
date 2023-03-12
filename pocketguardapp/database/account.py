from database import Database

class AccountDatabase(Database):
    def __init__(self):
        super().__init__("accounts")

