# backend/api/server.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from backend.rag.retriever import get_answer
from backend.personalization.store import load_profile, append_history, save_profile

import os
import shutil
import time

app = FastAPI(title="HOME AI Assistant API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskPayload(BaseModel):
    question: str
    user_id: str | None = None
    top_k: int = 3


@app.post("/ask")
def ask(payload: AskPayload):
    answer = get_answer(payload.question, top_k=payload.top_k)

    if payload.user_id:
        append_history(payload.user_id, "user", payload.question)
        append_history(payload.user_id, "assistant", answer)

    return {"answer": answer}


@app.post("/ask_stream")
def ask_stream(payload: AskPayload):
    """
    Streams ONLY text chunks using SSE-style format:
    data: <text>
    data: [DONE]
    """

    def event_generator():
        answer = get_answer(payload.question, top_k=payload.top_k)

        # Save user message immediately
        if payload.user_id:
            append_history(payload.user_id, "user", payload.question)

        # Stream word-by-word (safe & simple)
        for token in answer.split():
            yield f"data: {token} \n\n"
            time.sleep(0.03)

        yield "data: [DONE]\n\n"

        # Save assistant message
        if payload.user_id:
            append_history(payload.user_id, "assistant", answer)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )


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
