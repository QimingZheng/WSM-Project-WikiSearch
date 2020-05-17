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
    def test_parallel_inverted_index(self):
        return
        wikis = traversal("../data/parsed/text/")
        parallelBuildInvertedIndex(wikis, "../data/index/inv")

    def test_Indexer(self):
        return
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
        wikis = traversal("../data/parsed/text/")
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
        wikis = traversal("../data/parsed/text/")
        parallelBuildDocVecIndex(wikis, "../data/index/docvec/")
        LoadDocVecIndex("../data/index/docvec/docvec_index.0.json")

    def test_positional_index(self):
        return
        articles = parseWikiJsons("../data/parsed/text/AA/wiki_00")
        BuildPositionalIndex(articles, "../data/index/positional_index.json")

    def test_parallel_positional_index(self):
        return
        wikis = traversal("../data/parsed/text/")
        parallelBuildPositionalIndex(wikis, "../data/index/pos/")


if __name__ == "__main__":
    unittest.main()
