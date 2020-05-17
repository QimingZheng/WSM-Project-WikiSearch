import unittest
unittest.TestLoader.sortTestMethodsUsing = None
import wikisearch
from wikisearch.indexer.build_index_util import *
from wikisearch.indexer.docvec_index import *
from wikisearch.indexer.inverted_index import *
from wikisearch.indexer.positional_index import *
import logging
import os
logging.basicConfig(level=logging.INFO)
import time


def traversal(rootDir):
    re = []
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if os.path.isdir(path):
            re += traversal(path)
        else:
            re.append(path)
    return re


class IndexBuilderTestCase(unittest.TestCase):
    def test_Indexer(self):
        # Do some benchmarks here
        keyword_list = ["上海", "广州", "纽约", "科学", "技术", "艺术", "仲夏夜"]

        # inverted index
        start = time.time()
        inv_ind = InvertedIndexer("../data/index/inv", True)
        elapsed = time.time() - start
        logging.info("InvertedIndexer load time: " + str(elapsed))

        start = time.time()
        for kw in keyword_list:
            inv_ind[kw]
        elapsed = time.time() - start
        logging.info("InvertedIndexer retrieval time: " + str(elapsed))

        docid_list = ["3045934", "3046815", "4849654", "6529222"]
        # docvec index
        start = time.time()
        docvec_ind = DocVecIndexer("../data/index/docvec", True)
        elapsed = time.time() - start
        logging.info("DocVecIndexer load time: " + str(elapsed))

        start = time.time()
        for doc in docid_list:
            docvec_ind[doc]
        elapsed = time.time() - start
        logging.info("DocVecIndexer retrieval time: " + str(elapsed))

        # positional index
        start = time.time()
        pos_ind = PositionalIndexer("../data/index/pos", True)
        elapsed = time.time() - start
        logging.info("PositionalIndexer load time: " + str(elapsed))

        start = time.time()
        for kw in keyword_list:
            pos_ind[kw]
        elapsed = time.time() - start
        logging.info("PositionalIndexer retrieval time: " + str(elapsed))

    def test_parallel_dump_meta(self):
        return
        wikis = traversal("../data/parsed/text/")
        parallel_dump_meta(wikis, "../data/index/meta.json")
        load_meta("../data/index/meta.json")

    def test_parallel_inverted_index(self):
        return
        wikis = traversal("../data/parsed/text/")
        parallelBuildInvertedIndex(wikis, "../data/index/inv")

    def test_parallel_docvec_index(self):
        return
        wikis = traversal("../data/parsed/text/")
        parallelBuildDocVecIndex(wikis, "../data/index/docvec/")
        LoadDocVecIndex("../data/index/docvec/docvec_index.0.json")

    def test_parallel_positional_index(self):
        return
        wikis = traversal("../data/parsed/text/")
        parallelBuildPositionalIndex(wikis, "../data/index/pos/")


if __name__ == "__main__":
    unittest.main()
