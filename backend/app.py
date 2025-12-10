from fastapi import FastAPI
from pydantic import BaseModel
from backend.rag.retriever import get_answer
from fastapi.middleware.cors import CORSMiddleware

class QuestionPayload(BaseModel):
    question: str

app = FastAPI()

# Allow CORS from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
def ask_question(payload: QuestionPayload):
    answer = get_answer(payload.question)
    return {"answer": answer}
