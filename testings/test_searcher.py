import sys
sys.path.append("../wikisearch")
import unittest
import wikisearch
from wikisearch.searcher.searcher_util import *
from wikisearch.searcher.filter import *
from wikisearch.searcher.score import *
from wikisearch.searcher.search import searcher
import logging

logging.basicConfig(level=logging.INFO)

import time


class SearcherTestCase(unittest.TestCase):
    
    #### test score
    def test_jaccard(self):
        query = ['广州市', '上海市', '福州市', '开源软件']
        doc = ['广州市', '上海', '福州市', '你好']
        assert (jaccard(set(query), set(doc)) == 2 / math.sqrt(6))

    def test_similarity(self):
        query = {'广州市': 1, '上海市': 1, '福州市': 1, '开源软件': 1}
        doc = {'广州市': 2, '上海': 2, '福州市': 2, '你好': 2}
        assert (similarity(query, doc) == 0.5)

    def test_get_scores(self):
        query = {'广州市': 1, '上海市': 1, '福州市': 1, '开源软件': 1}
        docs = {
            '1': {
                '广州市': 2,
                '上海': 2,
                '福州市': 2,
                '你好': 2
            },
            '2': {
                '广州市': 2,
                '上海': 2,
                '福州市': 3,
                '你好': 2
            }
        }
        assert (get_scores(query, docs, similarity) == {
            '1': 0.5,
            '2': 2.5 / math.sqrt(21)
        })

    #### test filter
    def test_get_all_docs(self):
        invertedIndex = {
            '上海': {
                '1': 2,
                '2': 3
            },
            "背景": {
                '1': 3
            },
            "daf": {
                '4': 3
            }
        }
        assert (sorted(get_all_docs(invertedIndex)) == ['1', '2', '4'])

    def test_get_high_idf_docs(self):
        query = ['上海', '背景', 'nothing']
        idf = {'上海': 3, '背景': 10}
        invertedIndex = {
            '上海': {
                '1': 2,
                '2': 3
            },
            "背景": {
                '1': 3
            },
            "daf": {
                '4': 3
            }
        }
        assert (sorted(get_high_idf_docs(query, idf, invertedIndex,
                                         5)) == ['1', '2'])

    def test_get_docs_with_multi_terms(self):
        query = ['上海', '背景', 'nothing', 'test1', 'test2']
        invertedIndex = {
            '上海': {
                '1': 2,
                '2': 3
            },
            "背景": {
                '1': 3,
                '4': 2
            },
            "daf": {
                '4': 3
            },
            'test1': {
                '1': 3,
                '2': 1,
                '4': 2
            },
            'test2': {
                '2': 12
            }
        }
        assert (sorted(get_docs_with_multi_terms(query, invertedIndex,
                                                 3)) == ['1', '2'])

    def test_cluster(self):
        docVecIndex = {
            '1': {
                'test1': 2,
                'test2': 3
            },
            '2': {
                'test2': 5,
                'test3': 2
            },
            '3': {
                'test1': 9,
                'test3': 16
            },
            '4': {
                'test1': 1,
                'test2': 2,
                'test3': 3
            }
        }
        seed = 0
        leaders, neighbours = cluster(docVecIndex, seed, 'jaccard')
        assert (leaders == [{
            'test1': 1,
            'test2': 2,
            'test3': 3
        }, {
            'test1': 2,
            'test2': 3
        }])
        assert (neighbours == [['2', '3', '4'], ['1']])

        leaders, neighbours = cluster(docVecIndex, seed, 'bow')

        l1 = math.sqrt(14)
        l2 = math.sqrt(13)

        assert (leaders == [{
            'test1': 1 / l1,
            'test2': 2 / l1,
            'test3': 3 / l1
        }, {
            'test1': 2 / l2,
            'test2': 3 / l2
        }])
        # print(leaders)
        assert (neighbours == [['2', '3', '4'], ['1']])

    #### test searcher
    def test_heap_jaccard(self):
        return
        mysearcher = searcher("../data/index/inv",
                              "../data/index/docvec",
                              in_memory=True)
        
        while True:
            query = input("query input: ")
            if query == "q":
                break
            print(mysearcher.search(query))
            break
    
    def test_heap_bow(self):
        return
        mysearcher = searcher("../data/index/inv",
                              "../data/index/docvec",
                              in_memory=True, score="bow")
        while True:
            query = input("query input: ")
            if query == "q":
                break
            print(mysearcher.search(query))
            break
    
    def test_heap_tf_idf(self):
        return
        mysearcher = searcher("../data/index/inv",
                              "../data/index/docvec",
                              in_memory=True, score="tf-idf")
        while True:
            query = input("query input: ")
            if query == "q":
                break
            print(mysearcher.search(query))
            break
    
    def test_high_idf_tf_idf(self):
        return
        mysearcher = searcher("../data/index/inv",
                              "../data/index/docvec",
                              in_memory=True, score="tf-idf", filter_type="high-idf")
        while True:
            query = input("query input: ")
            if query == "q":
                break
            print(mysearcher.search(query))
            break
    
    def test_multi_terms_tf_idf(self):
        return
        mysearcher = searcher("../data/index/inv",
                              "../data/index/docvec",
                              in_memory=True, score="tf-idf", filter_type="multi-terms")
        while True:
            query = input("query input: ")
            if query == "q":
                break
            print(mysearcher.search(query))
            break
    
    def test_cluster_terms_bow(self):
        mysearcher = searcher("../data/index/inv",
                              "../data/index/docvec",
                              in_memory=True, score="bow", filter_type="cluster")
        while True:
            query = input("query input: ")
            if query == "q":
                break
            print(mysearcher.search(query))
            

    # def test

    # def test_boolean_search(self):
    #     searcher = NaiveBooleanSearch("../data/index/inv", "../data/index/meta.json", in_memory=False, proc_num=32)
    #     start = time.time()
    #     for query in ["广州市", "上海市", "福州市", "教师是人类灵魂的工程师"]:
    #         result = searcher.search(query, dump=False)
    #         for res in result[:3]:
    #             logging.info(res["title"])
    #         logging.info("---------")
    #     elapsed = time.time() - start
    #     logging.info("search cost " + str(elapsed) +" secs")

    # def test_tfidf_search(self):
    #     return
    #     searcher = TFIDFSearch("../data/index/inverted_index.json",
    #                            "../data/index/meta.json")
    #     for query in ["广州", "上海", "福州", "开源软件与版权"]:
    #         result = searcher.search(query, dump=False)
    #         for res in result[:3]:
    #             logging.info(res["title"])
    #         logging.info("---------")

    # def test_cosine_search(self):
    #     return
    #     searcher = CosineSearch("../data/index/inverted_index.json",
    #                             "../data/index/docvec_index.json",
    #                             "../data/index/meta.json")
    #     for query in ["广州", "上海", "福州", "开源软件与版权"]:
    #         result = searcher.search(query, dump=False)
    #         for res in result[:3]:
    #             logging.info(res["title"])
    #         logging.info("---------")

    # def test_proximity_searcher(self):
    #     return
    #     searcher = ProximitySearch("../data/index/positional_index.json",
    #                                "../data/index/meta.json",
    #                                proc_num=1)
    #     for query in ["广州", "上海", "福州", "开源软件与版权"]:
    #         result = searcher.search(query)
    #         for res in result[:3]:
    #             logging.info(res["title"])
    #         logging.info("---------")


if __name__ == "__main__":
    unittest.main()
