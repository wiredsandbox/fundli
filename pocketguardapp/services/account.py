import bcrypt
import datetime
import jwt
import re
from pocketguardapp.settings.settings import SECRET_KEY, EMAIL_REGEX


def create_account():
    pass


def hash_password(password):
    """
    hash_password returns an encrypted version of the password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def compare_password(password, hashed_password):
    """
    compare_password compares a password with a hashed password.
    It returns True if they match, False otherwise.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)


# generate token from email, first name, last name
def generate_token(email, first_name, last_name):
    return jwt.encode(
        {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30),
        },
        SECRET_KEY,
        algorithm="RS256",
    )


# decode token
def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms="RS256")


# check if email is a valid email
def is_valid_email(email):
    if re.fullmatch(EMAIL_REGEX, email):
        return True
    return False
