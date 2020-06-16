from wikisearch.indexer.build_index_util import load_meta
from wikisearch.searcher.search import searcher
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
load_searcher = True
if load_searcher:
    my_searcher = searcher("../data/index/inv","../data/index/docvec","../resources/stopwords/cn_stopwords.txt",
    in_memory=True,proc_num=8)


def getPage(docId):
    if docId not in meta_data:
        return None
    file_path = meta_data[docId]
    doc = read_file(file_path)
    return doc


def generate_abstract(docId):
    doc = getPage(docId)
    return {
        'title': doc['title'],
        'abstract': doc['text'][len(doc['title']):50],
        'url':doc['url'],
        'id':doc['id']
    }


def search(searchParams):
    """
    Perform search according to params
    """
    # pass a list or a string?
    query = searchParams['query']
    print(query)
    # method = searchParams['method']
    begin_time = time.time()
    # what the result structure is?
    # result_list = search_method[method](query)
    result_list = my_searcher.search(query)
    print(result_list)
    # result_list = []
    end_time = time.time()
    # how to generate abstract?
    res = [generate_abstract(doc) for doc in result_list]
    return {
        'result': res,
        'time': end_time-begin_time
    }


if __name__=="__main__":
    print(my_searcher.search("北京"))
    # print(meta_data)