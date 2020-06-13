from wikisearch.searcher.searcher_util import *
from wikisearch.searcher.score import SCORE, get_scores
from wikisearch.indexer.inverted_index import InvertedIndexer
from wikisearch.indexer.docvec_index import DocVecIndexer
from wikisearch.util import Traditional2Simplified
from wikisearch.util import text_segmentation
from wikisearch.searcher.filter import get_all_docs, get_high_idf_docs, get_docs_with_multi_terms, cluster, get_docs_with_cluster, heap
import time
import logging


class searcher(SearchEngineBase):
    """ Searcher class.

        Three kinds of scores: jaccard, bow, tf-idf
        Four kinds of filter algorithms: heap, high-idf, multi-terms, cluster
        More infomation is located at /doc directory.
    """

    def __init__(self,
                 inverted_index_file,
                 docvec_index_file,
                 score="jaccard",
                 filter_type="heap",
                 in_memory=False,
                 proc_num=1,
                 idf_threshold=50,
                 terms=3,
                 seed=-1):
        # Load term inverted index and doc vector index
        start = time.time()
        self.invertedIndex = InvertedIndexer(inverted_index_file,
                                             in_memory=in_memory,
                                             thread_num=proc_num)
        self.DocVecIndex = DocVecIndexer(docvec_index_file,
                                         in_memory=in_memory)

        elapsed = time.time() - start
        logging.info("Contruct index in %f secs" % elapsed)

        start = time.time()

        # Score and filter function selection
        self.score_handler = SCORE[score]
        self.score = score
        self.filter = filter_type

        if filter_type == 'high-idf' or score == "tf-idf":
            self.idf = get_idf(self.invertedIndex)
            self.idf_threshold = idf_threshold
            self.N = len(self.DocVecIndex)

        elif filter_type == "multi-terms":
            self.terms = terms
        elif filter_type == "cluster":
            self.seed = seed
            if score == "tf-idf":
                for doc in self.DocVecIndex:
                    for term in self.DocVecIndex[doc]:
                        tf = self.DocVecIndex[doc][term]
                        idf = self.idf[term]
                        self.DocVecIndex[doc][term] = get_tf_idf_score(
                            tf, idf, self.N)
            self.leaders, self.docs = cluster(self.DocVecIndex, seed,
                                              self.score)

    def search(self, query, top_k=10):
        query = Traditional2Simplified(query)
        query = list(text_segmentation(query))

        if self.score == "bow":
            query_vec = get_bow(query)
        elif self.score == "tf-idf":
            query_vec = get_tf_idf(query)
        elif self.filter == "cluster":
            query_vec = get_bow(query)

        if self.filter == "heap":
            val_docs = get_all_docs(self.invertedIndex)
        elif self.filter == "high-idf":
            val_docs = get_high_idf_docs(query, self.idf, self.invertedIndex,
                                         self.idf_threshold)
        elif self.filter == "multi-terms":
            val_docs = get_docs_with_multi_terms(query, self.invertedIndex,
                                                 self.terms)
        elif self.filter == "cluster":
            val_docs = get_docs_with_cluster(query_vec, self.leaders,
                                             self.docs, self.score)

        if self.score == "jaccard":
            val_doc_reps = {
                docID: set(self.DocVecIndex[docID].keys())
                for docID in val_docs
            }
            scores = get_scores(query, val_doc_reps, self.score_handler)
        else:
            val_doc_reps = {
                docID: self.DocVecIndex[docID]
                for docID in val_docs
            }
            scores = get_scores(query_vec, val_doc_reps, self.score_handler)

        return heap(scores, top_k)
