from wikisearch.util import *
from wikisearch.indexer.inverted_index import *
from wikisearch.indexer.docvec_index import *
from wikisearch.indexer.positional_index import *
import logging
import collections
import math


def get_tf_idf_score(tf, idf, N):
    return (1 + math.log(tf, 10)) * math.log(N / idf, 10)


# def cosine_similarity(query, doc_term_freq, inverted_index, N):
#     epsilon = 1e-8
#     product = 0.0
#     query_norm = epsilon
#     doc_norm = epsilon
#     doc_tfidf = {}
#     query_tfidf = {}
#     for term in query:
#         if term in query_tfidf:
#             query_tfidf[term] += 1
#         else:
#             query_tfidf[term] = 1
#     for term, _ in query_tfidf.items():
#         if not term in inverted_index:
#             query_tfidf[term] = 0
#             continue
#         query_tfidf[term] = (1 + math.log(epsilon + query_tfidf[term]) /
#                              math.log(10)) * math.log(
#                                  N * 1.0 / len(inverted_index[term]))
#         query_norm += query_tfidf[term]**2
#     for term, _ in doc_term_freq.items():
#         if not term in inverted_index:
#             continue
#         doc_tfidf[term] = (1 + math.log(epsilon + doc_term_freq[term]) /
#                            math.log(10)) * math.log(
#                                N * 1.0 / len(inverted_index[term]))
#         doc_norm += doc_tfidf[term]**2
#     for term, _ in doc_tfidf.items():
#         if term in doc_tfidf and term in query_tfidf:
#             product += doc_tfidf[term] * query_tfidf[term]
#     return product / (query_norm * doc_norm)


def get_idf(invertedIndex):
    return {term: len(invertedIndex[term]) for term in invertedIndex.keys()}


def get_bow(term_list):
    bow = collections.defaultdict(int)
    for term in term_list:
        bow[term] += 1
    return bow


def get_tf_idf(term_list, idf, N):
    tf = get_bow(term_list)
    tf_idf = {}
    for term in set(term_list):
        if term in idf:
            tf_idf[term] = get_tf_idf_score(tf[term], idf[term], N)
    return tf_idf


class SearchEngineBase(object):
    """
    should support concurrent search requests,
    speed requirements.
    """

    def __init__(self):
        pass

    def search(self, query, dump):
        raise NotImplementedError

    def rank(self, results):
        raise NotImplementedError


# if __name__ == "__main__":
#     searcher = NaiveBooleanSearch("inverted_index.json", "meta.json")
#     searcher2 = TFIDFSearch("inverted_index.json", "meta.json")
#     searcher3 = CosineSearch("inverted_index.json", "docvec_index.json",
#                              "meta.json")
#     for query in ["中国", "数学", "计算机科学中的数学原理", "内核"]:
#         print("======Naive Search=======")
#         result = searcher.search(query, dump=False)
#         for res in result[:3]:
#             # print (res["url"], res["title"])
#             print(res["title"])

#         print("======TF IDF Search=======")

#         result = searcher2.search(query, dump=False)
#         for res in result[:3]:
#             # print (res["url"], res["title"])
#             print(res["title"])

#         print("======Cosine Search=======")

#         result = searcher3.search(query, dump=False)
#         for res in result[:3]:
#             # print (res["url"], res["title"])
#             print(res["title"])