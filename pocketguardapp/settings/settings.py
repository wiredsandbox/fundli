from decouple import config

SECRET_KEY = config("SECRET_KEY")
PORT = config("PORT", default=7000, cast=int)
EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
