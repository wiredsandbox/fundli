import datetime
import re

import bcrypt
from bson.errors import InvalidId
from bson.objectid import ObjectId
from jose import jwt

from pocketguardapp.database.account import account_database
from pocketguardapp.errors.error import Error
from pocketguardapp.models.account_models import Account
from pocketguardapp.settings.settings import EMAIL_REGEX, SECRET_KEY


def create_account(email: str, password: str, first_name: str, last_name: str):
    """
    create_account creates a new account.
    It validates the email and checks that the email is not already in use.
    It returns the new account and an error if there is one.
    """
    if not is_valid_email(email):
        return None, Error("invalid email", 400)

    query_filter = {"email": email}
    if account_database.count(query_filter) > 0:
        return None, Error("email already in use", 400)

    account = Account(
        id=ObjectId(),
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow(),
        email=email,
        password=hash_password(password),
        first_name=first_name,
        last_name=last_name,
    )

    try:
        account_database.create(account)
    except Exception as e:
        print(e)
        return None, Error("failed to create account", 500)

    return account, None


def get_account(idOrEmail):
    """fetch account from database"""
    if idOrEmail == "":
        return None, Error("id or email is required", 400)

    query_filter = {}
    try:
        oid = ObjectId(idOrEmail)
        query_filter = {"_id": oid}
    except InvalidId:
        query_filter["email"] = idOrEmail

    account = account_database.find_one(query_filter)
    if not account:
        return None, Error("account not found", 404)

    return account, None


def login_account(email, password):
    if not is_valid_email(email):
        return None, Error("invalid email", 400)

    if not compare_password(password, hash_password(password)):
        return None, Error("invalid password", 400)

    return get_account(email)


def hash_password(password):
    """
    hash_password returns an encrypted version of the password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def compare_password(password, hashed_password):
    """
    compare_password compares a password with a hashed password.
    It returns True if they match, False otherwise.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


# generate token
def generate_token(email, first_name, last_name):
    # encode secret key with HS256 algorithm

    # token = jws.sign(
    #     payload={
    #         "email": email,
    #         "name": f"{first_name} {last_name}",
    #         "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30),
    #         "iat": datetime.datetime.utcnow(),
    #         "iss": "pocketguard-api",
    #         "aud": "pocketguard-app",
    #     },
    #     key=SECRET_KEY,
    #     algorithm="HS256",
    # )
    token = jwt.encode(
        claims={
            "email": email,
            "name": f"{first_name} {last_name}",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30),
            "iat": datetime.datetime.utcnow(),
            "iss": "pocketguard-api",
            "aud": "pocketguard-app",
        },
        key=SECRET_KEY,
        algorithm="HS256",
    )

    return token


# decode token
def decode_token(token):
    # return jws.verify(token, SECRET_KEY, algorithms=["HS256"])
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=["HS256"],
        audience="pocketguard-app",
        issuer="pocketguard-api",
    )


# check if email is a valid email
def is_valid_email(email):
    if re.fullmatch(EMAIL_REGEX, email):
        return True
    return False
