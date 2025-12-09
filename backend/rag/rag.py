from sentence_transformers import SentenceTransformer
from backend.vector_store.store import query_store
from backend.models.local_llm import run_llm

# Load embedding model once
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_rag_answer(query: str) -> str:
    """
    Answer a query using:
    1. Vector store to get context
    2. Local LLM (Ollama) to generate response
    """
    # 1. Embed the query
    q_embedding = embed_model.encode([query])

    # 2. Retrieve top relevant documents from local vector store
    results = query_store(q_embedding)
    if not results or not results.get("documents"):
        context = ""
    else:
        # Join top retrieved documents as context
        context = "\n".join(results["documents"][0])

    # 3. Create prompt for LLM
    prompt = f"""
You are HOME, a private AI assistant.
Use ONLY the context below to answer the question.

Context:
{context}

Question:
{query}

Answer:
"""

    # 4. Run local LLM via Ollama CLI
    response = run_llm(prompt)

    return response
