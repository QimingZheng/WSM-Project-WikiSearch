import json
import codecs
from collections import defaultdict


def read_file(path):
    with codecs.open(path, 'r', 'utf8') as f:
        return f.readlines()


def get_avg_time(path):
    results = read_file(path)
    score = ["jaccard", "bow", "tf-idf"]
    filter_type = ["high-idf", "multi-terms", "cluster", "heap"]
    time_count = defaultdict(lambda: 0)
    num = len(results)
    for result in results:
        result = json.loads(result)
        for t in filter_type:
            for s in score:
                time_count[t+"+"+s] += float(result[t][s]['time'])
    for t in filter_type:
        for s in score:
            time_count[t+"+"+s] /= num
            print(t, s, time_count[t+"+"+s])
    return time_count


if __name__ == "__main__":
    print("time for title query result:")
    t1 = get_avg_time("./title_query_result.json")
    print()
    print("time for content query result:")
    t2 = get_avg_time("./content_query_result.json")
    score = ["jaccard", "bow", "tf-idf"]
    filter_type = ["high-idf", "multi-terms", "cluster", "heap"]
    print()
    for t in filter_type:
        times = []
        for s in score:
            times.append(t1[t+"+"+s])
            times.append(t2[t+"+"+s])
        times = ["%.4f"%t for t in times]
        print("&","& ".join(times))
