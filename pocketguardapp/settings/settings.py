from decouple import config

SECRET_KEY = config("SECRET_KEY")
PORT = config("PORT", default=7000, cast=int)
