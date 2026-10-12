from src.pdf_processor import extract_pdf, clean_text, chunk_text

pdf = extract_pdf(
    "data/pdf/The Best Optimizer Depends on Batch Size.pdf"
)

print(f"Extracted {len(pdf)} pages")

print(pdf[0]["text"][:200])