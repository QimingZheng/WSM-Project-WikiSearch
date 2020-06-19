from wikisearch.indexer.build_index_util import load_meta
from wikisearch.searcher.search import searcher
import os
import json
import time
import codecs
from wikisearch.query.query_suggestion import QuerySuggestion


def read_file(path):
    with codecs.open(path, 'r', 'utf8') as f:
        return json.loads(f.read())


docs_path = "../data/parsed/docs"
meta_data = read_file(os.path.join(docs_path, "meta.json"))

search_method = {}
load_searcher = True
if load_searcher:
    my_searcher = searcher("../data/index/inv", "../data/index/docvec","../data/index/meta.json", "../resources/stopwords/cn_stopwords.txt",
                           in_memory=True, proc_num=8, cluster_load=1, tf_idf=1)

load_query = True
if load_query:
    sugguestions = QuerySuggestion(5)
    sugguestions.load("../data/index/query_suggestion.pkl")

def getPage(docId):
    if docId not in meta_data:
        return None
    file_path = meta_data[docId]
    doc = read_file(file_path)
    return doc

def get_suggestion(query):
    res = sugguestions.suggest(query)
    res = [{'value': item} for item in res]
    return res


def generate_abstract(docId, words):
    doc = getPage(docId)
    text = doc['text'][len(doc['title']):]
    begin = 0
    abstract_len = 50
    max_point = 0
    for i in range(len(text)):
        point = 0
        for word in words:
            if word in text[i:i+abstract_len]:
                point += 1
                
        if max_point < point:
            max_point = point
            begin = i
    abstract = text[begin:begin+abstract_len]
    match_word = [word for word in words if word in abstract]
    return {
        'title': doc['title'],
        'abstract': abstract,
        'words':match_word,
        'url': doc['url'],
        'id': doc['id']
    }


def reorder(res):
    pass

def search(searchParams):
    """
    Perform search according to params
    """
    # pass a list or a string?
    query = searchParams['query']
    print(query)
    print(searchParams['method'])
    method = searchParams['method'].split(',')
    score = method[0]
    filter_type = method[1]

    begin_time = time.time()
    # result_list, words = (['1044464', '1545352', '1890891', '2986961', '3449645',
    #                 '424030', '492002', '6099798', '813550', '885066'], ['北京'])
    result_list, words = my_searcher.search(
        query, score=score, filter_type=filter_type)
    print(result_list)
    # result_list = []
    end_time = time.time()
    res = [generate_abstract(doc, words) for doc in result_list if doc in meta_data]

    return {
        'result': res,
        'time': end_time-begin_time
    }


if __name__ == "__main__":
    # print(my_searcher.search("北京",score="tf-idf",filter_type="cluster"))
    print(meta_data)
    # docs, words = (['1044464', '1545352', '1890891', '2986961', '3449645',
    #                 '424030', '492002', '6099798', '813550', '885066'], ['北京'])
    # for doc in docs:
    #     print(generate_abstract(doc,words))
    # begin  = time.time()
    # print(sugguestions.suggest("日料里的三文"))
    # end = time.time()
    # print("use %fs"%(end-begin))
