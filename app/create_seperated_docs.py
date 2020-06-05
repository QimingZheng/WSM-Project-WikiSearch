"""
Convert parsed json file into seperated doc files, save meta data
"""
import json
import os
from tqdm import tqdm


def get_files(path):
    files = os.listdir(path)
    files = [os.path.join(path, file) for file in files]
    return files


def maybe_make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def write_file(path, file):
    with open(path, 'w') as f:
        f.write(file)


def read_file(path):
    with open(path, 'r') as f:
        return f.readlines()


def parse_json_file(json_path, output_dir):
    maybe_make_dir(output_dir)
    files = get_files(json_path)
    meta_data = {}
    for i in tqdm(range(len(files))):
        file = files[i]
        lines = read_file(file)
        for j in tqdm(range(len(lines))):
            line = lines[j]
            line_obj = json.loads(line)
            output_file_name = os.path.join(output_dir, line_obj['id']+".json")
            meta_data[line_obj['id']] = output_file_name
            write_file(output_file_name, line)
    write_file(os.path.join(output_dir, "meta.json"), json.dumps(meta_data))


if __name__ == "__main__":
    parse_json_file("../data/parsed/text/AA/", "../data/parsed/docs/")
