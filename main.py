from src.pdf_processor import extract_pdf, clean_text
from src.chunker import chunk_text

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