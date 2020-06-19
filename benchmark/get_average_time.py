import json
import codecs
from collections import defaultdict


def read_file(path):
    with codecs.open(path, 'r', 'utf8') as f:
        return f.readlines()


def get_avg_time(path):
    results = read_file(path)
    score = ["tf-idf", "jaccard", "bow"]
    filter_type = ["cluster", "high-idf", "multi-terms", "heap"]
    time_count = defaultdict(lambda: 0)
    num = len(results)
    for result in results:
        result = json.loads(result)
        for t in filter_type:
            for s in score:
                time_count[t+"+"+s] += float(result[t][s]['time'])
    for t in filter_type:
        for s in score:
            print(t, s, time_count[t+"+"+s]/num)


if __name__ == "__main__":
    print("time for title query result:")
    get_avg_time("./title_query_result.json")
    print()
    print("time for content query result:")
    get_avg_time("./content_query_result.json")
