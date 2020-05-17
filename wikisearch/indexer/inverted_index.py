from wikisearch.indexer.build_index_util import *
import multiprocessing as mp
import os
import shutil
import linecache

def saveInvertedIndexMeta(term2F, indexFolder):
    with open(os.path.join(indexFolder, "inverted_index_meta.json"), 'w') as ind_meta:
        for term, (filename, lineno) in term2F.items():
            ind_meta.write(json.dumps({term: (filename, lineno)}) + "\n")


def loadInvertedIndexMeta(indexFolder):
    term2F = {}
    with open(os.path.join(indexFolder, "inverted_index_meta.json")) as ind_meta:
        line = ind_meta.readline()
        while line:
            meta = json.loads(line)
            for term, (filename, lineno) in meta.items():
                term2F[term] = (filename, lineno)
            line = ind_meta.readline()
    return term2F


def BuildInvertedIndex(articles, indexFolder):
    """build inverted index, see slide Lect-2-p19 (but a bit different, see the following example)

    Args:
        articles (list(json)): in memory articles
        indexFile (str): in disk index file

    Examples:
        each line of the inverted index file is a dumped json objects.
        {term: {DocID_0: freq_0, DocID_1: freq_1, ... DocID_n: freq_n}}
    """
    invertedIndex = dict()
    for article in articles:
        docID = article["uid"]
        text = text_segmentation(article["text"])
        for word in text:
            if not word in invertedIndex:
                invertedIndex[word] = {docID: 1}  # set([docID])
            else:
                if not docID in invertedIndex[word]:
                    invertedIndex[word][docID] = 1  # .add(docID)
                else:
                    invertedIndex[word][docID] += 1
    term2F = {}
    # output to indexFile
    with open(os.path.join(indexFolder, "inverted_index.json"),
              "w") as indfile:
        lineno = 1
        for term, docList in invertedIndex.items():
            term2F[term] = (os.path.join(indexFolder, "inverted_index.json"), lineno)
            indfile.write(json.dumps({term: docList}) + "\n")
            lineno += 1
    saveInvertedIndexMeta(term2F, indexFolder)
    return


def parallelBuildInvertedIndex(article_file_list, indexFolder):
    cpu_num = mp.cpu_count()
    pool = mp.Pool(cpu_num)
    article_list = pool.map(parseWikiJsons, article_file_list)

    for i in range(len(article_list)):
        indFolder = os.path.join(indexFolder, str(i))
        if not os.path.exists(indFolder):
            os.mkdir(indFolder)

    pool.starmap(BuildInvertedIndex,
                 [(article_list[i], os.path.join(indexFolder, str(i)))
                  for i in range(len(article_list))])
    inverted_index_list = pool.map(LoadInvertedIndex, [
        os.path.join(os.path.join(indexFolder, str(i)), "inverted_index.json")
        for i in range(len(article_list))
    ])
    merge_inverted_index(inverted_index_list, indexFolder)

    for i in range(len(article_list)):
        if os.path.exists(os.path.join(indexFolder, str(i))):
            shutil.rmtree(os.path.join(indexFolder, str(i)))
    return


def LoadMultiInvertedIndex(indexFiles, proc_num):
    pool = mp.Pool(proc_num)
    invertedIndices = pool.map(LoadInvertedIndex, indexFiles)
    return invertedIndices


def LoadInvertedIndex(indexFile):
    invertedIndex = {}
    with open(indexFile) as indfile:
        line = indfile.readline()
        while line:
            ind = json.loads(line)
            for k, v in ind.items():
                if not k in invertedIndex:
                    invertedIndex[k] = {}
                for _docid, _freq in v.items():
                    invertedIndex[k][int(_docid)] = _freq
            line = indfile.readline()
    return invertedIndex


def merge_inverted_index(inverted_index_list, indexFolder):
    cpu_num = mp.cpu_count()
    terms = []
    for ind in inverted_index_list:
        terms += list(ind.keys())

    terms = list(set(terms))

    def _build_partial_ind(terms, inv_ind_lst, rank, world_size, indexFolder):
        _partial_ind = {}
        with open(
                os.path.join(
                    indexFolder,
                    "inverted_index." + str(rank % world_size) + ".json"),
                'w') as ind_file:
            for id in range(len(terms)):
                if id % world_size != rank:
                    continue
                term = terms[id]
                _partial_ind[term] = {}
                for ind in inv_ind_lst:
                    if not term in ind:
                        continue
                    _partial_ind[term].update(ind[term])
                ind_file.write(json.dumps({term: _partial_ind[term]}) + "\n")

    jobs = [
        mp.Process(target=_build_partial_ind,
                   args=(terms, inverted_index_list, i, cpu_num, indexFolder))
        for i in range(cpu_num)
    ]

    for j in jobs:
        j.start()
    for j in jobs:
        j.join()

    term2F = {}
    for i in range(len(terms)):
        term2F[terms[i]] = (os.path.join(
            indexFolder,
            "inverted_index." + str(i % cpu_num) + ".json"), i // cpu_num + 1)
    saveInvertedIndexMeta(term2F, indexFolder)

    return
