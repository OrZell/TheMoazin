from DALs.ElasticSearch_DAL import Elastic
from DALs.MongoDB_DAL import MongoDB_DAL
from  Models.Logger import Logger
from STT import STT

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Manager:

    def __init__(self):
        self.Logger = Logger.get_logger()
        self.MongoDAL = MongoDB_DAL()
        self.Elastic = Elastic()
        self.STT = STT()

    def run(self):
        dct_of_docs_from_elastic = self.fetch_all_docs_from_elastic()
        dct_with_text = self.loop_through_dct_of_docs_and_add_text_field(dct_of_docs_from_elastic)
        # self.insert_the_docs_to_elastic(dct_with_text)

    def fetch_all_docs_from_elastic(self) -> list:
        docs = self.Elastic.fetch_all()
        self.Logger.info('Fetch all docs from Elastic successed')
        return docs['hits']['hits']

    def fetch_doc_from_mongo_by_id(self, id):
        fs = self.MongoDAL.get_fs()
        audio_file = fs.find_one({'file_id': id})
        self.Logger.info(f'Fetch doc from Mongo successed doc_id - {id}')
        return audio_file

    def loop_through_dct_of_docs_and_add_text_field(self, lst:list) -> dict:
        new_ordered_dct = {}

        for doc in lst:
            # new_ordered_dct[doc['_id']] = doc['_source']
            # doc_inner_id = doc['_source']['id']
            # doc_audio = self.fetch_doc_from_mongo_by_id(doc_inner_id)
            # doc_text = self.STT.convert_audio_to_text(doc_audio)
            # new_ordered_dct[doc['_id']]['text'] = doc_text

            source_doc = doc['_source']
            doc_inner_id = source_doc['id']
            doc_audio = self.fetch_doc_from_mongo_by_id(doc_inner_id)
            doc_text = self.STT.convert_audio_to_text(doc_audio)
            source_doc['text'] = doc_text


            self.Logger.info(f'Created text from doc_id - {doc_inner_id}')
            print(doc_text)
            self.Elastic.insert_one_with_id(doc=source_doc, id=doc['_id'])
            self.Logger.info(f'Insert to Elastic succeseed doc_id - {doc_inner_id}')

        return new_ordered_dct

    def insert_the_docs_to_elastic(self, dct:dict):
        self.Elastic.insert_list_of_docs(dct)
        self.Logger.info('Insert all the docs with the text field to Elastic successed')


manager = Manager()
manager.run()