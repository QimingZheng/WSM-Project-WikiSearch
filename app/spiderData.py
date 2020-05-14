import os, sys
lib_path = os.path.abspath(os.path.join('../wikisearch'))
sys.path.append(lib_path)

import requests
import re
import json
import urllib
import time
# from lxml import etree
from flask import render_template

import wikisearch
from wikisearch.searcher.boolean_searcher import *
from wikisearch.searcher.cosine_searcher import *
from wikisearch.searcher.tfidf_searcher import *

def search_info(query):
    start = time.time()
    searcher = NaiveBooleanSearch("../data/index/inverted_index.json", "../data/index/meta.json", 1)
    result = searcher.search(query, dump=False)
    tim = time.time() - start
    for res in result:
        print (res["url"], res["title"])
    return result, tim
