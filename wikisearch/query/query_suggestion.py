from wikisearch.indexer.inverted_index import *
from wikisearch.indexer.build_index_util import *
import heapq as hq
import logging
import pickle


class node:
    def __init__(self):
        self.child = {}
        self.top_k = []


class Trie:
    def __init__(self, top_k):
        self.top_k = top_k
        self.root = node()
        return

    def add(self, sentence, weight):
        # char = sentence[0]
        cur = self.root
        for char in sentence:
            char = str(char)
            if char in cur.child:
                if len(cur.child[char].top_k) < self.top_k:
                    hq.heappush(cur.child[char].top_k, (weight, sentence))
                else:
                    smallest = hq.nsmallest(1, cur.child[char].top_k)
                    if weight > smallest[0][0]:
                        hq.heapreplace(cur.child[char].top_k,
                                       (weight, sentence))
            else:
                cur.child[char] = node()
                cur.child[char].top_k = [(weight, sentence)]
                hq.heapify(cur.child[char].top_k)
            cur = cur.child[char]
        return

    def match(self, partial_sentence, dump=False):
        cur = self.root
        anchor = 0
        if dump:
            logging.info(partial_sentence)
        for char in partial_sentence:
            anchor += 1
            char = str(char)
            if char in cur.child:
                cur = cur.child[char]
            else:
                return anchor, []
        _re = cur.top_k
        _re.sort(key=lambda x: x[0])
        re = [_re[len(_re) - r - 1][1] for r in range(len(_re))]
        return anchor, re

    def load(self, dump_file):
        dump_f = open(dump_file, 'rb')
        obj = pickle.load(dump_f)
        ind = [0]
        self.traversal(obj, self.root, True, ind)
        dump_f.close()

    def dump(self, dump_file):
        obj = []
        self.traversal(obj, self.root)
        dump_f = open(dump_file, 'wb')
        pickle.dump(obj, dump_f)
        dump_f.close()

    def traversal(self, obj, cur, is_load=False, ind=[0]):
        if is_load:
            if ind[0] >= len(obj):
                raise IndexError
            childs = obj[ind[0]]
            cur.top_k = obj[ind[0] + 1]
            for ch in childs:
                cur.child[ch] = node()
            ind[0] += 2
            for ch in childs:
                self.traversal(obj, cur.child[ch], True, ind)
            return
        childs = list(cur.child.keys())
        obj.append(childs)
        obj.append(cur.top_k)
        for ch in childs:
            self.traversal(obj, cur.child[ch])


class QuerySuggestion:
    def __init__(self, top_k):
        self.top_k = top_k
        self.trie = Trie(top_k)
        return

    def build(self, meta_file, inverted_index_folder):
        self.corpus = []
        inv_ind = InvertedIndexer(inverted_index_folder, in_memory=True)
        _corpus = list(inv_ind.keys())
        self.corpus = [(sentence, -1.0 / inv_ind.get_doc_num(sentence))
                       for sentence in _corpus]
        del inv_ind
        meta = load_meta(meta_file)
        docids = list(meta.keys())
        _corpus = [(meta[doc]["title"], 0) for doc in docids]
        self.corpus += _corpus
        del meta
        for item in self.corpus:
            sentence = item[0]
            weight = item[1]
            self.trie.add(sentence, weight)
        return

    def load(self, trie_dump_file):
        self.trie.load(trie_dump_file)

    def dump(self, trie_dump_file):
        # self.trie.traversal(self.trie.root, "")
        self.trie.dump(trie_dump_file)

    def suggest(self, partial_query):
        assert len(partial_query) > 0, "empty query string"
        anchor = 0
        last_step = 0
        while anchor < len(partial_query) - 1:
            # logging.info(str(anchor) + "/" + str(len(partial_query)))
            _anchor, _re = self.trie.match(partial_query[anchor:], False)
            last_step = anchor
            anchor += _anchor
        re = [partial_query[:last_step] + r for r in _re]
        return re