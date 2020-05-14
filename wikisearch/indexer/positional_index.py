from wikisearch.indexer.build_index_util import *


def BuildPositionalIndex(articles, indexFile):
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
    # output to indexFile
    with open(indexFile, "w") as indfile:
        for term, docList in positionalIndex.items():
            # indfile.write(json.dumps({term:sorted(docList)})+"\n")
            indfile.write(json.dumps({term: docList}) + "\n")
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