# from logging import Filter
# from qdrant_client import QdrantClient
# from qdrant_client.models import VectorParams
# from qdrant_client import QdrantClient
# from qdrant_client.http.models import Filter, PointIdsList, MatchAll
# # VECTOR_DIM = 384  # your embedding dimension

# # # Connect to local Qdrant
# # client = QdrantClient(url="http://localhost:6333")

# # # Recreate collection
# # client.recreate_collection(
# #     collection_name="documents",
# #     vectors_config=VectorParams(
# #         size=VECTOR_DIM,
# #         distance="Cosine"
# #     )
# # )

# # print("Collection created successfully!")
# from qdrant_client import QdrantClient

# client = QdrantClient(url="http://localhost:6333")  # Qdrant default port

# # Scroll through points in the collection
# # ...existing code...
# # results, _ = client.scroll(
# #     collection_name="documents",  # replace with your collection name
# #     limit=10,                     # number of points to fetch
# # )

# # for point in results:
# #     print("ID:", point.id)
# #     print("Vector length:", len(point.vector))
# #     print("Payload:", point.payload)
# #     print("---")
# # # ...existing code...


# # Delete all points in the collection
# client.delete(
#     collection_name="documents",
#     points_selector={"filter": {}}  # empty filter matches all points
# )

# print("All points deleted from the collection.")



from qdrant_client import QdrantClient, models

# Initialize the client
client = QdrantClient(host="localhost", port=6333) # Replace with your Qdrant instance details

collection_name = "documents" # Replace with the name of your collection

# 1. Delete the collection
print(f"Deleting collection: {collection_name}")
client.delete_collection(collection_name=collection_name)
print(f"Collection '{collection_name}' deleted.")

# 2. Recreate the collection (with the same configuration if desired)
print(f"Recreating collection: {collection_name}")
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(size=512, distance=models.Distance.COSINE), # Adjust size and distance as per your original collection
    # Add other configuration parameters if needed, e.g., on_disk_payload=True
)
print(f"Collection '{collection_name}' recreated.")