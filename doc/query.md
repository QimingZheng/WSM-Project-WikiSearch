# Query处理

## Query 补全

**大致的思路**

1. 用倒排索引的term和所有文章的title作为语料（正确的做法应该是采用用户query log作为语料），这样就有了很多的短语（词语和单字）以及常用的短语组合
2. 为语料中的每个项设计权重（用于挑选top-k candidate list），我采用的是：
    - 对于title，所有的title的权重均为0
    - 对于term，权重为 - 1/freq(term)
    也就是说偏好频繁出现的term，比起term更偏好title
3. 基于语料构建trie树
4. query补全的时候，从句首开始，逐字在trie树中查找，出现没有匹配的词时，认为是一个新短语的开始位置，回退到trie树根继续查找后续的query，直到query完全匹配完，这时在树中的位置即为需要补全的开始位置，选择top-k list，返回。

注意，返回的补全query有如下几种情况：
1. 返回的candidate list长度小于top-k （语料中对应这个trie树前缀的短语不足top-k条，全部返回了）
2. 返回的candidate list为空list（可能是语料中没有东西可补全这个query，也可能是query本身的语义已经完整了，最后一个词用户已经敲完了，这两种情况都没必要补全了）
3. 返回的candidate list长度正好为top-k （正常情况）

**使用**

```python
qs = QuerySuggestion(10)
qs.load("../data/index/query_suggestion.pkl")
partial_query = "日料里的三文"
qs.suggest(partial_query)
```
