from pymongo import MongoClient
import gridfs
import os


class MongoDB_DAL:

    def __init__(self):
        self.HOST = os.getenv('MONGODB_HOST')
        self.PORT = os.getenv('MONGODB_PORT')
        self.ConnectionString = os.getenv('MONGODB_CONNECTION_STRING')

        self.DB = os.getenv('MONGODB_DB')
        self.Collection = os.getenv('MONGODB_COLLECTION')

        self.connection = None
        self.fs = None

    def open_connection(self):
        if self.connection is None:
            self.connection = MongoClient(self.ConnectionString)
        return self.connection

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def get_fs(self):
        if self.fs is None:
            connection = self.open_connection()
            self.fs = gridfs.GridFS(connection[self.DB])
        return self.fs

    def close_fs(self):
        if self.fs:
            self.close_connection()
            self.fs = None

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
        # value is the value that you want to in the field

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