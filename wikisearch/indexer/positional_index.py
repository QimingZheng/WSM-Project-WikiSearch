from wikisearch.indexer.build_index_util import *
from wikisearch.indexer.indexer_base import *
import os
import shutil
import linecache
from tqdm import tqdm


def savePosIndexMeta(term2F, indexFolder):
    with open(os.path.join(indexFolder, "positional_index_meta.json"),
              'w') as ind_meta:
        for term, filename_lineno in term2F.items():
            ind_meta.write(json.dumps({term: filename_lineno}) + "\n")


def loadPosIndexMeta(indexFolder):
    term2F = {}
    with open(os.path.join(indexFolder,
                           "positional_index_meta.json")) as ind_meta:
        line = ind_meta.readline()
        while line:
            meta = json.loads(line)
            for term, filename_lineno in meta.items():
                term2F[term] = filename_lineno
            line = ind_meta.readline()
    return term2F


def BuildPositionalIndex(article_file, indexFolder):
    """build the positional index, see slide Lect-2-p7

    Args:
        articles (list(json)): in memory articles
        indexFile (str): in disk index file

    Examples:
        {term: {DocID_0: [pos_00, pos_01, ... pos_0n1], ... DocID_m: [pos_m0, pos_m1, ... pos_mnm]}}
        the position list is sorted already
    """
    articles = parseWikiJsons(article_file)
    positionalIndex = dict()
    for article in articles:
        docID = article["uid"]
        text = text_segmentation(article["text"])
        for pos, word in enumerate(text):
            if not word in positionalIndex:
                positionalIndex[word] = {}
            if not docID in positionalIndex[word]:
                positionalIndex[word][docID] = [pos]
            else:
                positionalIndex[word][docID].append(pos)
    term2F = {}
    # output to indexFile
    indexFile = os.path.join(indexFolder, "positional_index.json")
    with open(indexFile, "w") as indfile:
        lineno = 1
        for term, docList in positionalIndex.items():
            term2F[term] = (indexFile, lineno)
            indfile.write(json.dumps({term: docList}) + "\n")
            lineno += 1
    savePosIndexMeta(term2F, indexFolder)
    return


def LoadPositionalIndex(indexFile):
    positionalIndex = {}
    with open(indexFile, 'r') as indFile:
        line = indFile.readline()
        while line:
            ind = json.loads(line)
            for term, term_pos_in_docs in ind.items():
                if not term in positionalIndex:
                    positionalIndex[term] = {}
                for _doc, _pos_list in term_pos_in_docs.items():
                    positionalIndex[term][int(_doc)] = _pos_list
            line = indFile.readline()
    return positionalIndex

def _build_pos_ind(indFol):
    return PositionalIndexer(indFol)

def parallelBuildPositionalIndex(article_file_list, indexFolder):
    cpu_num = mp.cpu_count()
    pool = mp.Pool(cpu_num)
    # article_list = pool.map(parseWikiJsons, article_file_list)

    for i in range(len(article_file_list)):
        indFolder = os.path.join(indexFolder, str(i))
        if not os.path.exists(indFolder):
            os.mkdir(indFolder)

    # pool.starmap(BuildPositionalIndex,
    #              [(article_file_list[i], os.path.join(indexFolder, str(i)))
    #               for i in range(len(article_file_list))])

    pos_index_list = pool.map(
        _build_pos_ind,
        [os.path.join(indexFolder, str(i)) for i in range(len(article_file_list))])

    merge_pos_index(pos_index_list, indexFolder)

    for i in range(len(article_file_list)):
        # if os.path.exists(os.path.join(indexFolder, str(i))):
        #     shutil.rmtree(os.path.join(indexFolder, str(i)))
        meta_file = os.path.join(os.path.join(indexFolder, str(i)), "positional_index_meta.json")
        if os.path.exists(meta_file):
            os.remove(meta_file)
    return


def merge_pos_index(pos_index_list, indexFolder):
    cpu_num = mp.cpu_count()
    terms = []
    for ind in pos_index_list:
        terms += list(ind.keys())

    terms = list(set(terms))

    term2F = {}
    
    for i in range(len(terms)):
        term2F[terms[i]] = []
        for ind in pos_index_list:
            if not ind.has_key(terms[i]):
                continue
            term2F[terms[i]].append(ind.get_meta(terms[i]))

    savePosIndexMeta(term2F, indexFolder)
    return


def _line2json(filename, lineno):
    content = linecache.getline(filename, lineno)
    linecache.clearcache()
    return json.loads(content)

class PositionalIndexer(Indexer):
    def __init__(self, IndexFolder, in_memory=False, thread_num=0):
        super().__init__(IndexFolder, in_memory)
        self.meta = loadPosIndexMeta(IndexFolder) # meta information is small enough to be stored in memory
        if self.in_memory:
            term_list = list(self.meta.keys())
            for id in tqdm(range(len(term_list))):
                term = term_list[id]
                self.cache[term] = {}
                for (filename, lineno) in self.meta[term]:
                    content = linecache.getline(filename, lineno)
                    self.cache[term].update(json.loads(content)[term])
            linecache.clearcache()
        if thread_num > 0:
            self.thread_num = thread_num
        else:
            self.thread_num = mp.cpu_count()
        self.pool = mp.Pool(self.thread_num)

    def __getitem__(self, key):
        if self.in_memory:
            return self.cache[key]
        re = {}
        re[key] = {}
        filename_lineno = self.meta[key]
        # for (filename, lineno) in filename_lineno:
        #     content = linecache.getline(filename, lineno)
        #     re[key].update(json.loads(content)[key])
        # linecache.clearcache()
        
        res = self.pool.starmap(_line2json,
                                [(i[0], i[1]) for i in filename_lineno])

        for _re in res:
            re[key].update(_re[key])

        return re[key]
        # return self.__dict__[key]

    def get_meta(self, key):
        return self.meta[key]

    def __len__(self):
        return len(self.meta)
        # return len(self.__dict__)

    def has_key(self, k):
        return k in self.meta
        # return k in self.__dict__

    def keys(self):
        return self.meta.keys()
        # return self.__dict__.keys()