import math
from typing import List

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    tokens = text.split()
    if not tokens:
        return []
    chunks = []
    i = 0
    n = len(tokens)
    while i < n:
        j = min(i + chunk_size, n)
        chunk = " ".join(tokens[i:j])
        chunks.append(chunk)
        if j == n:
            break
        i = j - overlap
    return chunks
