import datetime
import re
from random import randint

import bcrypt
from bson.errors import InvalidId
from bson.objectid import ObjectId
from jose import jwt

from fundli.database.account import account_database
from fundli.email_service.email_schema import EmailResponse, EmailSchema
from fundli.email_service.email_service import send_email
from fundli.errors.error import Error
from fundli.models.account_models import Account
from fundli.settings.settings import EMAIL_REGEX, SECRET_KEY


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

    token = jwt.encode(
        claims={
            "email": email,
            "name": f"{first_name} {last_name}",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30),
            "iat": datetime.datetime.utcnow(),
            "iss": "fundli-api",
            "aud": "fundli-app",
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
        audience="fundli-app",
        issuer="fundli-api",
    )


# check if email is a valid email
def is_valid_email(email):
    if re.fullmatch(EMAIL_REGEX, email):
        return True
    return False


def generate_verification_code(n: int):
    range_start = 10 ** (n - 1)
    range_end = (10**n) - 1
    return randint(range_start, range_end)


def forgot_password(email: str, code: int):
    if not is_valid_email(email):
        return None, Error("invalid email", 400)

    account, error = get_account(email)
    if error:
        return None, error
    if not account:
        return None, Error("account not found", 404)

    account_update = {"password_verification_code": code}
    query = {"_id": account.id}
    try:
        account_database.update(query, account_update)
    except Exception as e:
        print(e)
        return None, Error("failed to update account", 500)
    return send_verification_code(account, code), None


def send_verification_code(account: Account, code: int):
    send_email(
        EmailSchema(
            recipients=[account.email],
            subject="Fundli Verification Code",
            body=code,
            sender_email="info@fundli.live",
            sender_name="Favour from Fundli",
            first_name=account.first_name,
            email_template="password_reset.html",
        )
    )

    return EmailResponse(message="Verification code sent successfull")


def verify_code(account: Account, code: int):
    print(account.password_verification_code, code)
    if account.password_verification_code == code:
        return True, None
    return False, Error("invalid verification code", 400)


def reset_password(email: str, password: str, code: int):
    if not is_valid_email(email):
        return None, Error("invalid email", 400)

    account, error = get_account(email)
    if error:
        return None, error
    if not account:
        return None, Error("account not found", 404)

    _, error = verify_code(account, code)
    if error:
        return None, error

    account_update = {"password": hash_password(password)}
    query = {"_id": account.id}

    try:
        account_database.update(query, account_update)
    except Exception as e:
        print(e)
        return None, Error("failed to update account", 500)
    return (
        send_email(
            EmailSchema(
                recipients=[account.email],
                subject="Fundli Password Reset",
                body="Your password has been reset successfully",
                sender_email="info@fundli.live",
                sender_name="Favour from Fundli",
                first_name=account.first_name,
                email_template="success.html",
            )
        ),
        None,
    )
