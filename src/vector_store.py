import faiss
from sentence_transformers import SentenceTransformer
from sentence_transformers import util

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    device="cpu"
)


def build_index(embeddings):
    embeddings = embeddings.astype("float32")
    # get the vector dimension
    dimension = embeddings.shape[1]
    # inner product
    index = faiss.IndexFlatIP(dimension)
    #storing all chunk emdddings
    index.add(embeddings)
    return index

def semantic_search(query, model, index, chunks, k=5):
    results = []
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")

    k = min(k, index.ntotal)

    scores, indices = index.search(query_embedding, k)

    for i, loc in enumerate(indices[0]):
        res = chunks[loc].copy()
        res['score'] = float(scores[0][i])

        results.append(res)

    return results
        


