from wikisearch.indexer.inverted_index import *
from wikisearch.indexer.docvec_index import *
from wikisearch.indexer.positional_index import *

class Indexer(object):
    def __init__(self, IndexFolder):
        self.IndexFolder = IndexFolder
        return

    def __setitem__(self, key, item):
        raise Exception("indexer set error", "inverted indexer is read only")

    def __repr__(self):
        raise Exception("indexer repr error", "unsupported")
        # return repr(self.__dict__)

    def __delitem__(self, key):
        raise Exception("indexer delitem error", "inverted indexer is read only")
        # del self.__dict__[key]

    def clear(self):
        raise Exception("indexer clear error", "inverted indexer is read only")
        # return self.__dict__.clear()

    def copy(self):
        raise Exception("indexer copy error", "inverted indexer is read only")
        # return self.__dict__.copy()

    def update(self, *args, **kwargs):
        raise Exception("indexer update error", "inverted indexer is read only")
        # return self.__dict__.update(*args, **kwargs)

    def values(self):
        raise Exception("indexer values error", "inverted indexer is stored on disk, load values is inefficient")
        # return self.__dict__.values()

    def items(self):
        raise Exception("indexer values error", "inverted indexer is stored on disk, load items is inefficient")
        # return self.__dict__.items()

    def pop(self, *args):
        raise Exception("indexer pop error", "inverted indexer is read only")
        # return self.__dict__.pop(*args)

    def __cmp__(self, dict_):
        raise Exception("indexer cmp error", "unsupported")
        # return self.__cmp__(self.__dict__, dict_)

    def __contains__(self, item):
        raise Exception("indexer contains error", "unsupported")
        return item in self.__dict__

    def __iter__(self):
        raise Exception("indexer iter error", "unsupported")
        return iter(self.__dict__)

    def __unicode__(self):
        raise Exception("indexer unicode error", "unsupported")
        return unicode(repr(self.__dict__))

class InvertedIndexer(Indexer):
    def __init__(self, IndexFolder):
        super().__init__(IndexFolder)
        self.meta = loadInvertedIndexMeta(IndexFolder) # meta information is small enough to be stored in memory

    def __getitem__(self, key):
        (filename, lineno) = self.meta[key]
        content = linecache.getline(filename, lineno)
        return json.loads(content)[key]
        # return self.__dict__[key]

    def __len__(self):
        return len(self.meta)
        # return len(self.__dict__)

    def has_key(self, k):
        return k in self.meta
        # return k in self.__dict__

    def keys(self):
        return self.meta.keys()
        # return self.__dict__.keys()

class DocVecIndexer(Indexer):
    def __init__(self, IndexFolder):
        super().__init__(IndexFolder)
        self.meta = loadDocVecIndexMeta(IndexFolder) # meta information is small enough to be stored in memory

    def __getitem__(self, key):
        (filename, lineno) = self.meta[key]
        content = linecache.getline(filename, lineno)
        return json.loads(content)[key]
        # return self.__dict__[key]

    def __len__(self):
        return len(self.meta)
        # return len(self.__dict__)

    def has_key(self, k):
        return k in self.meta
        # return k in self.__dict__

    def keys(self):
        return self.meta.keys()
        # return self.__dict__.keys()


class PositionalIndexer(Indexer):
    def __init__(self, IndexFolder):
        super().__init__(IndexFolder)
        self.meta = loadPosIndexMeta(IndexFolder) # meta information is small enough to be stored in memory

    def __getitem__(self, key):
        (filename, lineno) = self.meta[key]
        content = linecache.getline(filename, lineno)
        return json.loads(content)[key]
        # return self.__dict__[key]

    def __len__(self):
        return len(self.meta)
        # return len(self.__dict__)

    def has_key(self, k):
        return k in self.meta
        # return k in self.__dict__

    def keys(self):
        return self.meta.keys()
        # return self.__dict__.keys()