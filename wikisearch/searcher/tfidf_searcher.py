from wikisearch.searcher.searcher_util import *
import time


class TFIDFSearch(SearchEngineBase):
    def __init__(self, inverted_index_file, meta_file):
        start = time.time()
        self.invertedIndex = LoadInvertedIndex(inverted_index_file)
        self.article_mata = load_meta(meta_file)
        elapsed = time.time() - start
        logging.info("Build TFIDFSearch Engine in %f secs" % elapsed)
        return

    def search(self, query, dump):
        N = len(self.article_mata)
        query = Traditional2Simplified(query)
        query = list(text_segmentation(query))
        result = []  #self.invertedIndex[query[0]]
        for q_term in query:
            if q_term in self.invertedIndex:
                for key, _ in self.invertedIndex[q_term].items():
                    result += [key]
        result = list(set(result))
        for q_term in query:
            if q_term in self.invertedIndex:
                temp = []
                for key, _ in self.invertedIndex[q_term].items():
                    temp += [key]
                result = list(set(result).intersection(set(temp)))
        score = {}
        for doc_id in result:
            score[doc_id] = tf_idf_score(query, doc_id, self.invertedIndex, N)
        score = sorted(score.items(), key=lambda d: d[1], reverse=True)
        for i in range(len(score)):
            uid = score[i][0]
            result[i] = {
                "url": self.article_mata[uid]["url"],
                "title": self.article_mata[uid]["title"]
            }
        return result
