from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from qdrant_client.http.models import PointStruct
import os
import uuid

from shapely import points

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "multimodal_docs")
client = QdrantClient(url=QDRANT_URL.split("://")[-1] if "://" in QDRANT_URL else QDRANT_URL, prefer_grpc=False)

# create collection if not exists
def ensure_collection(dim: int = 384):
    try:
        client.get_collection(collection_name=COLLECTION_NAME)
    except Exception:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=rest.VectorParams(size=dim, distance=rest.Distance.COSINE)
        )

def upsert_documents(items: list, vector_dim: int):
    """
    items: list of dicts with structure:
    {
        'id': str,
        'embedding': list[float],
        'payload': dict  # contains 'text' key
    }
    """
    import uuid
    from qdrant_client.http.models import PointStruct
    points = []
    for idx, it in enumerate(items):
        # Ensure valid UUID for point ID
        pid = str(uuid.uuid5(uuid.UUID(it.get("doc_id")), str(idx))) if "doc_id" in it else str(uuid.uuid4())
        embedding = it["embedding"]
        if hasattr(embedding, "tolist"):
            embedding = embedding.tolist()
        payload = it.get("payload", {})
        if "text" not in payload:
            payload["text"] = ""
        points.append(PointStruct(
            id=pid,
            vector=embedding,
            payload=payload
        ))


    print(f"[DEBUG] Upserting {len(points)} points to Qdrant")
    client.upsert(collection_name=COLLECTION_NAME, points=points)

def search(query_vector, top_k=5):
    res = client.search(collection_name=COLLECTION_NAME, query_vector=query_vector, limit=top_k)
    out = []
    for hit in res:
        out.append({
            "id": hit.id,
            "score": hit.score,
            "text": hit.payload.get("text", ""),
            "metadata": hit.payload.get("metadata", {})
        })
    return out
