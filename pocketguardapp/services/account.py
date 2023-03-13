import bcrypt
import datetime
import jwt
import re

from bson.objectid import ObjectId

from pocketguardapp.errors.error import Error
from pocketguardapp.settings.settings import SECRET_KEY, EMAIL_REGEX
from pocketguardapp.database.account import account_database
from pocketguardapp.models.account_models import Account


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

    account = Account()
    account.id = ObjectId()
    account.created_at = datetime.datetime.utcnow()
    account.updated_at = account.created_at
    account.email = email
    account.password = hash_password(password)
    account.first_name = first_name
    account.last_name = last_name
    account.used_projection = False

    try:
        account_database.create(account)
    except Exception as e:
        print(e)
        return None, Error("failed to create account", 500)

    return account, None


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
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)


# generate token 
def generate_token(email, first_name, last_name):
    # encode  secret key with RS256 algorithm

    token = jwt.encode(
        payload={
            "email": email,
            "name": f"{first_name} {last_name}",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30),
        },
        key=SECRET_KEY,
        algorithm="HS256",
    )

    return token


# decode token
def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms="RS256")


# check if email is a valid email
def is_valid_email(email):
    if re.fullmatch(EMAIL_REGEX, email):
        return True
    return False

# function to check token validity and return id 
def get_account(token):
    try:
        decoded_token = decode_token(token)
    except Exception as e:
        print(e)
        return None, Error("invalid token", 401)

    query_filter = {"email": decoded_token["email"]}
    account = account_database.find_one(query_filter)
    if not account:
        return None, Error("account not found", 404)

    return account, None
