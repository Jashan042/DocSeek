from rank_bm25 import BM25Okapi
import numpy as np

def build_bm25_index(chunks: list[dict]):

    # spli the words from the chunks and lower them
    tokenised_corpus = [chunk['text'].lower().split() for chunk in chunks]

    # 
    bm25 = BM25Okapi(tokenised_corpus)

    return bm25

def bm25_search(query, bm25, chunks, k=5):
    #tokenise the query similar to the chunks
    query = query.lower().split()
    #get the scores    
    scores = bm25.get_scores(query)

    top_indices = np.argsort(scores)[::-1][:k]

    results = []

    for index in top_indices:
        # Ignore chunks with non-positive scores
        if scores[index] <= 0:
            continue

        
        result = chunks[int(index)].copy()

        # Attach the BM25 score
        result['score'] = float(scores[index])

        results.append(result)

    return results
 
    