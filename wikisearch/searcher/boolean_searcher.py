from wikisearch.searcher.searcher_util import *
import time
"""
parallel search
"""


def partial_search(inds, query):
    res = []
    for q_term in query:
        if q_term in inds:
            for key, val in inds[q_term].items():
                res += [(key, val)]
    res = list(set(res))
    for q_term in query:
        if q_term in inds:
            temp = []
            for key, val in inds[q_term].items():
                temp += [(key, val)]
            res = list(set(res).intersection(set(temp)))
    return res


class NaiveBooleanSearch(SearchEngineBase):
    """
    requirements:
    1. support concurrent search query (inter-query)
    2. support intra-query parallelization
    """
    def __init__(self, indexFolder, meta_file, proc_num=1):
        self.proc_num = proc_num
        start = time.time()
        self.invertedIndex = InvertedIndexer(indexFolder,
                                             in_memory=False,
                                             thread_num=self.proc_num)
        self.article_mata = load_meta(meta_file)
        elapsed = time.time() - start
        logging.info("Build NaiveBooleanSearch Engine in %f secs" % elapsed)
        return

    def search(self, query, dump):
        query = Traditional2Simplified(query)
        query = list(text_segmentation(query))
        result = []

        for q_term in query:
            if self.invertedIndex.has_key(q_term):
                for key, val in self.invertedIndex[q_term].items():
                    result += [(key, val)]
        result = list(set(result))
        for q_term in query:
            if self.invertedIndex.has_key(q_term):
                temp = []
                for key, val in self.invertedIndex[q_term].items():
                    temp += [(key, val)]
                result = list(set(result).intersection(set(temp)))

        result.sort(key = lambda x: x[1], reverse=True)
        
        if dump:
            print(result)
        for i in range(len(result)):
            uid = result[i][0]
            result[i] = {
                "url": self.article_mata[uid]["url"],
                "title": self.article_mata[uid]["title"]
            }
        return result
