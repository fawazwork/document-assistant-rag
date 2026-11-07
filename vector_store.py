import faiss


def build_index(vectors):
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    return index


def search(index, query_vector, k=3):
    k = min(k, index.ntotal)
    scores, ids = index.search(query_vector, k)
    return scores[0], ids[0]