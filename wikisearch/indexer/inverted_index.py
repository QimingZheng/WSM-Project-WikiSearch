from wikisearch.indexer.build_index_util import *
import multiprocessing as mp
import os


def BuildInvertedIndex(articles, indexFile):
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
    # output to indexFile
    with open(indexFile, "w") as indfile:
        for term, docList in invertedIndex.items():
            # indfile.write(json.dumps({term:sorted(docList)})+"\n")
            indfile.write(json.dumps({term: docList}) + "\n")
    return


def parallelBuildInvertedIndex(article_file_list, indexFile):
    cpu_num = mp.cpu_count()
    pool = mp.Pool(cpu_num)
    article_list = pool.map(parseWikiJsons, article_file_list)
    pool.starmap(BuildInvertedIndex, [(article_list[i], indexFile + str(i))
                                      for i in range(len(article_list))])
    inverted_index_list = pool.map(
        LoadInvertedIndex,
        [indexFile + str(i) for i in range(len(article_list))])
    invertedIndex = merge_inverted_index(inverted_index_list)
    # output to indexFile
    with open(indexFile, "w") as indfile:
        for term, docList in invertedIndex.items():
            # indfile.write(json.dumps({term:sorted(docList)})+"\n")
            indfile.write(json.dumps({term: docList}) + "\n")
    for i in range(len(article_list)):
        if os.path.exists(indexFile + str(i)):
            os.remove(indexFile + str(i))
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
                    # invertedIndex[k] = list(set(invertedIndex[k]).union(set(v)))
            line = indfile.readline()
    return invertedIndex


def merge_inverted_index(inverted_index_list):
    """
    Need to be optimized. Very Slow, no appearant parallel way (parallel write dictionary, locks are slow)
    """
    # cpu_num = mp.cpu_count()
    # mgr = mp.Manager()
    # invertedIndex = mgr.dict()
    terms = []
    for ind in inverted_index_list:
        terms += list(ind.keys())
    invertedIndex = {}
    # def _dict_insert(invind, terms, inv_ind_lst, rank, wordl_size):
    #     for id in range(len(terms)):
    #         if id % wordl_size != rank:
    #             continue
    #         term = terms[id]
    #         temp_dict = {}
    #         temp_dict[term] = {}
    #         for ind in inv_ind_lst:
    #             if not term in ind:
    #                 continue
    #             temp_dict[term].update(ind[term])
    #         invind[term] = temp_dict[term]
    # jobs = [mp.Process(target=_dict_insert, args=(invertedIndex, terms, inverted_index_list, i, cpu_num)) for i in range(cpu_num)]
    # for j in jobs:
    #     j.start()
    # for j in jobs:
    #     j.join()
    for term in terms:
        invertedIndex[term] = {}
        for ind in inverted_index_list:
            if not term in ind:
                continue
            invertedIndex[term].update(ind[term])
    return invertedIndex
