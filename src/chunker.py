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