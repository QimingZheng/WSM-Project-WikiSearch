from wikisearch.indexer.build_index_util import load_meta
from wikisearch.searcher import boolean_searcher, cosine_searcher, proximity_searcher, searcher_util, tfidf_searcher
import os
import json
import time


def read_file(path):
    with open(path, 'r') as f:
        return json.loads(f.read())


docs_path = "../data/parsed/docs"
meta_data = read_file(os.path.join(docs_path, "meta.json"))

search_method = {}


def search(searchParams):
    """
    Perform search according to params
    """
    # pass a list or a string?
    query = searchParams['query']
    method = searchParams['method']
    begin_time = time.time()
    # what the result structure is?
    result_list = search_method[method](query)
    end_time = time.time()
    # how to generate abstract?
    abstract = []
    return {
        'result': result_list,
        'time': end_time-begin_time,
        'abstract': abstract
    }


def getPage(docId):
    if docId not in meta_data:
        return None
    file_path = meta_data[docId]
    doc = read_file(file_path)
    return doc

