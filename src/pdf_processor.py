import pymupdf
import re
from pathlib import Path

def extract_pdf(pdf_path: str) -> list[dict]:
    """
    Extract text from every page of a PDF.

    Returns:
        List of dictionaries containing:
        - document: filename
        - page: page number (starting at 1)
        - text: extracted page text
    """
    pages = []
    # open the pdf
    with pymupdf.open(pdf_path) as doc:

        #print(f'The title of the pdf is : {doc.metadata['title']}')
        #check for 0 pages
        if (doc.page_count == 0): return []

        # get the title, page number and text content
        for i, page in enumerate(doc):
            content = {}
            content['document'] = Path(pdf_path).name
            content['page'] = i+1
            content['text'] = page.get_text()
            pages.append(content)

    return pages

def clean_text(text:str) -> str:
    res = text.replace("\n", " ")
    res = re.sub(' +', ' ', res)
    
    res = re.sub(r"\s+", " ", text)
    return res.strip()


def chunk_text(text: str, chunk_size: int = 200, overlap: int = 40) -> list[str]:
    """
    Breaks the text into smaller chunks with overlap

    Returns:
        list of chunks
    """

    
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Invalid chunk size or overlap")
    
    result = []

    if not text.split(): return []

    step = chunk_size - overlap

    words = text.split()
   

    start = 0
    end = chunk_size


    while start < len(words):
        chunk = words[start:end]
        result.append(" ".join(chunk))

        if end >= len(words):
            break

        start += step
        end += step
 


    return result

    






if __name__ == "__main__":

    text = (
        "The quick brown fox jumps over the lazy dog "
        "near the river where the birds are singing."
    )

    chunks = chunk_text(text, chunk_size=5, overlap=2)

    print(f"Original text: {text}")
    print(f"Total words: {len(text.split())}")
    print(f"Number of chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks, start=1):
        print(f"\nChunk {i}:")
        print(chunk)
        print(f"Word count: {len(chunk.split())}")


