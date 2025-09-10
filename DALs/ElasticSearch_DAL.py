from configuerations import ELASTICSEARCH_DOCS_INDEX_MAP
from elasticsearch import Elasticsearch, helpers
from Models.Logger import Logger
import os



class Elastic:

    def __init__(self):
        self.Logger = Logger.get_logger() # Gets the logger with connection to es
        self.Host = os.getenv('ELASTICSEARCH_HOST')
        self.Port = os.getenv('ELASTICSEARCH_PORT')
        self.ConnectString = os.getenv('ELASTICSEARCH_CONNECTION_STRING')
        self.IndexName = os.getenv('ELASTICSEARCH_DOCS_INDEX')

        self.connection = None

        self.Map = ELASTICSEARCH_DOCS_INDEX_MAP

    def open_connection(self):
        if self.connection is None:
            self.connection = Elasticsearch(self.ConnectString)
        return self.connection

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def create_index(self):
        connection = self.open_connection()
        if not connection.indices.exists(index=self.IndexName):
            connection.indices.create(index=self.IndexName, body=self.Map)
            self.Logger.info(f'Create Index {self.IndexName}')
        self.close_connection()

    def insert_one(self, doc):
        connection = self.open_connection()

        connection.index(index=self.IndexName, body=doc)

        self.close_connection()

    def insert_one_with_id(self, doc, id):
        connection = self.open_connection()

        connection.index(index=self.IndexName, body=doc, id=id)

        self.close_connection()

    def fetch_all(self):
        connection = self.open_connection()

        query = {
            'match_all': {}
        }

        result = connection.search(index=self.IndexName, query=query, size=1000)
        self.close_connection()
        return result

    def search_word_in_text(self, word):
        connection = self.open_connection()

        query = {
            "query": {
                "match": {
                    "text": word
                }
            }
        }
        result = connection.search(index=self.IndexName, body=query)

        self.close_connection()
        return result

    def delete_list_of_docs(self, docs):
        connection = self.open_connection()

        new_docs = []
        for doc in docs:
            new_docs.append({
                '_op_type': 'delete',
                '_index': self.IndexName,
                '_id': doc['_id']
            })

        helpers.bulk(connection, new_docs)

    def insert_list_of_docs(self, docs:dict):
        connection = self.open_connection()

        new_docs = []
        for doc in docs:
            new_docs.append({
                '_index': self.IndexName,
                '_id': doc,
                '_source': docs[doc]
            })

        helpers.bulk(connection, new_docs)