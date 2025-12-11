from backend.vector_store.store import load_embeddings
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_answer(query, top_k=3):
    texts, embeddings = load_embeddings()

    if not texts:
        return "No documents indexed yet."

    query_emb = model.encode(query, convert_to_tensor=True)

    # Compute cosine similarity scores
    scores = util.cos_sim(query_emb, embeddings)[0]

    # Pick top-k results
    top_results = scores.topk(k=min(top_k, len(texts)))

    combined_context = ""

    for score, idx in zip(top_results.values, top_results.indices):
        combined_context += texts[idx] + "\n\n"

    if not combined_context.strip():
        return "I don't have enough information to answer that."

    return combined_context
