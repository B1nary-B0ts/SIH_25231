# app/utils.py
import os
import uuid
from typing import Tuple
from fastapi import UploadFile
from .config import STORAGE_DIR, CHUNK_SIZE, CHUNK_OVERLAP

os.makedirs(STORAGE_DIR, exist_ok=True)

def save_upload(file: UploadFile) -> Tuple[str, str]:
    ext = os.path.splitext(file.filename)[1]
    doc_id = str(uuid.uuid4())
    out_path = os.path.join(STORAGE_DIR, f"{doc_id}{ext}")
    with open(out_path, "wb") as f:
        f.write(file.file.read())
    return out_path, doc_id

def chunk_text_by_words(text: str, chunk_size:int=CHUNK_SIZE, overlap:int=CHUNK_OVERLAP):
    if not text:
        return []
    words = text.split()
    chunks = []
    i = 0
    n = len(words)
    while i < n:
        j = min(i + chunk_size, n)
        chunk = " ".join(words[i:j])
        chunks.append(chunk)
        if j == n:
            break
        i = j - overlap
    return chunks
