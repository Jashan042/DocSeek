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




    







