import json
import sys
import multiprocessing as mp
from wikisearch.util import *
# import wikisearch.deps.jieba.jieba as jieba

import math
import os


def readwiki(wikiFile):
    """read the articles in a wiki file

    Args:
        wikiFile (str): the filename of wiki files (should be generated by the wikiextractor tool)

    Returns:
        re (str): a concated article string
    """
    re = []
    with open(wikiFile) as wiki:
        wikiLine = wiki.readline()
        while wikiLine:
            re.append(wikiLine)
            wikiLine = wiki.readline()
    return re


def parseWikiJsons(wikiFile, only_meta=False):
    """parse a wiki string into multiple jsons, each json object contains one article

    Args:
        wikiFile (str): wiki file name
        only_meta (bool, optional): whether generate meta info or not. Defaults to False.

    Returns:
        articles (lsit[json]): each article is represented as a json object
    
    Examples:
        articles = dict{"uid": int, "url": wikipedia link of this article, "text": article content, "title": title of this article}
    """
    jsonStrings = readwiki(wikiFile)
    # DOMTree = xml.dom.minidom.parse(xmlFile)
    articles = []
    for jstr in jsonStrings:
        article = json.loads(jstr)
        article["uid"] = int(
            article["url"][article["url"].find("=") +
                           1:])  # use the id in the url as the uid
        if only_meta:
            article.pop("text")
        else:
            article["text"] = Traditional2Simplified(article["text"])
        article["title"] = Traditional2Simplified(article["title"])
        articles.append(article)
    return articles


# dump article meta information

def dump_meta(wikiFile, metaFile):
    """dump meta info of articles into files

    Args:
        wikiFile (str): wiki file name
        metaFile (str): meta info file name

    Examples:
        meta = dict{"uid": int, "url": wikipedia link of this article, "title": title of this article}
    """
    articles = parseWikiJsons(wikiFile, True)
    with open(metaFile, 'w') as metaF:
        for article in articles:
            metaF.write(json.dumps(article) + '\n')


def parallel_dump_meta(wikis, metaFile):
    """parallelize dump_meta

    Args:
        wikiFile (str): wiki file name
        metaFile (str): meta info file name
    """
    cpu_num = mp.cpu_count()
    pool = mp.Pool(cpu_num)
    pool.starmap(dump_meta,
                 [(wikis[i], metaFile + str(i)) for i in range(len(wikis))])
    articles = pool.map(load_meta,
                        [metaFile + str(i) for i in range(len(wikis))])
    with open(metaFile, 'w') as metaF:
        for i in range(len(wikis)):
            for uid, article in articles[i].items():
                metaF.write(json.dumps(article) + '\n')
    for i in range(len(wikis)):
        if os.path.exists(metaFile + str(i)):
            os.remove(metaFile + str(i))


def load_meta(metaFile):
    """load article meta info from dump files

    Args:
        metaFile (str): meta info file name

    Returns:
        articles (dict{int: json}): json objects contains the article meta
    """
    articles = dict()
    with open(metaFile) as metaF:
        line = metaF.readline()
        while line:
            _article = json.loads(line)
            articles[_article["uid"]] = _article
            line = metaF.readline()
    return articles
