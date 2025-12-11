import os
from sentence_transformers import SentenceTransformer
import torch
from backend.vector_store.store import save_embeddings

# Path to documents
DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "documents")

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

def load_all_texts(docs_dir):
    texts = []
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith((".txt", ".md")):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    texts.append(f.read())
    return texts

def main():
    texts = load_all_texts(DOCS_DIR)
    if not texts:
        print("No documents found to embed.")
        return

    # Compute embeddings
    embeddings = model.encode(texts, convert_to_tensor=True)

    # Save
    save_embeddings(texts, embeddings)
    print(f"Saved {len(texts)} documents and embeddings.")

if __name__ == "__main__":
    main()
