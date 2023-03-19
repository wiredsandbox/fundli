from .database import Database


class TransactionDatabase(Database):
    def __init__(self):
        super().__init__("transactions")


transaction_database = TransactionDatabase()
