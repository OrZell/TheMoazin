from elasticsearch import Elasticsearch, helpers
import os



class Elastic:

    def __init__(self):
        self.Host = os.getenv('ELASTICSEARCH_HOTS')
        self.Port = os.getenv('ELASTICSEARCH_PORT')
        self.ConnectString = os.getenv('ELASTICSEARCH_CONNECTION_STRING')
        self.IndexName = os.getenv('ELASTICSEARCH_INDEX')

        self.connection = None

        self.Map = {
            'properties': {
                'id': {'type': 'keyword'},
                'text': {'type': 'text'},
                'name': {'type': 'keyword'},
                'file_path': {'type': 'keyword'},
                'size': {'type': 'integer'},
                'create_date': {
                    'type': 'datetime',
                    'format': 'yyyy-MM-dd HH:mm:ss'
                },
                'modified_date': {
                    'type': 'datetime',
                    'format': 'yyyy-MM-dd HH:mm:ss'
                },
                'last_access': {
                    'type': 'datetime',
                    'format': 'yyyy-MM-dd HH:mm:ss'
                }
            }
        }

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
            connection.indices.create(index=self.IndexName)
        self.close_connection()

    def insert_one(self, doc):
        connection = self.open_connection()

        connection.index(index=self.IndexName, body=doc)

        self.close_connection()

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