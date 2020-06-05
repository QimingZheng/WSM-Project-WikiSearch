from wikisearch.indexer.build_index_util import load_meta
from wikisearch.searcher import boolean_searcher, cosine_searcher, proximity_searcher, searcher_util, tfidf_searcher
import os
import json
import time
import codecs

def read_file(path):
    with codecs.open(path, 'r', 'utf8') as f:
        return json.loads(f.read())


docs_path = "../data/parsed/docs"
meta_data = read_file(os.path.join(docs_path, "meta.json"))

search_method = {}


def getPage(docId):
    if docId not in meta_data:
        return None
    file_path = meta_data[docId]
    doc = read_file(file_path)
    return doc


def generate_abstract(docId):
    doc = getPage(docId)
    return doc['title'], doc['text'][0:50]


def search(searchParams):
    """
    Perform search according to params
    """
    # pass a list or a string?
    query = searchParams['query']
    # method = searchParams['method']
    begin_time = time.time()
    # what the result structure is?
    # result_list = search_method[method](query)
    result_list = ['109209', '120811', '109209', '120811',
                   '13238', '143064', '15192', '17359', '26268']
    end_time = time.time()
    # how to generate abstract?
    res = [generate_abstract(doc) for doc in result_list]
    return {
        'result': res,
        'time': end_time-begin_time
    }
