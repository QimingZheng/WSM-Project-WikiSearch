"""
The implementation of three kinds of scores.
"""
import math


################################ Helper Function #################################
def normalize(vec):
    """ Normalize a vector and return its normalized dict.

        vec: term-value dict {}
    """
    eucd_len = math.sqrt(sum(map(lambda x: x**2, vec.values())))
    for term in vec:
        vec[term] /= eucd_len
    return vec


def cosine(v1, v2):
    """ Return the cosine similarity of two vectors.

        v1: term-value dict {}
        v2: term-value dict {}
    """
    intersection = set(v1.keys()) & set(v2.keys())

    similarity = 0
    for term in intersection:
        similarity += v1[term] * v2[term]
    return similarity


def jaccard(query, doc):
    """ Return the jaccard score between query and doc.

        query: term set
        doc: term set
    """
    return len(query & doc) / math.sqrt(len(query | doc))


def similarity(query, doc):
    """ Return the similarity between query and doc in vector space.

        query: term-freq dict {}
        doc: term-freq dict {}
    """

    # Normalization
    query = normalize(query)
    doc = normalize(doc)

    return cosine(query, doc)


def get_scores(query, val_docs, score_handler):
    scores = {}
    for docID in val_docs:
        scores[docID] = score_handler(query, val_docs[docID])
    return scores


# Score function record
SCORE = {"jaccard": jaccard, "bow": similarity, "tf-idf": similarity}
