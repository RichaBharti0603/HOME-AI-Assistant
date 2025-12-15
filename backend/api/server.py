from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from backend.rag.retriever import get_answer_stream
from backend.memory.session_store import (
    append_turn,
    get_summary,
    summarize_session
)

app = FastAPI(title="HOME AI Assistant API")


class AskPayload(BaseModel):
    question: str
    session_id: str


@app.post("/ask_stream")
def ask_stream(payload: AskPayload):

    session_id = payload.session_id
    question = payload.question

    # Store user turn
    append_turn(session_id, "User", question)

    conversation_memory = get_summary(session_id)

    def stream():
        answer_text = ""

        for chunk in get_answer_stream(
            question=question,
            conversation_memory=conversation_memory
        ):
            answer_text += chunk
            yield f"data: {chunk}\n\n"

        # Store assistant turn
        append_turn(session_id, "Assistant", answer_text)

        # Summarize if needed
        summarize_session(session_id)

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream(),
        media_type="text/event-stream"
    )
