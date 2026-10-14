from src.bm25_search import bm25_search
from src.vector_store import semantic_search

def hybrid_search(query, model, index, bm25, chunks, k=5):
    semantic_results = semantic_search(query, model, index, chunks, k=20)
    bm25_results = bm25_search(query, bm25, chunks, k=20)

    rrf_scores = {}

    c = 60


    for results in [semantic_results, bm25_results]:
        for rank, chunk in enumerate(results, start=1):
            chunk_id = chunk['chunk_id']

            contribution = 1/(c+rank)

            initial_scores = rrf_scores.get(chunk_id, 0)

            rrf_scores[chunk_id] = initial_scores + contribution


    sorted_scores = sorted(
        rrf_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )[:k]

    top_k = []

    chunk_lookup = {
        chunk['chunk_id']: chunk
        for chunk in chunks
    }

    top_k = []

    for chunk_id, score in sorted_scores:
        result = chunk_lookup[chunk_id].copy()
        result['score'] = float(score)
        top_k.append(result)

    return top_k




            

