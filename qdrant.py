from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams

# VECTOR_DIM = 384  # your embedding dimension

# # Connect to local Qdrant
# client = QdrantClient(url="http://localhost:6333")

# # Recreate collection
# client.recreate_collection(
#     collection_name="documents",
#     vectors_config=VectorParams(
#         size=VECTOR_DIM,
#         distance="Cosine"
#     )
# )

# print("Collection created successfully!")
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")  # Qdrant default port

# Scroll through points in the collection
# ...existing code...
results, _ = client.scroll(
    collection_name="documents",  # replace with your collection name
    limit=10,                     # number of points to fetch
)

for point in results:
    print("ID:", point.id)
    print("Vector length:", len(point.vector))
    print("Payload:", point.payload)
    print("---")
# ...existing code...