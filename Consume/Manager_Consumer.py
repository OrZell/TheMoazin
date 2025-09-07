from DALs.ElasticSearch_DAL import Elastic
from DALs.MongoDB_DAL import MongoDB_DAL
from DALs.Kafka import Kafka
import hashlib
import gridfs
import json
import os


class Manager:

    def __init__(self):
        self.Kafka = Kafka()
        self.Elastic = Elastic()
        self.MongoDB = MongoDB_DAL()

        self.Topic = os.getenv('KAFKA_FIRST_PUBLISH')


    def run(self):
        self.Elastic.create_index()
        events = self.Kafka.get_consumer_events(topic=[self.Topic])

        for event in events:
            event = event.value
            self.generate_unique_id(event)

            elastic_doc = self.create_elastic_doc_from_event(event)

            self.Elastic.insert_one(elastic_doc)
            self.insert_wav_to_mongodb(event)

    @staticmethod
    def generate_unique_id(event:dict):
        md5_hash = hashlib.md5(json.dumps(event, sort_keys=True).encode('utf8')).hexdigest()
        event['id'] = md5_hash

    @staticmethod
    def create_elastic_doc_from_event(event):
        elastic_doc = {
            'id': event['id'],
            'name': event['Metadata']['File Name'],
            'file_path': event['File Path'],
            'size': event['Metadata']['Size (KB)'],
            'create_date': event['Metadata']['Creation Date'],
            'modified_date': event['Metadata']['Modified Date'],
            'last_access': event['Metadata']['Last Access Date']
        }

        return elastic_doc


    def insert_wav_to_mongodb(self, event):
        fs = gridfs.GridFS(self.MongoDB.get_database())
        file_id, file_path = event['id'], event['File Path']

        with open(file_path, 'rb') as file_data:
            fs.put(file_data, file_id=file_id)

        self.MongoDB.close_connection()
