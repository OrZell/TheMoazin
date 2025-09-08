from DALs.ElasticSearch_DAL import Elastic
from DALs.MongoDB_DAL import MongoDB_DAL
from STT import STT

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Manager:

    def __init__(self):
        self.Elastic = Elastic()
        self.MongoDAL = MongoDB_DAL()
        self.STT = STT()

    def run(self):
        dct_of_docs_from_elastic = self.fetch_all_docs_from_elastic()
        dct_with_text = self.loop_through_dct_of_docs_and_add_text_field(dct_of_docs_from_elastic)
        self.insert_the_docs_to_elastic(dct_with_text)

    def fetch_all_docs_from_elastic(self) -> list:
        docs = self.Elastic.fetch_all()
        return docs['hits']['hits']

    def fetch_doc_from_mongo_by_id(self, id):
        fs = self.MongoDAL.get_fs()
        audio_file = fs.find_one({'file_id': id})
        return audio_file

    def loop_through_dct_of_docs_and_add_text_field(self, lst:list) -> dict:
        new_ordered_dct = {}

        for doc in lst:
            new_ordered_dct[doc['_id']] = doc['_source']
            doc_inner_id = doc['_source']['id']
            doc_audio = self.fetch_doc_from_mongo_by_id(doc_inner_id)
            doc_text = self.STT.convert_audio_to_text(doc_audio)
            new_ordered_dct[doc['_id']]['text'] = doc_text

        return new_ordered_dct

    def insert_the_docs_to_elastic(self, dct:dict):
        self.Elastic.insert_list_of_docs(dct)


manager = Manager()
manager.run()