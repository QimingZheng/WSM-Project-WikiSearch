# wikipedia-search-engine

## Prerequisites

1. jieba
2. flask
3. wikipedia-zh dump dataset

## Quick Install

**install wikisearch**
```bash
# Enter a virtual environment (anaconda/virtualenv)
git clone https://github.com/QimingZheng/wikipedia-search-engine
git submodule update --init --recursive
python setup.py install # install wikisearch
```

**download wikipedia dump data and parse into jsons**
```bash
bash download.sh
```


**Test**
```bash
cd testings/
python test_indexer.py
python test_searcher.py
```

**run web**
```bash
cd app/
python web.py
```

![image](./doc/image.png)

## TODOs

* [ ] refactoring this project (cleaner code)
* [ ] add docs
* [ ] more parallel support
* [ ] more unittests

## Reference

[Introduction to Information Retrieval](https://nlp.stanford.edu/IR-book/)