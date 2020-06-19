import json
import codecs
from tqdm import tqdm
import os
import numpy as np


def read_file(path):
    with codecs.open(path, 'r', 'utf8') as f:
        return json.loads(f.read())


def get_files(path):
    files = os.listdir(path)
    files = [os.path.join(path, file) for file in files]
    return files


def generate_sample(n):
    files = get_files(docs_path)
    n = min(n, len(files))
    title_file = codecs.open("./title_query2.txt","w","utf8")
    content_file = codecs.open("./content_query2.txt","w","utf8")
    content_len = 15
    for i in tqdm(range(n)):
        idx = np.random.randint(len(files))
        file = files[idx]
        page = read_file(file)
        title = page['title']
        content = page['text']
        title_file.write(title+"\n")

        content = content.replace("\n","")[len(title):len(title)+content_len]
        if content == "":
            continue
        content_file.write(content+"\n")
    content_file.close()
    title_file.close()


docs_path = "../data/parsed/docs"

if __name__ == "__main__":
    generate_sample(10)
    {
        'query':'123',
        'heap':{
            'tf-idf':['1','2','3'],
            'jaccard':['1','2','3']
        }
    }