def retrieve(query: str, collection, k: int = 5) -> list:
    results = collection.query(
        query_texts=[query],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    chunks = []
    for text, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({
            "text": text,
            "source": meta["source"],
            "file_path": meta["file_path"],
            "distance": dist,
        })
    return chunks
