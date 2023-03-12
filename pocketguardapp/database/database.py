from pymongo import MongoClient
from settings.settings import DATABASE_URI, DATABASE_NAME

client = MongoClient("localhost", 27017)
