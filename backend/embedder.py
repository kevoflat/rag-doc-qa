import os
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / '.env')

model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.PersistentClient(path='./chroma_db')
COLLECTION_NAME = 'documents'

def get_collection():
    return chroma_client.get_or_create_collection(COLLECTION_NAME)

def embed_chunks(chunks: list[dict], doc_id: str) -> int:
    collection = get_collection()
    texts = [c['text'] for c in chunks]
    embeddings = model.encode(texts).tolist()
    ids = [f"{doc_id}_p{c['page']}_c{c['chunk_index']}" for c in chunks]
    metadatas = [{'source': c['source'], 'page': c['page']} for c in chunks]
    collection.upsert(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)
    return len(chunks)
