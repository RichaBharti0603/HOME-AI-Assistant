import os
import pickle
from sentence_transformers import SentenceTransformer
from backend.vector_store.store import save_embeddings

# Path to your documents folder
DOCS_FOLDER = os.path.join(os.path.dirname(__file__), "..", "documents")

# Load embedding model once
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def load_documents(folder=DOCS_FOLDER):
    """Load all text documents from folder safely."""
    documents = []
    if not os.path.exists(folder):
        print(f"[Warning] Documents folder not found: {folder}")
        return documents

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path) and filename.endswith(".txt"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read().strip()
                    if text:
                        documents.append(text)
            except Exception as e:
                print(f"[Error] Failed to read {filename}: {e}")
    return documents

def build_vector_store(documents):
    """Create embeddings and save vector store."""
    if not documents:
        print("[Warning] No documents found to index.")
        return

    embeddings = embed_model.encode(documents)
    if embeddings.size == 0:
        print("[Warning] Embeddings are empty, skipping vector store creation.")
        return

    save_embeddings(documents, embeddings)
    print(f"Indexed {len(documents)} documents.")

if __name__ == "__main__":
    docs = load_documents()
    build_vector_store(docs)
