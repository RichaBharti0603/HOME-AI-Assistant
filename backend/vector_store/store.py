# backend/vector_store/store.py
import os
import pickle
import numpy as np
import torch

EMBED_FILE = os.path.join(os.path.dirname(__file__), "..", "embeddings", "store.pkl")

def save_embeddings(documents, embeddings):
    os.makedirs(os.path.dirname(EMBED_FILE), exist_ok=True)
    # convert to numpy for storage
    np_embeddings = embeddings if isinstance(embeddings, np.ndarray) else np.array(embeddings)
    with open(EMBED_FILE, "wb") as f:
        pickle.dump({"documents": documents, "embeddings": np_embeddings}, f)

def load_embeddings():
    if not os.path.exists(EMBED_FILE):
        return [], np.array([])
    with open(EMBED_FILE, "rb") as f:
        store = pickle.load(f)
    docs = store.get("documents", [])
    embs = store.get("embeddings", np.array([]))
    # convert to torch tensor for cosine similarity with SentenceTransformers util
    try:
        import torch
        embs_t = torch.from_numpy(np.array(embs))
    except Exception:
        embs_t = embs
    return docs, embs_t
