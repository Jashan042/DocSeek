from src.pdf_processor import extract_pdf, clean_text
from src.chunker import chunk_text
from src.vector_store import build_index, semantic_search

pdf = extract_pdf(
    "data/pdf/The Best Optimizer Depends on Batch Size.pdf"
)

i = 0
chunks = []
for page in (pdf):
    cleaned_text = clean_text(page['text'])

    chunked_text = chunk_text(cleaned_text)

    for text in chunked_text:
        chunk = {}
        chunk['chunk_id'] = i
        i+=1
        chunk['document'] = page['document']
        chunk['page'] = page['page']
        chunk['text'] = text
        chunks.append(chunk)





print(f"Extracted {len(pdf)} pages")

print(f"Extracted {len(pdf)} pages")
print(f"Generated {len(chunks)} chunks")

for chunk in chunks[:3]:
    print(f"\nChunk ID: {chunk['chunk_id']}")
    print(f"Document: {chunk['document']}")
    print(f"Page: {chunk['page']}")
    print(f"Text: {chunk['text'][:200]}")

assert len(chunks) > 0, "No chunks generated!"
assert all(c["text"].strip() for c in chunks), "Empty chunk found!"
assert all(len(c["text"].split()) <= 200 for c in chunks), "Chunk too large!"
assert all(c["page"] >= 1 for c in chunks), "Invalid page number!"
assert len(set(c["chunk_id"] for c in chunks)) == len(chunks), "Duplicate IDs!"

print("All tests passed!")

from src.embeddings import generate_embeddings

embeddings = generate_embeddings(chunks)

print("Total chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)

assert embeddings.shape[0] == len(chunks)
assert embeddings.shape[1] == 384

print("All embedding tests passed!")

index = build_index(embeddings)

print("Vectors stored:", index.ntotal)
print("Embedding dimensions:", index.d)

assert index.ntotal == len(chunks)
assert index.d == 384


from src.vector_store import semantic_search
from src.embeddings import model

query = "How does batch size affect model training?"

results = semantic_search(
    query=query,
    model=model,
    index=index,
    chunks=chunks,
    k=5
)

for rank, result in enumerate(results, start=1):
    print(f"\nResult {rank}")
    print(f"Document: {result['document']}")
    print(f"Page: {result['page']}")
    print(f"Similarity: {result['score']:.4f}")
    print(f"Text: {result['text'][:300]}")
