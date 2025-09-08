from DALs.ElasticSearch_DAL import Elastic
from DALs.MongoDB_DAL import MongoDB_DAL
from Models.Logger import Logger
from DALs.Kafka import Kafka
import hashlib
import json
import os


class Manager:

    def __init__(self):
        self.Kafka = Kafka() # instance of Kafka class
        self.Elastic = Elastic() # instance of Elasticsearch class
        self.MongoDB = MongoDB_DAL() # instance of MongoDB DAL
        self.Logger = Logger.get_logger() # Gets the logger with connection to es

        self.Topic = os.getenv('KAFKA_FIRST_PUBLISH_TOPIC') # MainDirPath holds the var of the env MAIN_DATA_PATH
                                                            # that means the path of the main podcats dir



    # the main method that get the events from the known topic manipulate them, index
    # the files details in elasticsearch and insert the files in mongodb using GridFS
    def run(self):
        self.Logger.info('Service Consumer Started')
        self.Elastic.create_index()
        events = self.Kafka.get_consumer_events(topic=[self.Topic])
        self.Logger.info(f'Start Listen to topic {self.Topic}')

        for event in events:
            # print(event)
            # continue
            event = event.value
            self.generate_unique_id(event)

            elastic_doc = self.create_elastic_doc_from_event(event)

            try:
                self.Elastic.insert_one(elastic_doc)
                self.Logger.info(f'Insert doc to Elasticsearch id-{event['id']}')
            except:
                self.Logger.error(f'Field to insert the doc id - {event['id']} to Elasticsearch')

            try:
                self.insert_wav_to_mongodb(event)
                self.Logger.info(f'Insert doc to MongoDB id-{event['id']}')
            except:
                self.Logger.error(f'Field to insert the doc id - {event['id']} to MongoDB')


    @staticmethod
    #generate unique md5 id each file using hashlib library
    def generate_unique_id(event:dict):
        md5_hash = hashlib.md5(json.dumps(event, sort_keys=True).encode('utf8')).hexdigest()
        event['id'] = md5_hash

    @staticmethod
    # create doc that stands for the fields in the elasticsearch
    def create_elastic_doc_from_event(event) -> dict:
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

    # open the file based on the file path from the event then upload
    # it mongo using GridFS
    def insert_wav_to_mongodb(self, event):
        fs = self.MongoDB.get_fs()
        file_id, file_path = event['id'], event['file_path']

        with open(file_path, 'rb') as file_data:
            fs.put(file_data, file_id=file_id)

        self.MongoDB.close_fs()