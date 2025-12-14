from typing import Generator, List
from backend.vector_store.store import load_embeddings
from backend.models.local_llm import run_llm_stream
from sentence_transformers import SentenceTransformer, util
import torch

# Load embedding model once
embed_model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_topk(query: str, top_k: int = 3) -> List[str]:
    texts, embeddings = load_embeddings()

    if not texts or embeddings is None or len(embeddings) == 0:
        return []

    query_embedding = embed_model.encode(query, convert_to_tensor=True)

    scores = util.cos_sim(query_embedding, embeddings)[0]
    top_k = min(top_k, len(texts))
    top_results = torch.topk(scores, k=top_k)

    return [texts[idx] for idx in top_results.indices.tolist()]


def build_prompt(
    question: str,
    docs: List[str],
    session_memory: str
) -> str:
    context = "\n\n".join(docs) if docs else "No relevant documents found."

    return f"""
You are HOME, a private local AI assistant.

Conversation memory:
{session_memory}

Context:
{context}

User question:
{question}

Answer naturally and clearly.
"""


def get_answer_stream(
    question: str,
    session_memory: str = "",
    top_k: int = 3
) -> Generator[str, None, None]:
    """
    Stream answer tokens from local LLM
    """

    docs = retrieve_topk(question, top_k)
    prompt = build_prompt(question, docs, session_memory)

    for chunk in run_llm_stream(prompt):
        yield chunk
