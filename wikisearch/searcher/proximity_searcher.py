from wikisearch.searcher.searcher_util import *
import time
import bisect


def positional_search(query, pos_ind, doc_id):
    q_term_pos = []
    for q_term in query:
        q_term_pos.append(pos_ind[q_term][doc_id])
    for first_q_term_pos in q_term_pos[0]:
        last_pos = first_q_term_pos
        for term_id in range(1, len(query)):
            pos = bisect.bisect_left(q_term_pos[term_id], last_pos + 1)
            if pos < len(q_term_pos[term_id]) and pos >= 0:
                last_pos = q_term_pos[term_id][pos] + 1
            else:
                last_pos = -1
                break
        if last_pos >= 0:
            return doc_id
    return -1


class ProximitySearch(SearchEngineBase):
    def __init__(self, pos_index_file, meta_file, proc_num=1):
        self.proc_num = proc_num
        start = time.time()
        self.positionalIndex = LoadPositionalIndex(pos_index_file)
        self.article_mata = load_meta(meta_file)
        elapsed = time.time() - start
        logging.info("Build ProximitySearch Engine in %f secs" % elapsed)
        return

    def search(self, query):
        """
        exact search
        """
        N = len(self.article_mata)
        query = Traditional2Simplified(query)
        query = list(text_segmentation(query))
        result = list(self.positionalIndex[
            query[0]].keys()) if query[0] in self.positionalIndex else []
        for q_term in query:
            if q_term in self.positionalIndex:
                result = list(
                    set(result).intersection(
                        set(self.positionalIndex[q_term].keys())))
            else:
                result = []
                break

        pool = mp.Pool(self.proc_num)
        matched_doc_id = pool.starmap(positional_search,
                                      [(query, self.positionalIndex, res)
                                       for res in result])
        result = []
        for doc_id in matched_doc_id:
            if doc_id >= 0:
                result.append({
                    "url": self.article_mata[doc_id]["url"],
                    "title": self.article_mata[doc_id]["title"]
                })
        return result
