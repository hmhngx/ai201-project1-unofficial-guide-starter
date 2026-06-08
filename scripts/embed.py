import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

COLLECTION_NAME = "documents"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
BATCH_SIZE = 100


def _get_embedding_function():
    return SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)


def build_index(chunks: list, persist_dir: str = "./chroma_db") -> object:
    ef = _get_embedding_function()
    client = chromadb.PersistentClient(path=persist_dir)

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(COLLECTION_NAME, embedding_function=ef)

    texts = [c["text"] for c in chunks]
    metadatas = [{"source": c["source"], "file_path": c["file_path"]} for c in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    for i in range(0, len(chunks), BATCH_SIZE):
        collection.add(
            documents=texts[i : i + BATCH_SIZE],
            metadatas=metadatas[i : i + BATCH_SIZE],
            ids=ids[i : i + BATCH_SIZE],
        )

    return collection


def load_collection(persist_dir: str = "./chroma_db") -> object:
    ef = _get_embedding_function()
    client = chromadb.PersistentClient(path=persist_dir)
    return client.get_collection(COLLECTION_NAME, embedding_function=ef)
