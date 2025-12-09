import chromadb

client = chromadb.Client()
collection = client.create_collection("home_docs")

def add_to_store(text_chunks, embeddings):
    ids = [str(i) for i in range(len(text_chunks))]
    collection.add(
        documents=text_chunks,
        embeddings=embeddings,
        ids=ids
    )

def query_store(query_embedding, top_k=3):
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )
    return results
