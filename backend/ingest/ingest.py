import os
from PyPDF2 import PdfReader

def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def ingest_file(filepath):
    ext = filepath.split(".")[-1].lower()

    if ext == "pdf":
        return extract_text_from_pdf(filepath)
    else:
        raise ValueError("Unsupported file format")

if __name__ == "__main__":
    print(ingest_file("../sample.pdf"))
