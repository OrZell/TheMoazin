from pymongo import MongoClient
import os

class MongoDB_DAL:

    def __init__(self):
        self.HOST = os.getenv('MONGODB_HOST')
        self.PORT = os.getenv('MONGODB_PORT')
        self.ConnectionString = os.getenv('MONGODB_CONNECTION_STRING')

        self.DB = os.getenv('MONGODB_DB')
        self.Collection = os.getenv('MONGODB_COLLECTION')

        self.connection = None

    def open_connection(self):
        if self.connection is None:
            self.connection = MongoClient(self.ConnectionString)
        return self.connection

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def get_database(self):
        connection = self.open_connection()
        return connection[self.DB]

    def insert_one(self, doc):
        connection = self.open_connection()
        connection[self.DB][self.Collection].insert_one(doc)
        self.close_connection()

    def update_one(self, id, query):
        connection = self.open_connection()
        connection[self.DB][self.Collection].update_one(id, query)
        self.close_connection()

    def read_one(self, field, value, query=None):

        # field is the field in the document that you want to search the value in
        # value is the the value that you want to in the field

        if query is None:
            query = {field: value}

        connection = self.open_connection()
        doc = connection[self.DB][self.Collection].find_one(query)
        self.close_connection()

        return doc

    def delete_one(self, doc):
        connection = self.open_connection()
        connection[self.DB][self.Collection].delete_one(doc)
        self.close_connection()