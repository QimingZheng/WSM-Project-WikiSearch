import json
import codecs
from tqdm import tqdm
import os
from wikisearch.searcher.search import searcher
import time


def read_file(path):
    with codecs.open(path, "r", "utf8") as f:
        return f.readlines()

def run_and_write(path, queries):
    score = ["tf-idf", "jaccard", "bow"]
    filter_type = ["cluster", "high-idf", "multi-terms", "heap"]
    query_result_file = codecs.open(path, "w", "utf8")
    for query in tqdm(queries):
        res = {'query': query}
        for t in filter_type:
            res[t] = {}
            for s in score:
                result, words = my_searcher.search(query, score=s, filter_type=t)
                res[t][s] = result
        query_result_file.write(json.dumps(res,ensure_ascii=False)+"\n")
    query_result_file.close()


if __name__ == "__main__":
    title_query = read_file("./title_query.txt")
    content_query = read_file("./content_query.txt")
    print("load searcher")
    begin = time.time()
    my_searcher = searcher("../data/index/inv", "../data/index/docvec", "../data/index/meta.json", "../resources/stopwords/cn_stopwords.txt",
                           in_memory=True, proc_num=8, cluster_load=1, tf_idf=1)
    print("load done, use: %fs" % (time.time()-begin))
    print("run title query")
    run_and_write("./title_query_result.json", title_query)
    # print("run content query")
    # run_and_write("./content_query_result.json", content_query)
        
