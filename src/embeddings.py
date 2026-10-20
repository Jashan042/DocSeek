
from sentence_transformers import SentenceTransformer
from sentence_transformers import util

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    device="cpu"
)

def generate_embeddings(chunks: list[dict]):
    """
    Create embedding for the PDF chunks
    Returns:
        embedding vector with (Chunks, 386) dimensions
    """

    texts = [chunk['text'] for chunk in chunks]

    embeddings = model.encode(
        texts,
        batch_size=16,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings





if __name__ == "__main__":
    sentences = [
        "Deep learning models require training data.",
        "Neural networks learn patterns from datasets.",
        "I enjoy playing football on weekends."
    ]

    embeddings = model.encode(sentences)

    print("Embedding shape:", embeddings.shape)
    print("First 10 values:", embeddings[0][:10])

    similarity = util.cos_sim(embeddings, embeddings)

    print(similarity)
