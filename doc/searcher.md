# 搜索部分

需要实现的搜索算法（待定）：

1. boolean search

2. tfidf search

3. doc-query cosine search

接口：

```python
searcher = XXXSearcher(meta_file, index_folder, process_num, in_mem)
# meta_file str wiki文章元数据文件，包含 doc-id url title content
# index_folder str 索引数据文件夹 (可能有多种索引，暂不确定)
# process_num int 搜索算法可用的进程数
# in_mem bool 指定indexer是否使用in-memory模式

ranked_results = searcher.search(query)
# query str 查询字符串
# ranked_results list(str) 排序后的搜索结果，wiki-doc-id列表
```
