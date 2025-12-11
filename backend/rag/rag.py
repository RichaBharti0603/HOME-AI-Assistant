# backend/rag/rag.py
from sentence_transformers import SentenceTransformer, util
from backend.vector_store.store import load_embeddings
from backend.models.local_llm import run_llm_stream, run_llm  # see below
from typing import List

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_topk(query: str, top_k: int = 3):
    texts, embeddings = load_embeddings()  # return list[str], numpy array
    if not texts or embeddings.size == 0:
        return []
    q_emb = embed_model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(q_emb, embeddings)[0]  # torch tensor
    topk = scores.topk(k=min(top_k, len(texts)))
    top_idxs = topk.indices.tolist()
    top_texts = [texts[i] for i in top_idxs]
    return top_texts

def build_prompt(question: str, docs: List[str], user_profile: str = ""):
    context = "\n\n---\n\n".join(docs) if docs else "No context available."
    profile_section = f"User profile:\n{user_profile}\n\n" if user_profile else ""
    prompt = f"""{profile_section}You are HOME, a private AI assistant. Use ONLY the context below to answer the question. Be concise and show sources when possible.

Context:
{context}

Question:
{question}

Answer:"""
    return prompt

def get_rag_answer(question: str, user_profile: str = "", top_k: int = 3) -> str:
    docs = retrieve_topk(question, top_k=top_k)
    prompt = build_prompt(question, docs, user_profile)
    # use sync LLM (non-streaming)
    return run_llm(prompt)

def stream_rag_answer(question: str, user_profile: str = "", top_k: int = 3):
    # generator that yields bytes/chunks
    docs = retrieve_topk(question, top_k=top_k)
    prompt = build_prompt(question, docs, user_profile)
    # run local LLM streaming generator
    for chunk in run_llm_stream(prompt):
        yield chunk
