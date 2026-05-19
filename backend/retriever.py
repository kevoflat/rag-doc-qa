import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

chroma_client = chromadb.PersistentClient(path="./chroma_db")
ef = embedding_functions.DefaultEmbeddingFunction()
COLLECTION_NAME = "documents"

def get_collection():
    return chroma_client.get_or_create_collection(COLLECTION_NAME, embedding_function=ef)

def retrieve(query: str, top_k: int = 5) -> list[dict]:
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=top_k, include=["documents", "metadatas", "distances"])
    chunks = []
    for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
        chunks.append({"text": doc, "source": meta.get("source"), "page": meta.get("page"), "score": round(1 - dist, 4)})
    return chunks