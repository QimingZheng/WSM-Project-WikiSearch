"""
The implementation of four kinds of filter algorithms.
"""
import random
from heapq import heappop, heappush, heapify
from collections import defaultdict
import math
from wikisearch.searcher.score import SCORE
import logging
from tqdm import tqdm
import os
import json


def get_all_docs(invertedIndex):
    valid_docs = set()
    for term in invertedIndex.keys():
        valid_docs |= set(invertedIndex[term].keys())
    return valid_docs


def get_high_idf_docs(query, idf, invertedIndex, idf_threshold):
    valid_docs = set()
    for term in query:
        if term in idf:
            term_idf = idf[term]
            if term_idf < idf_threshold:
                valid_docs |= set(invertedIndex[term].keys())
    return valid_docs


def get_docs_with_multi_terms(query, invertedIndex, terms):
    docs = []
    record = defaultdict(int)

    for term in query:
        if term in invertedIndex.keys():
            for doc in invertedIndex[term]:
                record[doc] += 1

    terms = min(terms, len(query))
    for doc in record:
        if record[doc] >= terms:
            docs.append(doc)
    return docs


def get_docs_with_cluster(query, leaders, neighbours, score):
    nearest = get_nearest_leader(query, leaders, score)
    return neighbours[nearest]


def heap(scores, top_k):
    """ Return the top_k doc ID according to scores using heap.

        scores: docID-score dict {}
        top_k: int
    """
    heap = []
    heapify(heap)

    for doc in scores:
        heappush(heap, (-scores[doc], doc))

    top_k_docs = []
    num = min(len(heap), top_k)
    for i in range(num):
        top_k_docs.append(heappop(heap)[1])
    return top_k_docs


def get_nearest_leader(doc_vec, leaders, score):
    maxm_similarity, nearest = -1, -1
    for index, leader in enumerate(leaders):
        if score == "jaccard":
            cur_similarity = SCORE[score](set(doc_vec.keys()),
                                          set(leader.keys()))
        else:
            cur_similarity = SCORE[score](doc_vec, leader)

        if cur_similarity > maxm_similarity:
            maxm_similarity = cur_similarity
            nearest = index
    return nearest


def cluster(docVecIndex, seed, score, cluster_info_file):
    if seed >= 0:
        random.seed(seed)

    N = len(docVecIndex)
    lead_num = int(math.sqrt(N))

    
    leaders_index = []
    for i in range(lead_num):
        next_index = random.randint(0, N - 1)
        while next_index in leaders_index:
            next_index = random.randint(0, N - 1)
        leaders_index.append(next_index)
    
    logging.info("leaders have been generated randomly.")

    # print(leaders_index)
    leaders = []
    record = sorted(docVecIndex.keys())

    for index in leaders_index:
        doc = record[index]
        leaders.append(docVecIndex[doc])
    
    logging.info("start clustering.")

    neighbours = [[] for i in range(len(leaders))]

    for doc in tqdm(record):
        docID, doc_vec = doc, docVecIndex[doc]
        nearest = get_nearest_leader(doc_vec, leaders, score)
        neighbours[nearest].append(docID)
    
    if not os.path.exists(cluster_info_file):
        os.makedirs(cluster_info_file)
    
    cluster_info_dir = os.path.join(cluster_info_file, score)
    if not os.path.exists(cluster_info_dir):
        os.makedirs(cluster_info_dir)
    

    with open(os.path.join(cluster_info_dir, "leaders.json"), "w") as f:
        json.dump(leaders, f)
    
    with open(os.path.join(cluster_info_dir, "neighbours.json"), "w") as f:
        json.dump(neighbours, f)

    return leaders, neighbours


# def high_idf(idf, invertedIndex, scores, top_k, idf_threshold):
#     """ Return the top_k doc ID according to scores. Only consider high idf
#     terms.

#         idf: term-idf dict {}
#         invertedIndex: constructed inverted index
#         scores: docID-score dict {}
#         top_k: int
#         top_idf: int
#     """
#     high_idf_terms = []
#     for term in idf:
#         if idf[term] >= idf_threshold:
#             high_idf_terms.append(term)

#     valid_docs = set()
#     for term in high_idf_terms:
#         valid_docs |= set(invertedIndex[term].keys())

#     valid_scores = {docID: scores[docID] for docID in valid_docs}
#     return heap(valid_scores, top_k)

# def multi_terms(invertedIndex, terms, scores, top_k):
#     """ Return the top_k doc ID according to scores. Only consider docs with multiple query
#     terms.

#         invertedIndex: constructed inverted index
#         scores: docID-score dict {}
#         top_k: int
#         terms: int
#     """
#     valid_docs = get_docs_with_multi_terms(invertedIndex, terms)
#     valid_scores = {docID: scores[docID] for docID in valid_docs}
#     return heap(valid_scores, top_k)
