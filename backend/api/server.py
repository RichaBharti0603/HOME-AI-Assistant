# backend/api/server.py
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from backend.rag.retriever import get_answer as get_rag_answer
from backend.personalization.store import load_profile, append_history, save_profile
from backend.cache.cache import cached

import shutil, os

app = FastAPI(title="HOME AI Assistant API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str
    user_id: str = None
    stream: bool = False
    top_k: int = 3

@app.post("/ask")
def ask(payload: Query):
    profile = load_profile(payload.user_id) if payload.user_id else {}

    history_items = profile.get("history", [])[-5:]
    recent_history = "".join([h["text"] for h in history_items])

    user_profile_text = (
        f"Name: {profile.get('name','')}\n"
        f"Preferences: {profile.get('preferences','')}\n"
        f"Recent history: {recent_history}"
    )

    answer = get_rag_answer(payload.question, top_k=payload.top_k)

    # Save history
    if payload.user_id:
        append_history(payload.user_id, "user", payload.question)
        append_history(payload.user_id, "assistant", answer)

    return {"answer": answer}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    docs_dir = os.path.join(os.path.dirname(__file__), "..", "documents")
    os.makedirs(docs_dir, exist_ok=True)
    dest = os.path.join(docs_dir, file.filename)
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"status": "saved", "path": dest}

@app.get("/profile/{user_id}")
def get_profile(user_id: str):
    return load_profile(user_id)

@app.post("/profile/{user_id}")
def update_profile(user_id: str, payload: dict):
    profile = load_profile(user_id)
    profile.update(payload)
    save_profile(user_id, profile)
    return profile
