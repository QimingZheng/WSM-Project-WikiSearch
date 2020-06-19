import json
import sys


def metric(label, result):
    """
    return:
        precision, recall
    """
    assert len(label) > 0, "length of label is 0, recall is undefined"
    assert len(result) > 0, "length of result is 0, precision is undefined"
    precision = 1.0 * sum([1 if x in label else 0 for x in result]) / (1.0 * len(result))
    recall = 1.0 * sum([1 if x in label else 0 for x in result]) / (1.0 * len(label))
    return precision, recall

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        lines = f.readlines()
    for line in lines:
        data = json.loads(line)
        q = data["query"]
        ground_truth = data["heap"]
        del data["query"]
        del data["heap"]
        for filter_type, results in data.items():
            for method, result in results.items():
                try:
                    precision, recall = metric(ground_truth[method], result)
                    print(filter_type, method, precision, recall)
                except:
                    print("erro")
