from wikisearch.indexer.build_index_util import *
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


def BuildDocVecIndex(articles, indexFolder):
    """build document vector index, see slide Lect-4-p50

    Args:
        articles (list(json)): list of article jsons
        indexFile (str): index file name
    """
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
    articles = pool.map(parseWikiJsons, wikis)

    for i in range(len(articles)):
        indFolder = os.path.join(indexFolder, str(i))
        if not os.path.exists(indFolder):
            os.mkdir(indFolder)

    pool.starmap(BuildDocVecIndex,
                 [(articles[i], os.path.join(indexFolder, str(i)))
                  for i in range(len(wikis))])

    for i in range(len(articles)):
        indFolder = os.path.join(indexFolder, str(i))
        shutil.move(
            os.path.join(indFolder, "docvec_index.json"),
            os.path.join(indexFolder, "docvec_index." + str(i) + ".json"))

    with open(os.path.join(indexFolder, "docvec_index_meta.json"),
              'w') as metaF:
        for i in range(len(articles)):
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

    for i in range(len(articles)):
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
