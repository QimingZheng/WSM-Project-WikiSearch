"""
The implementation of four kinds of filter algorithms.
"""
import random
from heapq import heappop, heappush, heapify
from collections import defaultdict
import math
from wikisearch.searcher.score import SCORE


def get_all_docs(invertedIndex):
    valid_docs = set()
    for term in invertedIndex:
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
        if term in invertedIndex:
            for doc in invertedIndex[term]:
                record[doc] += 1

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


def cluster(docVecIndex, seed, score):
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

    print(leaders_index)
    leaders = []
    record = sorted(docVecIndex.items(), key=lambda x: x[0])

    for index in leaders_index:
        item = record[index]
        leaders.append(item[1])

    neighbours = [[] for i in range(len(leaders))]

    for item in record:
        docID, doc_vec = item
        nearest = get_nearest_leader(doc_vec, leaders, score)
        neighbours[nearest].append(docID)
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
