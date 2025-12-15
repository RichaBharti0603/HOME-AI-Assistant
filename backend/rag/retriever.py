from typing import Generator, List, Tuple
import requests
import json
import time

from sentence_transformers import SentenceTransformer, util
from backend.vector_store.store import load_embeddings

# --------------------
# CONFIG
# --------------------

LLM_HTTP_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "llama3.2:latest"
STREAM_FALLBACK_CHUNK = 200

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# --------------------
# RETRIEVAL
# --------------------

def retrieve_context(query: str, top_k: int = 3) -> str:
    texts, embeddings = load_embeddings()

    if not texts or embeddings is None:
        return ""

    q_emb = embed_model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(q_emb, embeddings)[0]

    k = min(top_k, len(texts))
    top = scores.topk(k=k)

    selected = [texts[i] for i in top.indices.tolist()]
    return "\n\n".join(selected)

# --------------------
# PROMPT ENGINEERING
# --------------------

def build_prompt(
    question: str,
    context: str,
    conversation_memory: str = ""
) -> str:
    return f"""
You are HOME, a private personal AI assistant.

Rules:
- Answer like a helpful human, not a document.
- Use ONLY the provided context and memory.
- If the answer is unknown, say so clearly.
- Do NOT mention documents or sources explicitly.

Conversation memory:
{conversation_memory or "None"}

Context:
{context or "No relevant context available."}

User question:
{question}

Answer naturally and clearly:
""".strip()

# --------------------
# STREAMING LLM
# --------------------

def stream_llm(prompt: str) -> Generator[str, None, None]:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True,
        "max_tokens": 512
    }

    with requests.post(LLM_HTTP_URL, json=payload, stream=True, timeout=60) as resp:
        resp.raise_for_status()

        for line in resp.iter_lines(decode_unicode=True):
            if not line:
                continue
            try:
                data = json.loads(line)
                token = data.get("response") or data.get("token")
                if token:
                    yield token
            except json.JSONDecodeError:
                continue

# --------------------
# PUBLIC API
# --------------------

def get_answer_stream(
    question: str,
    conversation_memory: str = "",
    top_k: int = 3
) -> Generator[str, None, None]:

    context = retrieve_context(
        query=conversation_memory + "\n" + question,
        top_k=top_k
    )

    prompt = build_prompt(
        question=question,
        context=context,
        conversation_memory=conversation_memory
    )

    try:
        for token in stream_llm(prompt):
            yield token
        return
    except Exception:
        pass

    # fallback (safe)
    fallback = "I’m having trouble generating a response right now."
    for i in range(0, len(fallback), STREAM_FALLBACK_CHUNK):
        yield fallback[i:i+STREAM_FALLBACK_CHUNK]
        time.sleep(0.02)
