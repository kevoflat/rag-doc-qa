import os
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

def embed_chunks(chunks: list[dict], doc_id: str) -> int:
    collection = get_collection()
    texts = [c["text"] for c in chunks]
    ids = [f"{doc_id}_p{c['page']}_c{c['chunk_index']}" for c in chunks]
    metadatas = [{"source": c["source"], "page": c["page"]} for c in chunks]
    collection.upsert(ids=ids, documents=texts, metadatas=metadatas)
    return len(chunks)