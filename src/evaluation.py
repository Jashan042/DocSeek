from src.vector_store import semantic_search

def recall_at_k( retrieved_ids: list[int], relevant_ids: list[int], k: int = 5) -> float:

    # only keep the k
    retrieved_ids = retrieved_ids[:k]
    # convert to set to remove duplicates
    retrieved_ids = set(retrieved_ids)
    relevant_ids = set(relevant_ids)

    # get the intersection (ids which exist in both retrived and relevant)
    matching = retrieved_ids & relevant_ids

    # check for dividing with zero case
    if (len(matching) == 0) or (len(relevant_ids) == 0): return 0
    # returnt he Recall@k
    return (len(matching)/len(relevant_ids)) 


def reciprocal_rank_at_k(retrieved_ids: list[int], relevant_ids: list[int], k: int = 10) -> float:
    retrieved_ids = retrieved_ids[:k]
    # loop to check if the relevnat chunk is in retrievd and its position. 
    for i, id in enumerate(retrieved_ids):
        if id in relevant_ids:
            return 1/(i+1)

    return 0 



def evaluate_search(queries, search_results):
    methods = ["semantic", "bm25", "hybrid"]

    # Match search results to questions using query_id
    results_by_id = {
        result["query_id"]: result
        for result in search_results
    }

    evaluation = {}

    for method in methods:
        recall_scores = []
        rr_scores = []

        for question in queries:
            query_id = question["query_id"]
            relevant_ids = question["relevant_chunk_ids"]

            # Skip questions without relevance labels
            if not relevant_ids:
                continue

            # Find corresponding search results
            if query_id not in results_by_id:
                raise ValueError(
                    f"No search results found for {query_id}"
                )

            result = results_by_id[query_id]

            # Extract ranked chunk IDs
            retrieved_ids = [
                chunk["chunk_id"]
                for chunk in result[method]
            ]

            # Calculate metrics for this question
            recall = recall_at_k(
                retrieved_ids, relevant_ids, k=5
            )

            rr = reciprocal_rank_at_k(
                retrieved_ids, relevant_ids, k=10
            )

            recall_scores.append(recall)
            rr_scores.append(rr)

        # Average metrics across evaluated questions
        count = len(recall_scores)

        evaluation[method] = {
            "recall_at_5": sum(recall_scores) / count if count else 0.0,
            "mrr_at_10": sum(rr_scores) / count if count else 0.0,
            "queries_evaluated": count
        }

    return evaluation

