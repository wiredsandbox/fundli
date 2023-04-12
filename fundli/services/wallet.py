from datetime import datetime

from bson.objectid import ObjectId
from bson.errors import InvalidId

from fundli.database.wallet import wallet_database
from fundli.models.account_models import AccountInfo
from fundli.models.wallet_models import Wallet
from fundli.errors.error import Error


def create_wallet(
    name: str,
    account_info: AccountInfo,
):
    if not name:
        return None, Error("name is required", 400)

    if not account_info.id:
        return None, Error("account info is required", 400)

    wallet = Wallet(
        id=ObjectId(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        name=name,
        account_info=account_info,
    )

    try:
        wallet_database.create(wallet)
    except Exception:
        return None, Error("failed to create wallet", 500)

    return wallet, None


def get_wallet(identifier: str, account_info: AccountInfo):
    query_filter = {}

    try:
        oid = ObjectId(identifier)
        query_filter["_id"] = oid
    except InvalidId:
        query_filter["name"] = identifier

    if account_info.id:
        query_filter["account_info.id"] = account_info.id

    wallet = wallet_database.find_one(query_filter)

    if not wallet:
        return None, Error("wallet not found", 404)

    return wallet, None


def list_wallets(page: int, per_page: int, account_info: AccountInfo):
    query_filter = {}

    if account_info.id:
        query_filter["account_info.id"] = account_info.id

    wallets, paginator, error = wallet_database.paginate(query_filter, page, per_page)
    if error:
        return None, None, Error("failed to list wallets", 500)

    return wallets, paginator, None
