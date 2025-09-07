from Kafka.Kafka import Kafka
from dotenv import load_dotenv, find_dotenv
from Reader import Reader
import os

load_dotenv(find_dotenv())

class Manager:

    def __init__(self):
        self.Reader = Reader()
        self.Kafka = Kafka()
        self.Topic = os.getenv('KAFKA_FIRST_PUBLISH')

    def publish_the_jsons(self):
        jsons = self.Reader.get_list_of_details()

        for js in jsons:
            self.Kafka.publish_message(message=js, topic=self.Topic)
