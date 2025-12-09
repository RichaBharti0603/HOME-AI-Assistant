from fastapi import FastAPI
from backend.rag.retriever import get_answer

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Home AI Assistant Backend Running!"}

@app.get("/query")
def query(q: str):
    answer = get_answer(q)
    return {"query": q, "answer": answer}
