from src.vector_store import semantic_search
from src.bm25_search import bm25_search
from src.hybrid_search import hybrid_search


def collect_results(queries, model, index, bm25, chunks):
    evaluation_results = []

    for question in queries:
        query = question["query"]

        semantic = semantic_search(
            query, model, index, chunks, k=10
        )

        keyword = bm25_search(
            query, bm25, chunks, k=10
        )

        hybrid = hybrid_search(
            query, model, index, bm25, chunks, k=10
        )

        evaluation_results.append({
            "query_id": question["query_id"],
            "query": query,
            "semantic": semantic,
            "bm25": keyword,
            "hybrid": hybrid
        })

    return evaluation_results
