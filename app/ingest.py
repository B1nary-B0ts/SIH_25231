# app/ingest.py
import os
import whisper
from fastapi import UploadFile
from pydub.utils import which

from .utils import save_upload, chunk_text_by_words
from .extractors import (
    extract_text_from_pdf_bytes,
    extract_text_from_docx_bytes,
    extract_text_from_image_bytes,
    transcribe_audio_bytes
)
from .embeddings import embed_text, embed_image_bytes
from .indexer import upsert_documents
from .config import CHUNK_SIZE, CHUNK_OVERLAP, VECTOR_DIM

# -------------------------------
# Load Whisper model once globally
# -------------------------------
_whisper_model = whisper.load_model("small")  # You can change "small" → "medium", "large", etc.

def process_upload(
    file: UploadFile
    # whisper_model=_whisper_model,
    # ffmpeg_path="C:/ffmpeg/bin/ffmpeg.exe",
    # ffprobe_path="C:/ffmpeg/bin/ffprobe.exe"
):
    """
    Handles uploaded file ingestion:
    1. Save file
    2. Extract text (PDF, DOCX, Image, Audio)
    3. Chunk text
    4. Embed text + images
    5. Upsert into Qdrant
    """
    whisper_model = _whisper_model
    # ffmpeg_path = ffmpeg_path or which("ffmpeg")
    # ffprobe_path = ffprobe_path or which("ffprobe")

    try:
        # -------------------------------
        # 1️⃣ Save uploaded file
        # -------------------------------
        path, doc_id = save_upload(file)
        with open(path, "rb") as f:
            file_bytes = f.read()

        mimetype = (file.content_type or "").lower()
        ext = os.path.splitext(path)[1].lower()
        print(f"[DEBUG] Received file: {file.filename}, mimetype={mimetype}, ext={ext}")

        # -------------------------------
        # 2️⃣ Extract text based on file type
        # -------------------------------
        text = ""
        if "application/pdf" in mimetype or ext == ".pdf":
            extracted = extract_text_from_pdf_bytes(file_bytes)
            text = extracted.get("text", "")
        elif "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in mimetype or ext in (".docx", ".doc"):
            extracted = extract_text_from_docx_bytes(file_bytes)
            text = extracted.get("text", "")
        elif mimetype.startswith("image") or ext in (".png", ".jpg", ".jpeg"):
            extracted = extract_text_from_image_bytes(file_bytes)
            text = extracted.get("text", "")
        elif mimetype.startswith("audio") or ext in (".wav", ".mp3", ".m4a"):
            trans = transcribe_audio_bytes(file_bytes, whisper_model)
            extracted = {
                "pages": [{"page": 1, "text": trans["text"], "char_count": len(trans["text"])}],
                "text": trans["text"]
            }
            text = trans["text"]
        else:
            raise ValueError(f"Unsupported file type: mimetype={mimetype}, ext={ext}")

        if not text.strip():
            raise ValueError("No text extracted from the uploaded file.")

        print(f"[DEBUG] Extracted text length: {len(text)}")

        # -------------------------------
        # 3️⃣ Chunk text
        # -------------------------------
        chunks = chunk_text_by_words(text, CHUNK_SIZE, CHUNK_OVERLAP)
        print(f"[DEBUG] Number of text chunks: {len(chunks)}")

        docs_to_index = []

        # -------------------------------
        # 4️⃣ Embed text chunks
        # -------------------------------
        for idx, chunk in enumerate(chunks):
            embedding = embed_text(chunk)
            if not embedding:
                print(f"[WARN] Empty embedding for chunk {idx}")
                continue

            docs_to_index.append({
                "id": f"{doc_id}_{idx}",
                "embedding": embedding,
                "payload": {
                    "text": chunk,
                    "filename": file.filename,
                    "doc_id": doc_id,
                    "chunk_index": idx,
                    "source_type": "text"
                }
            })

        # -------------------------------
        # 5️⃣ Embed image globally (if applicable)
        # -------------------------------
        if mimetype.startswith("image") or ext in (".png", ".jpg", ".jpeg"):
            try:
                img_embedding = embed_image_bytes(file_bytes)
                if img_embedding:
                    docs_to_index.append({
                        "id": f"{doc_id}_image",
                        "embedding": img_embedding,
                        "payload": {
                            "text": text,
                            "filename": file.filename,
                            "doc_id": doc_id,
                            "chunk_index": "image",
                            "source_type": "image"
                        }
                    })
            except Exception as e:
                print(f"[WARN] Image embedding failed: {e}")

        if not docs_to_index:
            raise RuntimeError("No chunks or images to index!")

        # -------------------------------
        # 6️⃣ Upsert to Qdrant
        # -------------------------------
        print(f"[DEBUG] Preparing to upsert {len(docs_to_index)} documents to Qdrant")
        upsert_documents(docs_to_index, vector_dim=VECTOR_DIM)
        print(f"[DEBUG] Finished upserting documents")

        return {
            "doc_id": doc_id,
            "filename": file.filename,
            "chunks_indexed": len(docs_to_index)
        }

    except Exception as e:
        print(f"[ERROR] process_upload failed: {e}")
        raise
