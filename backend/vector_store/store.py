import os
import pickle
import numpy as np

EMBEDDINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "embeddings", "store.pkl")

def save_embeddings(documents, embeddings):
    """Save embeddings safely."""
    os.makedirs(os.path.dirname(EMBEDDINGS_FILE), exist_ok=True)
    with open(EMBEDDINGS_FILE, "wb") as f:
        pickle.dump({"documents": documents, "embeddings": embeddings}, f)
    print(f"[Info] Saved embeddings for {len(documents)} documents.")

def load_embeddings():
    """Load embeddings safely."""
    if not os.path.exists(EMBEDDINGS_FILE):
        print(f"[Warning] Embeddings file not found: {EMBEDDINGS_FILE}")
        return {"documents": [], "embeddings": np.array([])}
    with open(EMBEDDINGS_FILE, "rb") as f:
        return pickle.load(f)

def query_store(query_embedding, top_k=3):
    """Query vector store safely."""
    store = load_embeddings()
    documents = store.get("documents", [])
    embeddings = store.get("embeddings", np.array([]))

    if embeddings.size == 0 or len(documents) == 0:
        return {"documents": []}

    # Compute cosine similarity
    similarity = embeddings @ query_embedding.T
    top_idx = np.argsort(-similarity.flatten())[:top_k]
    top_docs = [documents[i] for i in top_idx if i < len(documents)]
    return {"documents": [top_docs]}
