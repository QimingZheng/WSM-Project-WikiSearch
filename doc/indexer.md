# 索引部分

一共实现了三种索引：

1. inverted index:
    - term : {doc-id-0: freq-0, doc-id-1: freq-1, ... doc-id-n: freq-n}
    - type(term) = str, type(doc-id) = str, type(freq) = int
2. positional index:
    - term : {doc-id-0: [pos-0-0, pos-0-1, ... pos-0-l0], .. doc-id-n: [pos-n-0, pos-n-1, ... pos-n-ln]}
    - type(term) = str, type(doc-id) = str, type([pos]) = list(int)
3. document vector index:
    - docid : {term-0: freq-0, term-1: freq-1, ... term-n: freq-n} # 只包含 freq > 0 的term
    - type(doc-id) = str, type(term) = str, type(freq) = int

使用示例：

```python
inv_ind = InvertedIndexer("../data/index/inv")
docvec_ind = DocVecIndexer("../data/index/docvec")
pos_ind = PositionalIndexer("../data/index/pos")

print(inv_ind.has_key("广州"))
print(len(inv_ind["广州"]))
print(len(inv_ind.keys()))

print(docvec_ind.has_key("165"))
print(len(docvec_ind["165"]))
print(len(docvec_ind.keys()))

print(pos_ind.has_key("广州"))
print(len(pos_ind["广州"]))
print(len(pos_ind.keys()))
```

注意，这些indexer只支持部分的常规python dict操作，包括：

```python
__getitem__
__len__
has_key
keys
```

三种indexer均提供了两种模式，in-memory和in-disk，in-memory的索引构建时间较长，且占用内存很高，但是索引速度快。
in-disk索引构建时间相对较短，内存占用小，但是索引速度慢。

默认情况下使用in-disk的模式，这种模式下，因为索引文件的规模比较大，Indexer只会保存meta信息在内存里，具体的取数据要访问磁盘。索引文件除了索引建立阶段外，都是只读的，上述的接口返回的是存在内存中的对象，可以任意操作（读/写），但不会反映到索引文件上。

# Meta 信息

根据doc-id得到文章的url/title信息，示例：

```python
meta = load_meta("../data/index/meta.json")
docid = "789084"
logging.info(meta[docid]['title'])
logging.info(meta[docid]['url'])
```
