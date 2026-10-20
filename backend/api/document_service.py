from src.chunker import chunk_text
from src.pdf_processor import extract_pdf, clean_text
from pathlib import Path

def process_document(pdf_path: str, start_chunk_id: int) -> list[dict]:
    all_chunks = []
    chunk_id = start_chunk_id

    pdf_path = Path(pdf_path)

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
    return all_chunks

if __name__ == "__main__":
    chunks = process_document("data/pdf/The Best Optimizer Depends on Batch Size.pdf", start_chunk_id=100)

    print("Chunks generated:", len(chunks))
    print("First chunk:", chunks[0] if chunks else "No chunks")