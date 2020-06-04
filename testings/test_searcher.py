import unittest
import wikisearch
from wikisearch.searcher.searcher_util import *
from wikisearch.searcher.boolean_searcher import *
from wikisearch.searcher.cosine_searcher import *
from wikisearch.searcher.tfidf_searcher import *
from wikisearch.searcher.proximity_searcher import *
import logging

logging.basicConfig(level=logging.INFO)

import time

class SearcherTestCase(unittest.TestCase):
    def test_boolean_search(self):
        searcher = NaiveBooleanSearch("../data/index/inv", "../data/index/meta.json", in_memory=False, proc_num=32)
        start = time.time()
        for query in ["广州市", "上海市", "福州市", "教师是人类灵魂的工程师"]:
            result = searcher.search(query, dump=False)
            for res in result[:3]:
                logging.info(res["title"])
            logging.info("---------")
        elapsed = time.time() - start
        logging.info("search cost " + str(elapsed) +" secs")

    def test_tfidf_search(self):
        return 
        searcher = TFIDFSearch("../data/index/inverted_index.json",
                               "../data/index/meta.json")
        for query in ["广州", "上海", "福州", "开源软件与版权"]:
            result = searcher.search(query, dump=False)
            for res in result[:3]:
                logging.info(res["title"])
            logging.info("---------")

    def test_cosine_search(self):
        return
        searcher = CosineSearch("../data/index/inverted_index.json",
                                "../data/index/docvec_index.json",
                                "../data/index/meta.json")
        for query in ["广州", "上海", "福州", "开源软件与版权"]:
            result = searcher.search(query, dump=False)
            for res in result[:3]:
                logging.info(res["title"])
            logging.info("---------")

    def test_proximity_searcher(self):
        return
        searcher = ProximitySearch("../data/index/positional_index.json",
                                   "../data/index/meta.json",
                                   proc_num=1)
        for query in ["广州", "上海", "福州", "开源软件与版权"]:
            result = searcher.search(query)
            for res in result[:3]:
                logging.info(res["title"])
            logging.info("---------")


if __name__ == "__main__":
    unittest.main()
