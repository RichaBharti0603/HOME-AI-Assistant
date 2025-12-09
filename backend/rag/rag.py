from sentence_transformers import SentenceTransformer
from backend.vector_store.store import query_store
from backend.models.local_llm import run_llm

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def answer_query(query):
    q_embedding = embed_model.encode([query])
    results = query_store(q_embedding)
    context = "\n".join(results["documents"][0])

    prompt = f"""
    You are HOME, a private AI assistant.
    Use ONLY the context below:

    Context:
    {context}

    Question:
    {query}

    Answer:
    """
    return run_llm(prompt)
