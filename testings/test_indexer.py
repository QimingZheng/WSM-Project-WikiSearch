import unittest
unittest.TestLoader.sortTestMethodsUsing = None
import wikisearch
from wikisearch.indexer.indexer_collection import *
from wikisearch.indexer.build_index_util import *
from wikisearch.indexer.docvec_index import *
from wikisearch.indexer.inverted_index import *
from wikisearch.indexer.positional_index import *
import logging
import os
logging.basicConfig(level=logging.INFO)


class IndexBuilderTestCase(unittest.TestCase):
    def test_parallel_meta_build(self):
        return
        # slow
        all = os.walk("../data/parsed/text/AA/")
        wikis = []
        for path, dir_list, file_list in all:
            for file_name in file_list:
                wikis.append(os.path.join(path, file_name))
        parallel_dump_meta(wikis, "../data/index/meta.json")
        load_meta("../data/index/meta.json")

    def test_parallel_inverted_index(self):
        return
        article_list = []
        all = os.walk("../data/parsed/text/AA/")
        wikis = []
        for path, dir_list, file_list in all:
            for file_name in file_list:
                wikis.append(os.path.join(path, file_name))
        parallelBuildInvertedIndex(wikis, "../data/index/inv")
        LoadInvertedIndex("../data/index/inv/inverted_index.0.json")

    def test_Indexer(self):
        inv_ind = InvertedIndexer("../data/index/inv")
        docvec_ind = DocVecIndexer("../data/index/docvec")
        pos_ind = PositionalIndexer("../data/index/pos")

        logging.info(inv_ind.has_key("广州"))
        logging.info(len(inv_ind["广州"]))
        logging.info(len(inv_ind.keys()))
        
        logging.info(docvec_ind.has_key("165"))
        logging.info(len(docvec_ind["165"]))
        logging.info(len(docvec_ind.keys()))
        
        logging.info(pos_ind.has_key("广州"))
        logging.info(len(pos_ind["广州"]))
        logging.info(len(pos_ind.keys()))

    def test_meta_build(self):
        return
        dump_meta("../data/parsed/text/AA/wiki_00",
                  "../data/index/meta.json")
        ret = load_meta("../data/index/meta.json")

    def test_parallel_dump_meta(self):
        return
        all = os.walk("../data/parsed/text/AA/")
        wikis = []
        for path, dir_list, file_list in all:
            for file_name in file_list:
                wikis.append(os.path.join(path, file_name))
        parallel_dump_meta(wikis, "../data/index/meta.json")
        load_meta("../data/index/meta.json")


    def test_inverted_index(self):
        return
        articles = parseWikiJsons("../data/parsed/text/AA/wiki_00")
        BuildInvertedIndex(articles, "../data/index/")
        LoadInvertedIndex("../data/index/inverted_index.json")

    def test_docvec_index(self):
        return
        articles = parseWikiJsons("../data/parsed/text/AA/wiki_00")
        BuildDocVecIndex(articles, "../data/index/docvec_index.json")
        LoadDocVecIndex("../data/index/docvec_index.json")


    def test_parallel_docvec_index(self):
        return
        all = os.walk("../data/parsed/text/AA/")
        wikis = []
        for path, dir_list, file_list in all:
            for file_name in file_list:
                wikis.append(os.path.join(path, file_name))
        parallelBuildDocVecIndex(wikis, "../data/index/docvec/")
        LoadDocVecIndex("../data/index/docvec/docvec_index.0.json")

    def test_positional_index(self):
        return
        articles = parseWikiJsons("../data/parsed/text/AA/wiki_00")
        BuildPositionalIndex(articles, "../data/index/positional_index.json")

    def test_parallel_positional_index(self):
        return
        all = os.walk("../data/parsed/text/AA/")
        wikis = []
        for path, dir_list, file_list in all:
            for file_name in file_list:
                wikis.append(os.path.join(path, file_name))
        parallelBuildPositionalIndex(wikis, "../data/index/pos/")
        LoadPositionalIndex("../data/index/pos/positional_index.0.json")


if __name__ == "__main__":
    unittest.main()
