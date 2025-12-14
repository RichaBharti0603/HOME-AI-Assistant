from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from backend.rag.retriever import get_answer_stream
from backend.memory.session_store import (
    init_db,
    append_to_session,
    get_session_context
)

app = FastAPI(title="HOME AI Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

class AskPayload(BaseModel):
    question: str
    session_id: str

@app.post("/ask_stream")
def ask_stream(payload: AskPayload):
    session_id = payload.session_id
    question = payload.question

    append_to_session(session_id, "user", question)
    memory = get_session_context(session_id)

    def stream():
        answer_accumulator = ""
        for chunk in get_answer_stream(
            question=question,
            session_memory=memory
        ):
            answer_accumulator += chunk
            yield f"data: {chunk}\n\n"

        append_to_session(session_id, "assistant", answer_accumulator)
        yield "data: [DONE]\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")
