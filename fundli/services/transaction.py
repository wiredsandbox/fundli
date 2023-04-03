import datetime

from bson.errors import InvalidId
from bson.objectid import ObjectId

from fundli.database.transaction import transaction_database
from fundli.errors.error import Error
from fundli.models.account_models import AccountInfo
from fundli.models.transaction_models import Transaction

from .shared import parse_datetime

TRANSACTION_KIND_INCOME = "INCOME"
TRANSACTION_KIND_EXPENSE = "EXPENSE"


def create_transaction(
    name: str,
    amount: float,
    timestamp: str,
    kind: str,
    tags: list,
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
            "invalid transaction timestamp, expects format '2009-01-01T14:01:02-04:00'",
            400,
        )
    transaction_timestamp = transaction_timestamp.astimezone(datetime.timezone.utc)

    transaction = Transaction(
        id=ObjectId(),
        created_at=transaction_timestamp,
        updated_at=datetime.datetime.utcnow(),
        name=name,
        amount=int(amount * 100),
        kind=kind,
        tags=tags,
        account_info=account_info,
    )

    try:
        transaction_database.create(transaction)
    except Exception:
        return None, Error("failed to create transaction", 500)

    return transaction, None


def get_transaction(id: str, account_info: AccountInfo):
    try:
        oid = ObjectId(id)
        query_filter = {"_id": oid}

        if account_info.id:
            query_filter["account_info.id"] = account_info.id

        transaction = transaction_database.find_one(query_filter)

        if not transaction:
            return None, Error("transaction not found", 404)
        return transaction, None

    except InvalidId:
        return None, Error("invalid id", 400)


def list_transactions(page: int, per_page: int, account_info: AccountInfo):
    query_filter = {}

    if account_info.id:
        query_filter["account_info.id"] = account_info.id

    transactions, paginator, error = transaction_database.paginate(
        query_filter, page, per_page
    )
    if error:
        return None, None, Error("failed to list transactions", 500)

    return transactions, paginator, None


def update_transaction(
    name: str = None,
    amount: float = None,
    timestamp: str = None,
    kind: str = None,
    tags: list = None,
    transaction: Transaction = None,
):
    old_transaction = transaction
    if name is not None:
        transaction.name = name

    if amount is not None:
        transaction.amount = int(amount * 100)

    if timestamp is not None:
        transaction_timestamp = parse_datetime(timestamp)
        if not transaction_timestamp:
            return None, Error(
                "invalid transaction timestamp, expects format '2009-01-01T14:01:02-04:00'",
                400,
            )
        transaction_timestamp = transaction_timestamp.astimezone(datetime.timezone.utc)
        transaction.created_at = transaction_timestamp

    if kind is not None:
        if kind.upper() not in (TRANSACTION_KIND_INCOME, TRANSACTION_KIND_EXPENSE):
            return None, Error("invalid transaction kind", 400)
        transaction.kind = kind.upper()

    if tags is not None:
        # create property for tags
        transaction.tags += tags

    transaction.updated_at = datetime.datetime.utcnow()

    # if old_transaction.tags == [] or old_transaction.tags is None:
    #     del old_transaction.tags

    try:
        transaction_database.update(old_transaction.to_dict(), transaction.to_dict())
    except Exception:
        return None, Error("failed to update transaction", 500)
    return transaction, None
