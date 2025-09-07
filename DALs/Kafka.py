from kafka import KafkaProducer, KafkaConsumer
from dotenv import load_dotenv, find_dotenv
import json
import os

load_dotenv(find_dotenv())

class Kafka:

    def __init__(self):
        self.Host = os.getenv('KAFKA_HOST')
        self.Port = os.getenv('KAFKA_PORT')
        self.Group = os.getenv('KAFKA_GROUP')
        self.URI = os.getenv('KAFKA_CONNECT_STRING')

    def get_producer_config(self):
        producer = KafkaProducer(bootstrap_servers=[self.URI],
                                 value_serializer=lambda x:
                                 json.dumps(x).encode('utf-8'))
        return producer

    def get_consumer_events(self, topic):
        consumer = KafkaConsumer(*topic,
                                 group_id=self.Group,
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                 bootstrap_servers=[self.URI])

        # consumer_timeout_ms = 10000 optional

        return consumer

    def publish_message(self, topic, message):
        producer = self.get_producer_config()
        producer.send(topic=topic, value=message)
        producer.flush()

    def publish_message_with_key(self, topic, key, message):
        producer = self.get_producer_config()
        producer.send(topic, key=key, value=message)