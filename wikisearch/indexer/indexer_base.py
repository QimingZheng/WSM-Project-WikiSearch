import sys

class Indexer(object):
    def __init__(self, IndexFolder, in_memory):
        self.IndexFolder = IndexFolder
        self.meta = None
        self.in_memory = in_memory
        self.cache = {} # used if in_memory is true
        return

    def __sizeof__(self):
        return sys.getsizeof(self.meta)

    def __setitem__(self, key, item):
        raise Exception("indexer set error", "inverted indexer is read only")

    def __repr__(self):
        return repr(self.meta)
        # raise Exception("indexer repr error", "unsupported")
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

