from DALs.ElasticSearch_DAL import Elastic
from DALs.MongoDB_DAL import MongoDB_DAL
from Models.Logger import Logger
from Models.STT import STT

class Manager:

    def __init__(self):
        self.Logger = Logger.get_logger() # Gets the logger with connection to es
        self.MongoDAL = MongoDB_DAL() # instance of MongoDB DAL
        self.Elastic = Elastic() # instance of Elasticsearch class
        self.STT = STT() # instance of STT

    # main method
    def run(self):
        dct_of_docs_from_elastic = self.fetch_all_docs_from_elastic() # gets list of docs from elastic
        self.loop_through_dct_of_docs_and_add_text_field(dct_of_docs_from_elastic) # every doc create field text and assign the
                                                                                   # text from the audio index to elastic and continue
    #fetch all docs from elastic
    def fetch_all_docs_from_elastic(self) -> list:
        try:
            docs = self.Elastic.fetch_all()
            self.Logger.info('Fetch all docs from Elastic successed')
        except:
            self.Logger.error('Fetch all docs from Elastic failed')
        return docs['hits']['hits']

    # fetch doc from mongo by the id
    def fetch_doc_from_mongo_by_id(self, id):
        fs = self.MongoDAL.get_fs()
        audio_file = None
        try:
            audio_file = fs.find_one({'file_id': id})
            self.Logger.info(f'Fetch doc from Mongo successed doc_id - {id}')
        except:
            self.Logger.error(f'Fetch doc from Mongo failed doc_id - {id}')
        return audio_file

    # every doc from elastic become to the source, assign text and send back to elastic
    def loop_through_dct_of_docs_and_add_text_field(self, lst:list):
        for doc in lst:
            source_doc = doc['_source']
            doc_id = source_doc['id']
            doc_audio = self.fetch_doc_from_mongo_by_id(doc_id)
            doc_text = self.STT.convert_audio_to_text(doc_audio)
            source_doc['text'] = doc_text
            self.Logger.info(f'Created text from doc_id - {doc_id}')

            try:
                self.Elastic.insert_one_with_id(doc=source_doc, id=source_doc['id'])
                self.Logger.info(f'Insert to Elastic succeseed doc_id - {doc_id}')
            except:
                self.Logger.error(f'Insert to Elastic failed doc_id - {doc_id}')