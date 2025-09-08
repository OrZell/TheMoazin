from DALs.ElasticSearch_DAL import Elastic
from DALs.MongoDB_DAL import MongoDB_DAL
from DALs.Kafka import Kafka
import hashlib
import json
import os


class Manager:

    def __init__(self):
        self.Kafka = Kafka()
        self.Elastic = Elastic()
        self.MongoDB = MongoDB_DAL()

        self.Topic = os.getenv('KAFKA_FIRST_PUBLISH_TOPIC')



    def run(self):
        self.Elastic.create_index()
        events = self.Kafka.get_consumer_events(topic=[self.Topic])

        for event in events:
            # print(event)
            # continue
            event = event.value
            print(event)
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
            'name': event['metadata']['file_name'],
            'file_path': event['file_path'],
            'size': event['metadata']['size_kb'],
            'create_date': event['metadata']['creation_date'],
            'modified_date': event['metadata']['modified_date'],
            'last_access': event['metadata']['last_access_date']
        }

        return elastic_doc


    def insert_wav_to_mongodb(self, event):
        fs = self.MongoDB.get_fs()
        file_id, file_path = event['id'], event['file_path']

        with open(file_path, 'rb') as file_data:
            fs.put(file_data, file_id=file_id)

        self.MongoDB.close_fs()