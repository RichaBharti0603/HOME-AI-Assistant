# backend/rag/retriever.py
from typing import Generator, Optional, List, Tuple
import requests
import json
import time

from backend.vector_store.store import load_embeddings
from sentence_transformers import SentenceTransformer, util

# Load the embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Ollama-like local LLM HTTP endpoint (adjust if you run a different server)
LLM_HTTP_URL = "http://127.0.0.1:11434/api/generate"
DEFAULT_MODEL = "llama3.2:latest"
STREAM_CHUNK_SIZE = 256  # fallback chunk size for non-streaming fallback


def _retrieve_context(query_emb, top_k: int) -> Tuple[str, List[int]]:
    """
    Return combined context string and list of indices used.
    """
    texts, embeddings = load_embeddings()
    if not texts or embeddings is None:
        return "", []

    # compute cosine similarity
    scores = util.cos_sim(query_emb, embeddings)[0]
    # topk
    k = min(top_k, len(texts))
    top = scores.topk(k=k)
    selected_indices = [int(i.item()) for i in top.indices]
    combined = "\n\n".join([texts[i] for i in selected_indices])
    return combined, selected_indices


def get_answer(question: str, top_k: int = 3, user_profile_text: str = "") -> str:
    """
    Non-streaming answer: embed query (with optional user profile), retrieve top-k,
    and return combined context (or optionally call the LLM synchronously).
    """
    # combine profile + query for embedding (helps retrieval prioritize)
    full_query = (user_profile_text + "\n\n" + question).strip() if user_profile_text else question
    query_emb = model.encode(full_query, convert_to_tensor=True)

    combined_context, idxs = _retrieve_context(query_emb, top_k)
    if not combined_context.strip():
        return "I don't have enough indexed information to answer that."

    # By default return combined context (simple RAG). If you prefer to call LLM synchronously,
    # uncomment the LLM call below and return the LLM response instead.

    # prompt = f"""You are HOME, a private AI assistant.\n\nContext:\n{combined_context}\n\nQuestion:\n{question}\n\nAnswer:"""
    # resp = requests.post(LLM_HTTP_URL, json={"model": DEFAULT_MODEL, "prompt": prompt, "max_tokens": 512})
    # if resp.ok:
    #     return resp.json().get("response") or resp.text
    # else:
    #     return combined_context

    # Returning context is simple fallback / useful for debugging
    return combined_context


def _stream_from_llm(prompt: str, model_name: str = DEFAULT_MODEL, timeout: int = 60) -> Generator[str, None, None]:
    """
    Attempt to stream from local LLM HTTP API. This expects the server to
    support chunked or newline-delimited streaming responses.

    This function yields raw chunks as they arrive (strings).
    """
    try:
        # Note: Actual Ollama / local LLM streaming API specifics may differ.
        # Many self-hosted LLM HTTP servers return server-sent-events (text/event-stream)
        # or chunked JSON lines. We handle common patterns: streaming lines or chunked bytes.
        payload = {"model": model_name, "prompt": prompt, "max_tokens": 512, "stream": True}
        with requests.post(LLM_HTTP_URL, json=payload, stream=True, timeout=timeout) as resp:
            resp.raise_for_status()
            # attempt to stream line by line
            for raw in resp.iter_lines(decode_unicode=True):
                if raw is None:
                    continue
                line = raw.strip()
                if not line:
                    continue
                # some servers send JSON lines, some send plain text
                # try to parse JSON, otherwise yield raw line
                try:
                    data = json.loads(line)
                    # common patterns: {"token":"...", ...} or {"response": "..."}
                    if isinstance(data, dict):
                        # prefer content fields if present
                        text_chunk = data.get("token") or data.get("response") or data.get("content") or data.get("text")
                        if text_chunk:
                            yield text_chunk
                            continue
                    # fallback to entire line
                    yield line
                except json.JSONDecodeError:
                    # plain text chunk
                    yield line
    except Exception as e:
        # propagate exception to caller to fall back
        raise


def get_answer_stream(question: str, top_k: int = 3, user_profile_text: str = "") -> Generator[str, None, None]:
    """
    Streaming generator that yields chunks of the final answer.
    Behavior:
     - Retrieve context via embeddings.
     - Form a prompt that includes user_profile_text and the combined context.
     - Try streaming from the local LLM HTTP endpoint.
     - If that fails, fall back to synchronous get_answer() and yield chunked slices.
    """
    full_query = (user_profile_text + "\n\n" + question).strip() if user_profile_text else question
    query_emb = model.encode(full_query, convert_to_tensor=True)
    combined_context, idxs = _retrieve_context(query_emb, top_k)

    if not combined_context.strip():
        yield "I don't have enough indexed information to answer that."
        return

    prompt = f"""You are HOME, a private AI assistant. Use only the context below to answer the question.\n\nContext:\n{combined_context}\n\nQuestion:\n{question}\n\nAnswer:"""

    # Attempt streaming from local LLM HTTP server
    try:
        for chunk in _stream_from_llm(prompt, model_name=DEFAULT_MODEL):
            yield chunk
        return
    except Exception:
        # streaming failed — fallback to a synchronous LLM call if desired or chunk the retrieval text
        pass

    # Fallback: try synchronous LLM call (non-streaming)
    try:
        payload = {"model": DEFAULT_MODEL, "prompt": prompt, "max_tokens": 512}
        resp = requests.post(LLM_HTTP_URL, json=payload, timeout=30)
        if resp.ok:
            # Try JSON content
            try:
                data = resp.json()
                # common fields
                text = data.get("response") or data.get("completion") or data.get("text") or json.dumps(data)
            except Exception:
                text = resp.text
        else:
            text = combined_context
    except Exception:
        text = combined_context

    # yield in reasonable chunks (safe fallback)
    if not text:
        text = "No answer generated."

    for i in range(0, len(text), STREAM_CHUNK_SIZE):
        yield text[i : i + STREAM_CHUNK_SIZE]
        time.sleep(0.02)
