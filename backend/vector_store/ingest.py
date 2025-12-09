# backend/vector_store/ingest.py
import os
from sentence_transformers import SentenceTransformer
import faiss
import pickle
from PyPDF2 import PdfReader
import docx

VECTOR_STORE_PATH = "backend/vector_store/faiss_index.pkl"
DOC_STORE_PATH = "backend/vector_store/documents.pkl"

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def load_documents(folder="documents"):
    docs = []
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if filename.endswith(".pdf"):
            reader = PdfReader(path)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
            docs.append({"text": text, "source": filename})
        elif filename.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                docs.append({"text": text, "source": filename})
        elif filename.endswith(".docx"):
            doc = docx.Document(path)
            text = "\n".join([p.text for p in doc.paragraphs])
            docs.append({"text": text, "source": filename})
    return docs

def build_vector_store(docs):
    texts = [d["text"] for d in docs]
    embeddings = embed_model.encode(texts, convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    with open(VECTOR_STORE_PATH, "wb") as f:
        pickle.dump(index, f)
    with open(DOC_STORE_PATH, "wb") as f:
        pickle.dump(docs, f)
    print(f"Indexed {len(docs)} documents.")

if __name__ == "__main__":
    docs = load_documents()
    build_vector_store(docs)
