
from pathlib import Path
import json

from src.pdf_processor import extract_pdf, clean_text
from src.chunker import chunk_text
from src.embeddings import generate_embeddings
from src.vector_store import build_index
from src.bm25_search import build_bm25_index

from src.embeddings import model
from src.vector_store import semantic_search
from src.bm25_search import bm25_search
from src.hybrid_search import hybrid_search

from src.collect_results import collect_results

pdf_folder = Path("data/pdf")

pdf_paths = sorted(pdf_folder.glob("*.pdf"))

all_chunks = []
chunk_id = 0

for pdf_path in pdf_paths:

    print(f"\nProcessing: {pdf_path.name}")

    pages = extract_pdf(str(pdf_path))
    document_count = 0

    for page in pages:

        cleaned_text = clean_text(page["text"])
        chunked_text = chunk_text(cleaned_text)

        for text in chunked_text:

            chunk = {
                "chunk_id": chunk_id,
                "document": pdf_path.name,
                "page": page["page"],
                "text": text
            }

            all_chunks.append(chunk)
            chunk_id += 1
            document_count += 1

    print(f"Generated {document_count} chunks")

print(f"\nTotal documents: {len(pdf_paths)}")
print(f"Total chunks: {len(all_chunks)}")

# Verify unique chunk IDs
ids = [chunk["chunk_id"] for chunk in all_chunks]

assert len(ids) == len(set(ids)), "Duplicate IDs found!"
assert all(chunk["text"].strip() for chunk in all_chunks)

# Save chunk metadata
output_folder = Path("data/evaluation")
output_folder.mkdir(parents=True, exist_ok=True)

with open(output_folder / "chunks.json", "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=2, ensure_ascii=False)

print("All chunks saved successfully!")


# Generate embeddings for all documents
embeddings = generate_embeddings(all_chunks)

# Build the combined FAISS index
index = build_index(embeddings)

# Build the combined BM25 index
bm25 = build_bm25_index(all_chunks)

print("Embedding shape:", embeddings.shape)
print("FAISS vectors:", index.ntotal)
print("BM25 documents:", bm25.corpus_size)

assert index.ntotal == len(all_chunks)
assert bm25.corpus_size == len(all_chunks)



with open("data/evaluation/queries.json", encoding="utf-8") as f:
    queries = json.load(f)

results = collect_results(
    queries, model, index, bm25, all_chunks
)

with open("data/evaluation/search_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("Evaluation results saved!")



import json
from src.evaluation import evaluate_search

with open("data/evaluation/queries.json", "r", encoding="utf-8") as f:
    queries = json.load(f)

with open("data/evaluation/search_results.json", "r", encoding="utf-8") as f:
    search_results = json.load(f)

results = evaluate_search(queries, search_results)

print(f"{'Method':<15} {'Recall@5':<12} {'MRR@10':<12} {'Queries'}")
print("-" * 50)

for method, metrics in results.items():
    print(
        f"{method:<15} "
        f"{metrics['recall_at_5']:<12.4f} "
        f"{metrics['mrr_at_10']:<12.4f} "
        f"{metrics['queries_evaluated']}"
    )
