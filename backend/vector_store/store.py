# backend/vector_store/store.py
import faiss
import pickle
from sentence_transformers import SentenceTransformer

VECTOR_STORE_PATH = "backend/vector_store/faiss_index.pkl"
DOC_STORE_PATH = "backend/vector_store/documents.pkl"

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load vector store
with open(VECTOR_STORE_PATH, "rb") as f:
    index = pickle.load(f)
with open(DOC_STORE_PATH, "rb") as f:
    documents = pickle.load(f)

def query_store(query_embedding, top_k=3):
    """
    Return top_k relevant documents for a query embedding.
    """
    D, I = index.search(query_embedding, top_k)
    results = []
    for i in I[0]:
        if i < len(documents):
            results.append(documents[i]["text"])
    return {"documents": [results]}
