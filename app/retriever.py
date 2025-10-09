# app/retriever.py
from .embeddings import embed_text
from .indexer import search

def retrieve(query: str, top_k: int = 5):
    qv = embed_text(query)
    results = search(qv, top_k=top_k)
    return results
