# backend/vector_store/store.py
import os, pickle
import torch

STORE_PATH = os.path.join(os.path.dirname(__file__), "store.pkl")

def save_embeddings(texts, embeddings):
    with open(STORE_PATH, "wb") as f:
        pickle.dump({"texts": texts, "embeddings": embeddings}, f)

def load_embeddings():
    if not os.path.exists(STORE_PATH):
        return [], None
    with open(STORE_PATH, "rb") as f:
        data = pickle.load(f)
    return data["texts"], data["embeddings"]
