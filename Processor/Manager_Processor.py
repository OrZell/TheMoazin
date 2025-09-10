from ElasticSearch_DAL import Elastic
from MongoDB_DAL import MongoDB_DAL
from Processor import Processor
from Logger import Logger
from STT import STT

class Manager:

    def __init__(self):
        self.Logger = Logger.get_logger() # Gets the logger with connection to es
        self.MongoDAL = MongoDB_DAL() # instance of MongoDB DAL
        self.Elastic = Elastic() # instance of Elasticsearch class
        self.STT = STT() # instance of STT
        self.Processor = Processor()

    # main method
    def run(self):
        self.Processor.run()
        lst_of_docs_from_elastic = self.fetch_all_docs_from_elastic() # gets list of docs from elastic
        self.loop_through_docs_and_add_them_text_and_bds_details_and_send_back(lst_of_docs_from_elastic) # every doc create field text and assign the
                                                                                                         # text from the audio index to elastic and continue
                                                                                                         # create and assign the bds details and send back to elastic

    #fetch all docs from elastic
    def fetch_all_docs_from_elastic(self) -> list:
        try:
            docs = self.Elastic.fetch_all()
            self.Logger.info('Fetch all docs from Elastic successed')
            return docs['hits']['hits']
        except:
            self.Logger.error('Fetch all docs from Elastic failed')

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

    # loop through docs and add them text and bds details and send them back one by one
    def loop_through_docs_and_add_them_text_and_bds_details_and_send_back(self, docs:list):
        for doc in docs:
            self.add_text_field(doc)
            self.add_bds_details(doc)
            self.send_back_the_doc_to_elastic(doc)
        self.Logger.info('Send all docs to elastic successed')

    # every doc from elastic become to the source, assign text and send back to elastic
    def add_text_field(self, doc:dict):
        source_doc = doc['_source']
        doc_id = doc['_id']
        doc_audio = self.fetch_doc_from_mongo_by_id(doc_id)
        doc_text = self.STT.convert_audio_to_text(doc_audio)
        source_doc['text'] = doc_text
        self.Logger.info(f'Created text from doc_id - {doc_id}')


    # add the bds details
    def add_bds_details(self, doc):
        source_doc = doc['_source']
        dict_text = source_doc['text']
        text_without_stopwords = self.Processor.remove_stop_words_from_text(dict_text)
        power_counts = self.Processor.count_power_of_hostile_words_in_text(text=dict_text)
        bds_precents = self.Processor.count_precents_of_bds(power_counts, text_without_stopwords)
        is_indicted = self.Processor.indicted_text_by_precents(bds_precents)
        classify_thread_level = self.Processor.threaded_text_by_precents(bds_precents)

        source_doc['bds_precent'] = bds_precents
        source_doc['is_bds'] = is_indicted
        source_doc['bds_thread_level'] = classify_thread_level

        self.Logger.info(f'Created bds details for doc_id - {source_doc['id']}')

    # send the doc to elastic based on docs id
    def send_back_the_doc_to_elastic(self, doc:dict):
        source_doc = doc['_source']
        doc_id = source_doc['id']

        try:
            self.Elastic.insert_one_with_id(doc=source_doc, id=doc_id)
            self.Logger.info(f'Insert to Elastic succeseed doc_id - {doc_id}')
        except:
            self.Logger.error(f'Insert to Elastic failed doc_id - {doc_id}')