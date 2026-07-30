from pathlib import Path
import pickle

import faiss
from sentence_transformers import SentenceTransformer


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

INDEX_FILE = DATA_DIR / "ecochem_faiss.index"
DOCUMENTS_FILE = DATA_DIR / "rag_documents.pkl"


# Load FAISS index
index = faiss.read_index(str(INDEX_FILE))

# Load documents
with open(DOCUMENTS_FILE, "rb") as f:
    documents = pickle.load(f)

# Load the same embedding model used to create the index
model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve(query, top_k=3):
    """
    Retrieve the most relevant ingredient documents
    from the EcoChemAI FAISS knowledge base.
    """

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx < 0:
            continue

        results.append({
            "score": float(score),
            "ingredient": documents[idx]["ingredient"],
            "text": documents[idx]["text"]
        })

    return results
