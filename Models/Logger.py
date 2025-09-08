from dotenv import load_dotenv, find_dotenv
from elasticsearch import Elasticsearch
from datetime import datetime
import logging
import os

load_dotenv(find_dotenv())

class Logger:


    _logger = None
    @classmethod
    def get_logger(cls, name=os.getenv('LOGGER_NAME'),
                   es_host=os.getenv('ELASTICSEARCH_CONNECTION_STRING')
                   ,index=os.getenv('ELASTICSEARCH_LOGS_INDEX'),
                   level=logging.DEBUG):

        if cls._logger:
            return cls._logger

        logger = logging.getLogger(name)
        logger.setLevel(level)
        if not logger.handlers:
            es = Elasticsearch(es_host)

            mapping = {
                'mappings':{
                    'properties': {
                        'timestamp': {
                            'type': 'date',
                            'format': "yyyy-MM-dd'T'HH:mm:ss.SSSSSS"
                        },
                        'level': {'type': 'keyword'},
                        'logger': {'type': 'keyword'},
                        'message': {'type': 'text'}
                    }
                }
            }

            if not es.indices.exists(index=index):
                es.indices.create(index=index, body=mapping)

            class ESHandler(logging.Handler):
                def emit(self, record):
                    try:
                        es.index(index=index, document={
                            "timestamp": datetime.now().isoformat(),
                            "level": record.levelname,
                            "logger": record.name,
                            "message": record.getMessage()
                        })
                    except Exception as e:
                        print(f"ES log failed: {e}")
            logger.addHandler(ESHandler())
            logger.addHandler(logging.StreamHandler())
            cls._logger = logger
            return logger