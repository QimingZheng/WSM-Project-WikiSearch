from wikisearch.indexer.build_index_util import *


def BuildDocVecIndex(articles, indexFile):
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
    # output to indexFile
    with open(indexFile, "w") as indfile:
        for docID, term_freq_dict in DocVecIndex.items():
            # indfile.write(json.dumps({term:sorted(docList)})+"\n")
            indfile.write(json.dumps({docID: term_freq_dict}) + "\n")
    return


def parallelBuildDocVecIndex(wikis, indexFile):
    cpu_num = mp.cpu_count()
    pool = mp.Pool(cpu_num)
    articles = pool.map(parseWikiJsons, wikis)
    pool.starmap(BuildDocVecIndex, [(articles[i], indexFile + str(i))
                                    for i in range(len(wikis))])
    docvec_inds = pool.map(LoadDocVecIndex,
                           [indexFile + str(i) for i in range(len(wikis))])
    # output to indexFile
    with open(indexFile, "w") as indfile:
        for docvec_ind in docvec_inds:
            for docID, term_freq_dict in docvec_ind.items():
                indfile.write(json.dumps({docID: term_freq_dict}) + "\n")
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