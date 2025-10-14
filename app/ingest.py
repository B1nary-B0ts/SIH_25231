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
            print(f"extracted: {text}")
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
        # chunks = chunk_text_by_words(text, CHUNK_SIZE, CHUNK_OVERLAP)
        # print(f"[DEBUG] Number of text chunks: {len(chunks)}")

        # docs_to_index = []

        # # -------------------------------
        # # 4️⃣ Embed text chunks
        # # -------------------------------
        # for idx, chunk in enumerate(chunks):
        #     embedding = embed_text(chunk)
        #     if not embedding:
        #         print(f"[WARN] Empty embedding for chunk {idx}")
        #         continue

        #     docs_to_index.append({
        #         "id": f"{doc_id}_{idx}",
        #         "embedding": embedding,
        #         "payload": {
        #             "text": chunk,
        #             "filename": file.filename,
        #             "doc_id": doc_id,
        #             "chunk_index": idx,
        #             "source_type": "text"
        #         }
        #     })

#FOR PAGE NUMBERS
        # chunks = chunk_text_by_words(text, CHUNK_SIZE, CHUNK_OVERLAP)
        # print(f"[DEBUG] Number of text chunks: {len(chunks)}")

        # docs_to_index = []

        # # -------------------------------
        # # 4️⃣ Embed text chunks
        # # -------------------------------
        # line_counter = 0  # global line counter for the document
        # for idx, chunk in enumerate(chunks):
        #     embedding = embed_text(chunk)
        #     if not embedding:
        #         print(f"[WARN] Empty embedding for chunk {idx}")
        #         continue
        #     # Determine page and line range for this chunk
        #     chunk_start = line_counter
        #     chunk_lines = chunk.split(". ")  # approximate: each sentence as a line
        #     chunk_end = chunk_start + len(chunk_lines)

        #     # Collect page and line info from pages data
        #     # You can enhance this to find exact pages if needed
        #     pages = extracted.get("pages", [])
        #     pages_covered = []
        #     for page in pages:
        #         page_lines = [line['text'] for line in page['lines']]
        #         if any(sentence in page_lines for sentence in chunk_lines):
        #             pages_covered.append(page['page'])

        #     docs_to_index.append({
        #         "id": f"{doc_id}_{idx}",
        #         "embedding": embedding,
        #         "payload": {
        #             "text": chunk,
        #             "filename": file.filename,
        #             "doc_id": doc_id,
        #             "chunk_index": idx,
        #             "source_type": "text",
        #             "page_range": f"{pages_covered[0]}-{pages_covered[-1]}" if pages_covered else None,
        #             "line_range": f"{chunk_start+1}-{chunk_end}",
        #             "page_number": pages_covered[0] if pages_covered else None
        #         }
        #     })
        #     line_counter = chunk_end  # update line counter for next chunk

        # -------------------------------
        # 5️⃣ Embed image globally (if applicable)
        # -------------------------------

#AUDIO TIMESTAMPS
        # chunks = chunk_text_by_words(text, CHUNK_SIZE, CHUNK_OVERLAP)
        # docs_to_index = []

        # line_counter = 0

        # for idx, chunk in enumerate(chunks):
        #     embedding = embed_text(chunk)
        #     if not embedding:
        #         continue

        #     chunk_lines = chunk.split(". ")  # approximate sentence splitting
        #     chunk_end = line_counter + len(chunk_lines)

        #     pages = extracted.get("pages", [])
        #     pages_covered = []
        #     for page in pages:
        #         page_lines = [line['text'] for line in page.get("lines", [])]
        #         if any(sentence in page_lines for sentence in chunk_lines):
        #             pages_covered.append(page['page'])

        #     # ---- AUDIO TIMESTAMPS ----
        #     audio_start, audio_end = None, None
        #     if "segments" in extracted:  # Only audio
        #         for seg in extracted["segments"]:
        #             if any(line in seg["text"] for line in chunk_lines):
        #                 if audio_start is None or seg["start"] < audio_start:
        #                     audio_start = seg["start"]
        #                 if audio_end is None or seg["end"] > audio_end:
        #                     audio_end = seg["end"]


        #     docs_to_index.append({
        #         "id": f"{doc_id}_{idx}",
        #         "embedding": embedding,
        #         "payload": {
        #             "text": chunk,
        #             "filename": file.filename,
        #             "doc_id": doc_id,
        #             "chunk_index": idx,
        #             "source_type": "audio" if "segments" in extracted else "text",
        #             "page_range": f"{pages_covered[0]}-{pages_covered[-1]}" if pages_covered else None,
        #             "line_range": f"{line_counter+1}-{chunk_end}",
        #             "page_number": pages_covered[0] if pages_covered else None,
        #             "audio_start": audio_start,
        #             "audio_end": audio_end
        #         }
        #     })
        #     line_counter = chunk_end

#final 


        chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
        docs_to_index = []

        line_counter = 0
        pages = extracted.get("pages", [])

# Build a global line->page map for text documents
        line_to_page = {}
        for page in pages:
            for line in page.get("lines", []):
                line_num = line["line_number"]
                line_to_page[line_num] = page["page"]

        for idx, chunk in enumerate(chunks):
            embedding = embed_text(chunk)
            if not embedding:
                continue

            chunk_lines = chunk.split(". ")  # approximate sentence splitting
            chunk_start_line = line_counter + 1
            chunk_end_line = line_counter + len(chunk_lines)

            # Determine pages covered by line numbers
            pages_covered = sorted({line_to_page.get(ln) for ln in range(chunk_start_line, chunk_end_line+1) if line_to_page.get(ln)})

            # ---- AUDIO TIMESTAMPS ----
            audio_start, audio_end = None, None
            if "segments" in extracted:  # Only audio
                # Find segments overlapping with chunk
                for seg in extracted["segments"]:
                    seg_text = seg["text"].strip()
                    # naive: if any chunk line appears in segment
                    if any(line.strip() in seg_text for line in chunk_lines):
                        if audio_start is None or seg["start"] < audio_start:
                            audio_start = seg["start"]
                        if audio_end is None or seg["end"] > audio_end:
                            audio_end = seg["end"]

            docs_to_index.append({
                "id": f"{doc_id}_{idx}",
                "embedding": embedding,
                "payload": {
                    "text": chunk,
                    "filename": file.filename,
                    "doc_id": doc_id,
                    "chunk_index": idx,
                    "source_type": "audio" if "segments" in extracted else "text",
                    "page_range": f"{pages_covered[0]}-{pages_covered[-1]}" if pages_covered else None,
                    "line_range": f"{chunk_start_line}-{chunk_end_line}",
                    "page_number": pages_covered[0] if pages_covered else None,
                    "audio_start": audio_start,
                    "audio_end": audio_end
                }
            })
            line_counter = chunk_end_line


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
