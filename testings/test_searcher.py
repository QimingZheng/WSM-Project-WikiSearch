import unittest
import wikisearch
from wikisearch.searcher.searcher_util import *
from wikisearch.searcher.boolean_searcher import *
from wikisearch.searcher.cosine_searcher import *
from wikisearch.searcher.tfidf_searcher import *
from wikisearch.searcher.proximity_searcher import *
import logging

logging.basicConfig(level=logging.INFO)


class SearcherTestCase(unittest.TestCase):
    def test_boolean_search(self):
        searcher = NaiveBooleanSearch("../data/index/inverted_index.json",
                                      "../data/index/meta.json",
                                      proc_num=1)
        for query in ["谷歌", "中国", "数学", "计算机科学中的数学原理", "内核"]:
            result = searcher.search(query, dump=False)
            for res in result[:3]:
                logging.info(res["title"])

    def test_tfidf_search(self):
        searcher = TFIDFSearch("../data/index/inverted_index.json",
                               "../data/index/meta.json")
        for query in ["谷歌", "中国", "数学", "计算机科学中的数学原理", "内核"]:
            result = searcher.search(query, dump=False)
            for res in result[:3]:
                logging.info(res["title"])

    def test_cosine_search(self):
        searcher = CosineSearch("../data/index/inverted_index.json",
                                "../data/index/docvec_index.json",
                                "../data/index/meta.json")
        for query in ["谷歌", "中国", "数学", "计算机科学中的数学原理", "内核"]:
            result = searcher.search(query, dump=False)
            for res in result[:3]:
                logging.info(res["title"])

    def test_proximity_searcher(self):
        searcher = ProximitySearch("../data/index/positional_index.json",
                                   "../data/index/meta.json",
                                   proc_num=1)
        for query in ["谷歌", "中国", "数学", "计算机科学中的数学原理", "内核"]:
            result = searcher.search(query)
            for res in result[:3]:
                logging.info(res["title"])


if __name__ == "__main__":
    unittest.main()
