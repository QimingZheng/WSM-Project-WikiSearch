from wikisearch.searcher.searcher_util import *
import time
"""
parallel search
"""


def partial_search(inv_ind, query):
    res = []
    for q_term in query:
        if q_term in inv_ind:
            for key, _ in inv_ind[q_term].items():
                res += [key]
    res = list(set(res))
    for q_term in query:
        if q_term in inv_ind:
            temp = []
            for key, _ in inv_ind[q_term].items():
                temp += [key]
            res = list(set(res).intersection(set(temp)))
    return res


class NaiveBooleanSearch(SearchEngineBase):
    """
    requirements:
    1. support concurrent search query (inter-query)
    2. support intra-query parallelization
    """
    def __init__(self, inverted_index_files, meta_file, proc_num):
        self.proc_num = proc_num
        if not isinstance(inverted_index_files, list):
            inverted_index_files = [inverted_index_files]
        assert (
            self.proc_num == len(inverted_index_files)
        ), "allocated process number and inverted-index files should be equal"
        start = time.time()
        self.invertedIndex = LoadMultiInvertedIndex(inverted_index_files,
                                                    proc_num)
        self.article_mata = load_meta(meta_file)
        elapsed = time.time() - start
        logging.info("Build NaiveBooleanSearch Engine in %f secs" % elapsed)
        return

    def search(self, query, dump):
        query = Traditional2Simplified(query)
        query = list(text_segmentation(query))
        result = []  #self.invertedIndex[query[0]]
        """
        serial search
        """
        # for q_term in query:
        #     if q_term in self.invertedIndex:
        #         for key, _ in self.invertedIndex[q_term].items():
        #             result += [key]
        # result = list(set(result))
        # for q_term in query:
        #     if q_term in self.invertedIndex:
        #         temp = []
        #         for key, _ in self.invertedIndex[q_term].items():
        #             temp += [key]
        #         result = list(set(result).intersection(set(temp)))

        pool = mp.Pool(self.proc_num)
        results = pool.starmap(partial_search, [(self.invertedIndex[i], query)
                                                for i in range(self.proc_num)])

        for res in results:
            result += res
        for res in results:
            result = list(set(res).intersection(set(result)))

        if dump:
            print(result)
        for i in range(len(result)):
            uid = result[i]
            result[i] = {
                "url": self.article_mata[uid]["url"],
                "title": self.article_mata[uid]["title"]
            }
        return result
