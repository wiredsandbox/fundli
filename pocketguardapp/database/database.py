from pymongo import MongoClient
from pocketguardapp.settings.settings import DATABASE_URI, DATABASE_NAME

client = MongoClient(host=DATABASE_URI)


class Database:
    def __init__(self, collection_name):
        self.database = client[DATABASE_NAME]
        self.collection = self.database[collection_name]

    def create(self, data):
        self.collection.insert_one(data.to_dict())

    def find_one(self, query_filter):
        return self.collection.find_one(query_filter)

    def count(self, query_filter):
        return self.collection.count_documents(query_filter)
