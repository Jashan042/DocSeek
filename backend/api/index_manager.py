import json
import faiss
from pathlib import Path
from django.conf import settings
from .document_service import process_document
from src.embeddings import generate_embeddings
from src.vector_store import build_index

INDEX_DIR = settings.PROJECT_ROOT / "data" / "indexes"
INDEX_DIR.mkdir(parents=True, exist_ok=True)

FAISS_PATH = INDEX_DIR / "faiss.index"
CHUNKS_PATH = INDEX_DIR / "chunks.json"

def save_indexes(index, chunks):
    assert index.ntotal == len(chunks), "FAISS index and chunks count mismatch!"
    #save the FAISS indexing
    faiss.write_index(index, str(FAISS_PATH))
    # save the chunk metadata
    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)


def load_indexes():
    # no index saved yet
    if (not FAISS_PATH.exists()) and (not CHUNKS_PATH.exists()):
        return (None, [])
    # missing state
    if (not FAISS_PATH.exists()) or (not CHUNKS_PATH.exists()):
            raise FileNotFoundError("FAISS index or chunk metadata is missing.")
    index = faiss.read_index(str(FAISS_PATH))
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    # validating index consistency
    if index.ntotal != len(chunks):
        raise ValueError("FAISS index and chunk metadata count mismatch!")

    return index, chunks


def add_document(pdf_path: str):

    index, chunks = load_indexes()
    start_chunk_id = len(chunks)

    new_chunks = process_document(pdf_path, start_chunk_id)

    if not new_chunks:
        return 0

    new_embeddings = generate_embeddings(new_chunks)

    if index is None:
        index = build_index(new_embeddings)
    else:
        index.add(new_embeddings.astype('float32'))

    chunks.extend(new_chunks)

    save_indexes(index, chunks)

    return len(new_chunks)