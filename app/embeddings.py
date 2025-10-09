# app/embeddings.py
import io
import numpy as np
from .config import TEXT_EMBED_MODEL, IMAGE_CLIP_MODEL, VECTOR_DIM
import threading

_text_model = None
_text_model_lock = threading.Lock()
_clip = None
_clip_preprocess = None
_clip_device = None
_clip_lock = threading.Lock()

def get_text_model():
    global _text_model
    if _text_model is None:
        with _text_model_lock:
            if _text_model is None:
                from sentence_transformers import SentenceTransformer
                _text_model = SentenceTransformer(TEXT_EMBED_MODEL)
    return _text_model

def get_clip_model_and_preprocess():
    global _clip, _clip_preprocess, _clip_device
    if _clip is None:
        with _clip_lock:
            if _clip is None:
                import open_clip
                import torch
                model, _, preprocess = open_clip.create_model_and_transforms(
                    IMAGE_CLIP_MODEL, pretrained='openai'
                )
                device = "cuda" if torch.cuda.is_available() else "cpu"
                model.to(device)
                _clip = model
                _clip_preprocess = preprocess
                _clip_device = device
    return _clip, _clip_preprocess, _clip_device

def embed_text(text: str):
    model = get_text_model()
    emb = model.encode([text], convert_to_numpy=True)[0].astype(np.float32)
    # pad or truncate to VECTOR_DIM
    if len(emb) < VECTOR_DIM:
        pad = np.zeros(VECTOR_DIM - len(emb), dtype=np.float32)
        emb = np.concatenate([emb, pad])
    elif len(emb) > VECTOR_DIM:
        emb = emb[:VECTOR_DIM]
    # convert to plain list for Qdrant
    return emb.tolist()

def embed_image_bytes(img_bytes: bytes):
    clip_model, preprocess, device = get_clip_model_and_preprocess()
    from PIL import Image
    import torch
    image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    inp = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = clip_model.encode_image(inp)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        emb = image_features.cpu().numpy()[0].astype(np.float32)
    # pad/truncate to VECTOR_DIM
    if len(emb) < VECTOR_DIM:
        pad = np.zeros(VECTOR_DIM - len(emb), dtype=np.float32)
        emb = np.concatenate([emb, pad])
    elif len(emb) > VECTOR_DIM:
        emb = emb[:VECTOR_DIM]
    # convert to plain list for Qdrant
    return emb.tolist()
