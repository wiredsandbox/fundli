from decouple import config

EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
PORT = config("PORT", default=7000, cast=int)
SECRET_KEY = config("SECRET_KEY")
DATABASE_URI = str(config("DATABASE_URI"))
DATABASE_NAME = str(config("DATABASE_NAME"))
