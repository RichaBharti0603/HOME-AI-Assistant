# backend/rag/retriever.py

from .rag import get_rag_answer  # corrected import

def get_answer(query: str) -> str:
    """
    Retrieve an answer for the given query using the RAG pipeline.
    """
    try:
        response = get_rag_answer(query)
        return response
    except Exception as e:
        return f"Error retrieving answer: {str(e)}"

# Quick test when running this file directly
if __name__ == "__main__":
    test_query = "What is the Home AI Assistant?"
    print("Query:", test_query)
    print("Answer:", get_answer(test_query))
