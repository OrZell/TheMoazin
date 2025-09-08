from DALs.Kafka import Kafka
from Models.Reader import Reader
import os

class Manager:

    def __init__(self):
        self.Reader = Reader() # instance of the Reader class
        self.Kafka = Kafka() # instance of Kafka class
        self.Topic = os.getenv('KAFKA_FIRST_PUBLISH_TOPIC') # MainDirPath holds the var of the env MAIN_DATA_PATH
                                                            # that means the path of the main podcats dir

    # get dict with the details for each file, loop through, and
    # publish them in kafka use the self.Topic as topic
    def publish_the_jsons(self):
        dct_with_details = self.Reader.get_list_of_details()

        for js in dct_with_details:
            self.Kafka.publish_message(message=js, topic=self.Topic)