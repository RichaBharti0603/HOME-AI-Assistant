from fastapi import FastAPI
from pydantic import BaseModel
from backend.rag.retriever import get_answer

app = FastAPI(title="Home AI Assistant API")

class Query(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "Home AI Assistant API is running."}

@app.post("/ask")
def ask_question(payload: Query):
    answer = get_answer(payload.question)
    return {"question": payload.question, "answer": answer}
