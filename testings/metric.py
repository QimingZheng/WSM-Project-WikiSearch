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
    filter_method_dict = {}
    for line in lines:
        data = json.loads(line)
        q = data["query"]
        ground_truth = data["heap"]
        del data["query"]
        del data["heap"]
        del data["time"]
        for filter_type, results in data.items():
            for method, result in results.items():
                try:
                    precision, recall = metric(ground_truth[method]["result"], result["result"])
                    if not filter_type in filter_method_dict:
                        filter_method_dict[filter_type] = {}
                    if not method in filter_method_dict[filter_type]:
                        filter_method_dict[filter_type][method] = []
                    filter_method_dict[filter_type][method].append((precision, recall))
                except:
                    continue
    for filter_type in filter_method_dict.keys():
        for method in filter_method_dict[filter_type].keys():
            prec = [x[0] for x in filter_method_dict[filter_type][method]]
            reca = [x[1] for x in filter_method_dict[filter_type][method]]
            print (filter_type, method, "precision", sum(prec) * 1.0 / len(prec), "recall", sum(reca)*1.0/len(reca))

