import io
import os
import tempfile
from typing import Dict
from PIL import Image
import fitz  # PyMuPDF
from docx import Document

# OCR backends
try:
    from paddleocr import PaddleOCR
    _paddle = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
except Exception:
    _paddle = None

try:
    import easyocr
    _easy_reader = easyocr.Reader(['en'], gpu=False)
except Exception:
    _easy_reader = None

try:
    import pytesseract
    _tesseract = pytesseract
except Exception:
    _tesseract = None

# Whisper
try:
    import whisper
    _whisper_model = whisper.load_model("small")
except Exception:
    _whisper_model = None

# TrOCR (handwriting)
try:
    from transformers import TrOCRProcessor, VisionEncoderDecoderModel
    _trocr_processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
    _trocr_model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')
except Exception:
    _trocr_processor = None
    _trocr_model = None


# -------------------------------
# PDF Extraction
# -------------------------------
def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> Dict:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages = []
    full = []
    for i in range(len(doc)):
        page = doc.load_page(i)
        text = page.get_text().strip()
        if not text:
            pix = page.get_pixmap(dpi=200)
            img_bytes = pix.tobytes()
            text = ocr_image_bytes(img_bytes)
        pages.append({"page": i+1, "text": text, "char_count": len(text)})
        full.append(text)
    doc.close()
    return {"pages": pages, "text": "\n\n".join(full)}


# -------------------------------
# DOCX Extraction
# -------------------------------
def extract_text_from_docx_bytes(docx_bytes: bytes) -> Dict:
    doc = Document(io.BytesIO(docx_bytes))
    paras = [p.text for p in doc.paragraphs if p.text.strip()]
    text = "\n\n".join(paras)
    return {"pages":[{"page":1, "text":text, "char_count":len(text)}], "text": text}


# -------------------------------
# OCR Utilities
# -------------------------------
def ocr_image_bytes(img_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
        tmp.write(img_bytes)
        tmp.flush()
        return ocr_image_file(tmp.name)

def ocr_image_file(path: str) -> str:
    text = ""
    if _paddle:
        try:
            res = _paddle.ocr(path, cls=True)
            lines = [line[1][0] for block in res for line in block]
            text = " ".join(lines).strip()
            if text:
                return text
        except Exception:
            pass
    if _easy_reader:
        try:
            res = _easy_reader.readtext(path)
            lines = [t for (_, t, _) in res]
            text = " ".join(lines).strip()
            if text:
                return text
        except Exception:
            pass
    if _tesseract:
        try:
            img = Image.open(path)
            text = _tesseract.image_to_string(img).strip()
            if text:
                return text
        except Exception:
            pass
    if _trocr_processor and _trocr_model:
        try:
            img = Image.open(path).convert("RGB")
            pixel_values = _trocr_processor(images=img, return_tensors="pt").pixel_values
            generated_ids = _trocr_model.generate(pixel_values)
            generated_text = _trocr_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            if generated_text.strip():
                return generated_text.strip()
        except Exception:
            pass
    return text

def extract_text_from_image_bytes(img_bytes: bytes) -> Dict:
    text = ocr_image_bytes(img_bytes)
    return {"pages":[{"page":1, "text":text, "char_count": len(text)}], "text": text}


# -------------------------------
# Audio Transcription (WAV ONLY)
# -------------------------------
def transcribe_audio_bytes(audio_bytes: bytes, whisper_model) -> dict:
    """
    Directly transcribe WAV audio bytes using Whisper.
    No ffmpeg / pydub needed.
    """
    if whisper_model is None:
        raise RuntimeError("No ASR model available.")

    tmp_path = None
    try:
        # Save WAV file temporarily
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp.flush()
            tmp_path = tmp.name
            print(f"[DEBUG] Temp WAV path: {tmp_path}, size={os.path.getsize(tmp_path)} bytes")

        # Whisper transcription
        res = whisper_model.transcribe(tmp_path, task="translate")
        print(f"[DEBUG] Whisper transcription result: {res}")
        return {
            "text": res.get("text", ""),
            "segments": res.get("segments", []),
            "detected_language": res.get("language", "unknown")
        }
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
