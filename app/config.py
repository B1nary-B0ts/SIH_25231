# app/config.py
import os

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "documents")
STORAGE_DIR = os.getenv("UPLOAD_DIR", "storage")
VECTOR_DIM = int(os.getenv("VECTOR_DIM", "512"))  # unified vector dimension (images -> 512; text padded if needed)
# TEXT_EMBED_MODEL = os.getenv("TEXT_EMBED_MODEL", "all-MiniLM-L6-v2")
TEXT_EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
IMAGE_CLIP_MODEL = os.getenv("IMAGE_CLIP_MODEL", "ViT-B-32")  # for open_clip usage
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "150"))  # words per chunk
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
# app/config.py
# QDRANT_HOST = "localhost"
# QDRANT_PORT = 6333
# COLLECTION_NAME = "documents"
# VECTOR_DIM = 384  # make sure matches your embedding model output
# CHUNK_SIZE = 500
# CHUNK_OVERLAP = 50
# TEXT_EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# IMAGE_CLIP_MODEL = "ViT-B-32"  # open_clip model name
# STORAGE_DIR = "storage"