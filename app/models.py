# app/models.py
from pydantic import BaseModel
from typing import Optional, List, Dict

class IngestResponse(BaseModel):
    doc_id: str
    filename: str
    status: str
    chunks_indexed: int

class QueryRequest(BaseModel):
    q: str
    top_k: Optional[int] = 5

class Hit(BaseModel):
    id: str
    score: float
    payload: Dict
