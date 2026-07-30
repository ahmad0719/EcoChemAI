
from pathlib import Path
import json
import pickle

import faiss
from sentence_transformers import SentenceTransformer


# -----------------------------
# Project paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

input_file = DATA_DIR / "rag_documents.json"
index_file = DATA_DIR / "ecochem_faiss.index"
documents_file = DATA_DIR / "rag_documents.pkl"


# -----------------------------
# Load RAG documents
# -----------------------------
with open(input_file, "r", encoding="utf-8") as f:
	documents = json.load(f)

texts = [doc["text"] for doc in documents]

print(f"Loaded {len(texts)} documents.")


# -----------------------------
# Load embedding model
# -----------------------------
print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded.")


# -----------------------------
# Create embeddings
# -----------------------------
print("Creating embeddings...")

embeddings = model.encode(
	texts,
	show_progress_bar=True,
	normalize_embeddings=True
)

print(f"Created embeddings with shape: {embeddings.shape}")


# -----------------------------
# Create FAISS index
# -----------------------------
dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(embeddings)

print(f"FAISS index contains {index.ntotal} vectors.")


# -----------------------------
# Save FAISS index
# -----------------------------
faiss.write_index(index, str(index_file))


# -----------------------------
# Save documents
# -----------------------------
with open(documents_file, "wb") as f:
	pickle.dump(documents, f)


print("\n--------------------------------")
print("Embedding process completed!")
print(f"FAISS index: {index_file}")
print(f"Documents: {documents_file}")
print("--------------------------------")
