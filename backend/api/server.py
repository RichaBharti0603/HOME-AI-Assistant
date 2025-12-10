# backend/api/server.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from backend.rag.retriever import get_answer
import subprocess
import shlex
import os
from typing import Generator

app = FastAPI(title="HOME AI Assistant API")

# CORS - allow your frontend origin(s). For development allow all.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # TODO: restrict to your frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "Home AI Assistant API is running."}

@app.post("/ask")
def ask(payload: Query):
    """
    Non-streaming synchronous endpoint for simple use.
    """
    answer = get_answer(payload.question)
    return {"question": payload.question, "answer": answer}

# --- streaming endpoint using the Ollama CLI (reads stdout progressively) ---
def stream_ollama_cli(prompt: str) -> Generator[bytes, None, None]:
    """
    Run ollama in CLI mode and yield stdout as bytes for StreamingResponse.
    This uses: `ollama run <model> <prompt>` and reads stdout lines as they appear.
    """
    # model name - change if you want a different model
    model = os.getenv("OLLAMA_MODEL", "llama3.2")
    # build CLI command - use text mode
    # We run without shell=True; use shlex for safe tokenization.
    cmd = ["ollama", "run", model, prompt]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    except FileNotFoundError:
        yield "Error: ollama CLI not found on server.\n".encode()
        return

    # Stream stdout line by line
    with proc.stdout:
        for line in iter(proc.stdout.readline, ""):
            # Each chunk is sent as plain text chunk. Client can parse line breaks.
            yield line.encode("utf-8")
    proc.wait()

@app.post("/ask_stream")
async def ask_stream(payload: Query):
    """
    Streaming endpoint returns a chunked response of LLM output.
    The client should open a fetch and stream the bytes, or use EventSource-style parser.
    """
    prompt = f"You are HOME, a private AI assistant.\nQuestion:\n{payload.question}\nAnswer:\n"
    stream = stream_ollama_cli(prompt)
    return StreamingResponse(stream, media_type="text/plain")
