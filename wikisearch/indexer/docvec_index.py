from wikisearch.indexer.build_index_util import *
from wikisearch.indexer.indexer_base import *
import os
import shutil
import linecache


def saveDocVecIndexMeta(docid2F, indexFolder):
    with open(os.path.join(indexFolder, "docvec_index_meta.json"),
              'w') as ind_meta:
        for docid, (filename, lineno) in docid2F.items():
            ind_meta.write(json.dumps({docid: (filename, lineno)}) + "\n")


def loadDocVecIndexMeta(indexFolder):
    docid2F = {}
    with open(os.path.join(indexFolder, "docvec_index_meta.json")) as ind_meta:
        line = ind_meta.readline()
        while line:
            meta = json.loads(line)
            for docid, (filename, lineno) in meta.items():
                docid2F[docid] = (filename, lineno)
            line = ind_meta.readline()
    return docid2F


def BuildDocVecIndex(article_file, indexFolder):
    """build document vector index, see slide Lect-4-p50

    Args:
        articles (list(json)): list of article jsons
        indexFile (str): index file name
    """
    articles = parseWikiJsons(article_file)
    DocVecIndex = {}
    for article in articles:
        docID = article["uid"]
        DocVecIndex[docID] = {}
        text = text_segmentation(article["text"])
        for word in text:
            if not word in DocVecIndex[docID]:
                DocVecIndex[docID][word] = 1
            else:
                DocVecIndex[docID][word] += 1
    docid2F = {}
    # output to indexFile
    indexFile = os.path.join(indexFolder, "docvec_index.json")
    with open(indexFile, "w") as indfile:
        lineno = 1
        for docID, term_freq_dict in DocVecIndex.items():
            indfile.write(json.dumps({docID: term_freq_dict}) + "\n")
            docid2F[docID] = (indexFile, lineno)
            lineno += 1
    saveDocVecIndexMeta(docid2F, indexFolder)
    return


def parallelBuildDocVecIndex(wikis, indexFolder):
    cpu_num = mp.cpu_count()
    pool = mp.Pool(cpu_num)
    # articles = pool.map(parseWikiJsons, wikis)

    for i in range(len(wikis)):
        indFolder = os.path.join(indexFolder, str(i))
        if not os.path.exists(indFolder):
            os.mkdir(indFolder)

    pool.starmap(BuildDocVecIndex,
                 [(wikis[i], os.path.join(indexFolder, str(i)))
                  for i in range(len(wikis))])

    for i in range(len(wikis)):
        indFolder = os.path.join(indexFolder, str(i))
        shutil.move(
            os.path.join(indFolder, "docvec_index.json"),
            os.path.join(indexFolder, "docvec_index." + str(i) + ".json"))

    with open(os.path.join(indexFolder, "docvec_index_meta.json"),
              'w') as metaF:
        for i in range(len(wikis)):
            indFolder = os.path.join(indexFolder, str(i))
            with open(os.path.join(indFolder, "docvec_index_meta.json"),
                      'r') as srcF:
                line = srcF.readline()
                while line:
                    tmp = json.loads(line)
                    for docid, (_, lineno) in tmp.items():
                        metaF.write(json.dumps({
                            docid:
                            (os.path.join(indexFolder, "docvec_index." +
                                          str(i) + ".json"), lineno)
                        }) + "\n")
                    line = srcF.readline()

    for i in range(len(wikis)):
        indFolder = os.path.join(indexFolder, str(i))
        if os.path.exists(indFolder):
            shutil.rmtree(indFolder)

    return


def LoadDocVecIndex(indexFile):
    DocVecIndex = {}
    with open(indexFile) as indfile:
        line = indfile.readline()
        while line:
            ind = json.loads(line)
            for docid, term_freq_dict in ind.items():
                DocVecIndex[int(docid)] = {}
                for _term, _freq in term_freq_dict.items():
                    DocVecIndex[int(docid)][_term] = int(_freq)
            line = indfile.readline()
    return DocVecIndex


class DocVecIndexer(Indexer):
    def __init__(self, IndexFolder):
        super().__init__(IndexFolder)
        self.meta = loadDocVecIndexMeta(IndexFolder) # meta information is small enough to be stored in memory

    def __getitem__(self, key):
        (filename, lineno) = self.meta[key]
        content = linecache.getline(filename, lineno)
        linecache.clearcache()
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
