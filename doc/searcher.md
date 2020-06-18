# 搜索部分

#### 搜索方式：**boolean query**

#### Ranking algorithms

##### 分数计算方式

* 直接算得分，不考虑term frequency
  * JACCARD
* vector空间表示，算相似度，用cosine距离
  * Bag of words
  * TF-IDF

##### top k 筛选

* 先算好所有的$N$个文档得分，选出top $k$
  * heap
* Generic approach：先选出候选集$A$ ($k<|A|<<N$)，再从候选集$A$里选
  * Only consider high-idf query terms
  * Only consider docs containing many query terms
  * cluster based



#### 接口：

##### API

* searcher(

   ​				inverted_index_file,

  ​                 docvec_index_file,

  ​				meta_data_file,

  ​                 stopwords_file,

  ​                 in_memory=False,

  ​                 proc_num=1,

  ​                 idf_threshold=0.5,

  ​                 terms=3,

  ​                 seed=-1,

  ​                 cluster_load=-1,
  
  ​                 tf_idf=-1):

```
inverted_index_file: the file saving the index
docvec_index_file: the file saving the document vector
meta_data_file: the file saving the meta data
stopwords_file: the file containing stopwords
in_memory: if in the memory
proc_num: process number
idf_threshold: Given a term t, its df rate is df / N. Only term whose rate is less than
idf_threshold will be considered.
terms: only docs containing not less than <terms> terms in query will be considered.
seed: seed used in cluster algorithm. -1 indicates not using seed.
cluster_load: -1 indicates do not load and run anything. 0 indicates clustering and saving results. 1 indicates loading from file.
tf-idf: the same as cluster_load
```



* search(query, top_k=10, score="jaccard", filter_type="heap")

```
query: the query
top_k: select top k results
score: three kinds of scores: jaccard, bow, tf-idf
filter_type: four kinds of filter algorithms: heap, high-idf, multi-terms, cluster
```

##### Example

```python
mysearcher = searcher("../data/index/inv", "../data/index/meta.json", "../data/index/docvec",in_memory=True)
query = input("query input: ")
print(mysearcher.search(query))
```
