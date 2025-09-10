import json

import uvicorn

from DALs.ElasticSearch_DAL import Elastic
from fastapi import FastAPI


app =FastAPI() # instance of FastAPI server
elastic = Elastic() # instance of elasticsearch DAL


@app.get('/')
# shows little list that explain about the service paths
def homepage():

    home_string = ['/is_bds - returns all the docs that is_bds True',
                   '/high_thread_level - returns all the docs that bds_thread_level high',
                   '/middle_thread_level - returns all the docs that bds_thread_level middle',
                   '/all_logs - returns all the logs',
                   '/doc_logs (?id=...) - returns all the logs of this doc']

    return home_string

@app.get('/is_bds')
# returns all the is_bds True docs
def send_the_docs_is_bds():
    query = {
        "query": {
            "match": {
                'is_bds': True
            }
        }
    }
    docs = elastic.search_by_query(query)['hits']['hits']
    return docs

@app.get('/high_thread_level')
# returns all the docs that thread_level high
def send_the_docs_thread_level_high():
    query = {
        "query": {
            "match": {
                'bds_thread_level': 'high'
            }
        }
    }
    docs = elastic.search_by_query(query)['hits']['hits']
    return docs

@app.get('/middle_thread_level')
# returns all the docs that thread_level middle
def send_the_docs_thread_level_middle():
    query = {
        "query": {
            "match": {
                'bds_thread_level': 'middle'
            }
        }
    }
    docs = elastic.search_by_query(query)['hits']['hits']
    return docs

@app.get('/all_logs')
# returns all the logs
def get_all_logs():
    docs = elastic.fetch_all_from_logs()['hits']['hits']
    return docs


@app.get('/doc_logs')
# returns logs of doc by id
def get_logs_of_doc_by_id(doc_id):
    query = {
        "query": {
            "match": {
                'message': doc_id
            }
        }
    }
    docs = elastic.search_by_query_in_logs(query)['hits']['hits']
    return docs


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
