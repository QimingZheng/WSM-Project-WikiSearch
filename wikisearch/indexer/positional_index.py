from wikisearch.indexer.build_index_util import *
import os
import shutil
import linecache


def savePosIndexMeta(term2F, indexFolder):
    with open(os.path.join(indexFolder, "positional_index_meta.json"),
              'w') as ind_meta:
        for term, (filename, lineno) in term2F.items():
            ind_meta.write(json.dumps({term: (filename, lineno)}) + "\n")


def loadPosIndexMeta(indexFolder):
    term2F = {}
    with open(os.path.join(indexFolder,
                           "positional_index_meta.json")) as ind_meta:
        line = ind_meta.readline()
        while line:
            meta = json.loads(line)
            for term, (filename, lineno) in meta.items():
                term2F[term] = (filename, lineno)
            line = ind_meta.readline()
    return term2F


def BuildPositionalIndex(articles, indexFolder):
    """build the positional index, see slide Lect-2-p7

    Args:
        articles (list(json)): in memory articles
        indexFile (str): in disk index file

    Examples:
        {term: {DocID_0: [pos_00, pos_01, ... pos_0n1], ... DocID_m: [pos_m0, pos_m1, ... pos_mnm]}}
        the position list is sorted already
    """
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


def parallelBuildPositionalIndex(article_file_list, indexFolder):
    cpu_num = mp.cpu_count()
    pool = mp.Pool(cpu_num)
    article_list = pool.map(parseWikiJsons, article_file_list)

    for i in range(len(article_list)):
        indFolder = os.path.join(indexFolder, str(i))
        if not os.path.exists(indFolder):
            os.mkdir(indFolder)

    pool.starmap(BuildPositionalIndex,
                 [(article_list[i], os.path.join(indexFolder, str(i)))
                  for i in range(len(article_list))])
    pos_index_list = pool.map(LoadPositionalIndex, [
        os.path.join(os.path.join(indexFolder, str(i)),
                     "positional_index.json") for i in range(len(article_list))
    ])
    merge_pos_index(pos_index_list, indexFolder)

    for i in range(len(article_list)):
        if os.path.exists(os.path.join(indexFolder, str(i))):
            shutil.rmtree(os.path.join(indexFolder, str(i)))
    return

def merge_pos_index(pos_index_list, indexFolder):
    cpu_num = mp.cpu_count()
    terms = []
    for ind in pos_index_list:
        terms += list(ind.keys())

    terms = list(set(terms))

    def _build_partial_ind(terms, pos_ind_lst, rank, world_size, indexFolder):
        _partial_ind = {}
        with open(
                os.path.join(
                    indexFolder,
                    "positional_index." + str(rank % world_size) + ".json"),
                'w') as ind_file:
            for id in range(len(terms)):
                if id % world_size != rank:
                    continue
                term = terms[id]
                _partial_ind[term] = {}
                for ind in pos_ind_lst:
                    if not term in ind:
                        continue
                    _partial_ind[term].update(ind[term])
                ind_file.write(json.dumps({term: _partial_ind[term]}) + "\n")

    jobs = [
        mp.Process(target=_build_partial_ind,
                   args=(terms, pos_index_list, i, cpu_num, indexFolder))
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
            "positional_index." + str(i % cpu_num) + ".json"), i // cpu_num + 1)
    savePosIndexMeta(term2F, indexFolder)
    return
