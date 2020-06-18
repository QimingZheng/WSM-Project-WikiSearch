import unittest
unittest.TestLoader.sortTestMethodsUsing = None

import logging
import time
import multiprocessing as mp

import sys
import os
logging.basicConfig(level=logging.INFO)

import wikisearch

from wikisearch.query.query_suggestion import *


class IndexBuilderTestCase(unittest.TestCase):
    def test_2_query_suggestion(self):
        qs = QuerySuggestion(10)
        qs.load("../data/index/query_suggestion.pkl")
        partial_query = ["日料里的三文", "最近在北京市", "2019年出现的新型冠状", "我们观察了海洋", "夏天会台风", "冬天会大雪"]
        start = time.time()
        for par_q in partial_query:
            logging.info(qs.suggest(par_q))
        elapsed = time.time() - start
        logging.info("Qeury Completion Time Cost: " + str(elapsed) + " sec")
        return

    def test_1_dump_query_suggester(self):
        return
        _qs = QuerySuggestion(10)
        _qs.build("../data/index/meta.json", "../data/index/inv")
        _qs.dump("../data/index/query_suggestion.pkl")

if __name__ == "__main__":
    unittest.main()
