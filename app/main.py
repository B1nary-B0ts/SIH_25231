# app/main.py
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from .ingest import process_upload
from .retriever import retrieve
from .synthesizer import synthesize
from .models import IngestResponse, QueryRequest
from fastapi.staticfiles import StaticFiles
import os
app = FastAPI(title="Multimodal RAG (Offline Prototype)")

# Make sure STORAGE_DIR exists
STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

# Mount storage folder
app.mount("/storage", StaticFiles(directory=STORAGE_DIR), name="storage")


@app.post("/ingest/upload", response_model=IngestResponse)
async def upload_endpoint(file: UploadFile = File(...)):
    try:
        res = process_upload(file)
        return {"doc_id": res["doc_id"], "filename": res["filename"], "status": "indexed", "chunks_indexed": res["chunks_indexed"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/query")
async def query_endpoint(qr: QueryRequest):
    try:
        hits = retrieve(qr.q, top_k=qr.top_k)
        synth = synthesize(qr.q, hits)
        return {"query": qr.q, "results": hits, "synthesis": synth}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"status":"ok"}
