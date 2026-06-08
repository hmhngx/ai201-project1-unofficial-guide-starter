from scripts.embed import load_collection
from scripts.retrieve import retrieve
from scripts.generate import generate


def ask(question: str, k: int = 5, collection=None) -> dict:
    """
    End-to-end RAG query: retrieve chunks, generate grounded answer.

    Args:
        question:   The user's question.
        k:          Number of chunks to retrieve (default 5).
        collection: ChromaDB collection. If None, loads from ./chroma_db.

    Returns:
        {"answer": str, "sources": list[str], "chunks": list[dict]}
    """
    if collection is None:
        collection = load_collection()
    chunks = retrieve(question, collection, k=k)
    result = generate(question, chunks)
    result["chunks"] = chunks
    return result
