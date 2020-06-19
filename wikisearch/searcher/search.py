from wikisearch.searcher.searcher_util import *
from wikisearch.searcher.score import jaccard, similarity, add_title_scores, naive_jaccard
from wikisearch.indexer.inverted_index import InvertedIndexer
from wikisearch.indexer.docvec_index import DocVecIndexer
from wikisearch.indexer.build_index_util import load_meta
from wikisearch.util import Traditional2Simplified
from wikisearch.util import text_segmentation
from wikisearch.searcher.filter import get_all_docs, get_high_idf_docs, get_docs_with_multi_terms, cluster, get_docs_with_cluster, heap
import time
import logging
from tqdm import tqdm
import os

class searcher(SearchEngineBase):
    """ Searcher class.

        Three kinds of scores: jaccard, bow, tf-idf
        Four kinds of filter algorithms: heap, high-idf, multi-terms, cluster
        More infomation is located at /doc directory.
    """

    def __init__(self,
                 inverted_index_file,
                 docvec_index_file,
                 meta_data_file,
                 stopwords_file,
                 in_memory=False,
                 proc_num=1,
                 idf_threshold=0.5,
                 terms=3,
                 seed=-1,
                 cluster_load=-1,
                 tf_idf=-1):
        # Load term inverted index and doc vector index
        start = time.time()
        self.invertedIndex = InvertedIndexer(inverted_index_file,
                                             in_memory=in_memory,
                                             thread_num=proc_num)
        self.DocVecIndex = DocVecIndexer(docvec_index_file,
                                         in_memory=in_memory)
        
        self.metaData = load_meta(meta_data_file)

        elapsed = time.time() - start
        logging.info("Contruct index in %f secs" % elapsed)

        start = time.time()

        self.idf = get_idf(self.invertedIndex)
        self.N = len(self.DocVecIndex)
        self.idf_threshold = int(idf_threshold * self.N)
        self.terms = terms

        self.seed = seed
        self.stopwords = load_stopwords(stopwords_file)
        tf_idf_file = os.path.join("/".join(inverted_index_file.split("/")[:-1]), "tf_idf")
        if tf_idf == 0:
            logging.info("retrieve tf-idf vactor...")
            self.tf_idf_DocVecIndex = {}
            for doc in tqdm(self.DocVecIndex.keys()):
                self.tf_idf_DocVecIndex[doc] = {}
                for term in self.DocVecIndex[doc]:
                    tf = self.DocVecIndex[doc][term]
                    idf = self.idf[term]
                    self.tf_idf_DocVecIndex[doc][term] = get_tf_idf_score(
                        tf, idf, self.N)
            
            if not os.path.exists(tf_idf_file):
                os.makedirs(tf_idf_file)


            with open(os.path.join(tf_idf_file, "tf_idf.json"), "w") as f:
                json.dump(self.tf_idf_DocVecIndex, f)
            logging.info("vector space projection has been finished!")
        
        elif tf_idf == 1:
            with open(os.path.join(tf_idf_file, "tf_idf.json"), "r") as f:
                self.tf_idf_DocVecIndex = json.load(f)

        cluster_info_file = os.path.join("/".join(inverted_index_file.split("/")[:-1]), "cluster")
        if cluster_load == 0:
            logging.info("clustering...")
            self.leaders, self.docs = {}, {}
            for score in ["jaccard", "bow", "tf-idf"]:
                if score != "tf-idf":
                    self.leaders[score], self.docs[score] = cluster(self.DocVecIndex, seed,
                                                score, cluster_info_file)
                else:
                    self.leaders[score], self.docs[score] = cluster(self.tf_idf_DocVecIndex, seed,
                                                score, cluster_info_file)

            logging.info("clustering has been finished!")
        elif cluster_load == 1:
            logging.info("clustering...")
            self.leaders, self.docs = {}, {}
            for score in ["jaccard", "bow", "tf-idf"]:
                new_cluster_file = os.path.join(cluster_info_file, score)
                self.leaders[score], self.docs[score] = load_cluster_info(new_cluster_file)
            logging.info("clustering has been finished!")
        
        else:
            logging.info("no clustering...")


    def search(self, query, top_k=10, score="jaccard", filter_type="heap"):
        query = Traditional2Simplified(query)
        query = list(text_segmentation(query))

        query = process_query(query, self.stopwords)

        if score == "bow":
            query_vec = get_bow(query)
        elif score == "tf-idf":
            query_vec = get_tf_idf(query, self.idf, self.N)
        elif filter_type == "cluster":
            query_vec = get_bow(query)

        if filter_type == "heap":
            val_docs = get_all_docs(self.invertedIndex)
        elif filter_type == "high-idf":
            val_docs = get_high_idf_docs(query, self.idf, self.invertedIndex,
                                         self.idf_threshold)
        elif filter_type == "multi-terms":
            val_docs = get_docs_with_multi_terms(query, self.invertedIndex,
                                                 self.terms)
        elif filter_type == "cluster":
            val_docs = get_docs_with_cluster(query_vec, self.leaders[score],
                                             self.docs[score], score)
        
        # Get title scores        
        title_scores = {}
        for doc in val_docs:
            title = Traditional2Simplified(self.metaData[doc]["title"])
            title = list(text_segmentation(title))
            title = process_query(title, self.stopwords)
            
            title_scores[doc] = naive_jaccard(set(query), set(title))

        scores = {}
        if score == "jaccard":
            for docID in val_docs:
                scores[docID] = jaccard(query, set(self.DocVecIndex[docID].keys()))

        elif score == "tf-idf":
            for docID in val_docs:
                scores[docID] = similarity(query_vec, self.tf_idf_DocVecIndex[docID])
        else:
            for docID in val_docs:
                scores[docID] = similarity(query_vec, self.DocVecIndex[docID])
        
        add_title_scores(scores, title_scores, score)

        return (heap(scores, top_k), query)
