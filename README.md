# Multimodal RAG (offline) — FastAPI prototype

## Overview
This project ingests PDFs/DOCX/images/audio, extracts text (OCR for image/scans), creates embeddings (text + image), stores in Qdrant, and answers queries using a local LLM with retrieved context.

## Pre-reqs
- Python 3.10+
- Docker (for Qdrant)
- Download models locally (Sentence-Transformers, CLIP, Whisper)
- Install requirements: `pip install -r requirements.txt`
- Start Qdrant: `docker-compose up -d`

## Run
1. Start Qdrant: `docker-compose up -d`
2. Start app: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
3. Upload files: POST `/ingest/upload`
4. Query: POST `/query` with JSON `{"q": "your question", "top_k": 5}`

## Notes
- For production/offline distribution, include model weights in a defined model folder and change model load paths accordingly.
- LLM synthesizer is pluggable. Replace `synthesizer.generate_answer(...)` in code to call your local LLM (Ollama/llama.cpp/transformers).
