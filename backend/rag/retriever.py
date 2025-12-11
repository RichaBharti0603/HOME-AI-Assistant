# backend/rag/retriever.py
from backend.vector_store.store import load_embeddings
from sentence_transformers import SentenceTransformer, util
import requests

# Embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# LLM endpoint (Ollama / local LLaMA/H2O GPT)
LLM_URL = "http://127.0.0.1:11434/api/completions"

def get_answer(query, user_profile="", top_k=3):
    texts, embeddings = load_embeddings()

    if not texts:
        return "No documents indexed yet."

    query_emb = embed_model.encode(query, convert_to_tensor=True)

    # Cosine similarity
    scores = util.cos_sim(query_emb, embeddings)[0]

    # Top-k relevant documents
    top_results = scores.topk(k=min(top_k, len(texts)))

    combined_context = ""
    for score, idx in zip(top_results.values, top_results.indices):
        combined_context += texts[idx] + "\n\n"

    if not combined_context.strip():
        return "I don't have enough information to answer that."

    # Build prompt for LLM
    prompt = f"""You are a helpful personal AI assistant.

User profile:
{user_profile}

Context from documents:
{combined_context}

Question:
{query}

Answer:"""

    # Call the local LLM (Ollama / H2O GPT)
    response = requests.post(
        LLM_URL,
        json={"model": "llama3.1:latest", "prompt": prompt, "max_tokens": 500}
    )

    if response.status_code == 200:
        return response.json().get("completion", "").strip()
    else:
        return f"Error contacting LLM: {response.text}"


def get_answer_stream(query, top_k=3):
    texts, embeddings = load_embeddings()
    if not texts:
        yield "No documents indexed yet."
        return

    query_emb = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_emb, embeddings)[0]
    top_results = scores.topk(k=min(top_k, len(texts)))

    for score, idx in zip(top_results.values, top_results.indices):
        context_chunk = texts[idx] + "\n\n"
        yield context_chunk
