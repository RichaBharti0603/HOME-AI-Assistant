import os
import pdfplumber
import docx
from backend.vector_store.store import save_embeddings

docs_path = "backend/documents"

def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def read_docx(path):
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def ingest_all():
    documents = []

    for root, _, files in os.walk(docs_path):
        for file in files:
            path = os.path.join(root, file)

            if file.endswith(".txt"):
                documents.append(read_txt(path))
            elif file.endswith(".pdf"):
                documents.append(read_pdf(path))
            elif file.endswith(".docx"):
                documents.append(read_docx(path))

    if not documents:
        print("[Warning] No documents found to index.")
    else:
        save_embeddings(documents)
        print(f"[Info] Indexed {len(documents)} documents.")

if __name__ == "__main__":
    ingest_all()
