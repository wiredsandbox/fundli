import datetime
from bson.objectid import ObjectId

from pocketguardapp.database.transaction import transaction_database
from pocketguardapp.errors.error import Error
from pocketguardapp.models.transaction_models import Transaction
from pocketguardapp.models.account_models import AccountInfo
from .services import parse_datetime


TRANSACTION_KIND_INCOME = "INCOME"
TRANSACTION_KIND_EXPENSE = "EXPENSE"


def create_transaction(
    name: str,
    amount: float,
    timestamp: str,
    kind: str,
    account_info: AccountInfo,
):
    """
    create_transaction creates a new transaction.
    A transaction is expected to be of kind INCOME or EXPENSE.
    """
    if not account_info.id:
        return None, Error("account info is required", 400)

    if kind.upper() not in (TRANSACTION_KIND_INCOME, TRANSACTION_KIND_EXPENSE):
        return None, Error("invalid transaction kind", 400)
    kind = kind.upper()

    if amount <= 0:
        return None, Error("invalid transaction amount, must be greater than 0", 400)

    transaction_timestamp = parse_datetime(timestamp)
    if not transaction_timestamp:
        return None, Error(
            "invalid transaction timestamp, expects format '%Y-%m-%dT%H:%M:%S.%f'", 400
        )

    transaction = Transaction(
        id=ObjectId(),
        created_at=transaction_timestamp,
        updated_at=datetime.datetime.utcnow(),
        name=name,
        amount=int(amount * 100),
        kind=kind,
        account_info=account_info,
    )

    try:
        transaction_database.create(transaction)
    except Exception as e:
        return None, Error("failed to create transaction", 500)

    return transaction, None
