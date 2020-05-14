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


class IndexBuilderTestCase(unittest.TestCase):
    def test_parallel_meta_build(self):
        all = os.walk("../data/parsed/zh/json/AA/")
        wikis = []
        for path, dir_list, file_list in all:
            for file_name in file_list:
                wikis.append(os.path.join(path, file_name))
        parallel_dump_meta(wikis, "../data/index/meta.json")
        load_meta("../data/index/meta.json")

    def test_parallel_inverted_index(self):
        article_list = []
        all = os.walk("../data/parsed/zh/json/AA/")
        wikis = []
        for path, dir_list, file_list in all:
            for file_name in file_list:
                wikis.append(os.path.join(path, file_name))
        parallelBuildInvertedIndex(wikis, "../data/index/inverted_index.json")
        LoadInvertedIndex("../data/index/inverted_index.json")

    def test_meta_build(self):
        dump_meta("../data/parsed/zh/json/AA/wiki_00",
                  "../data/index/meta.json")
        ret = load_meta("../data/index/meta.json")

    def test_inverted_index(self):
        articles = parseWikiJsons("../data/parsed/zh/json/AA/wiki_00")
        BuildInvertedIndex(articles, "../data/index/inverted_index.json")
        LoadInvertedIndex("../data/index/inverted_index.json")

    def test_docvec_index(self):
        articles = parseWikiJsons("../data/parsed/zh/json/AA/wiki_00")
        BuildDocVecIndex(articles, "../data/index/docvec_index.json")
        LoadDocVecIndex("../data/index/docvec_index.json")

    def test_positional_index(self):
        articles = parseWikiJsons("../data/parsed/zh/json/AA/wiki_00")
        BuildPositionalIndex(articles, "../data/index/positional_index.json")

    def test_parallel_docvec_index(self):
        article_list = []
        all = os.walk("../data/parsed/zh/json/AA/")
        wikis = []
        for path, dir_list, file_list in all:
            for file_name in file_list:
                wikis.append(os.path.join(path, file_name))
        parallelBuildDocVecIndex(wikis, "../data/index/docvec_index.json")
        LoadDocVecIndex("../data/index/docvec_index.json")


if __name__ == "__main__":
    unittest.main()
