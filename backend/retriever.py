import os
from sentence_transformers import SentenceTransformer
from embedder import get_collection
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / '.env')

model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve(query: str, top_k: int = 5) -> list[dict]:
    query_embedding = model.encode([query]).tolist()[0]
    collection = get_collection()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k, include=['documents', 'metadatas', 'distances'])
    chunks = []
    for doc, meta, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
        chunks.append({'text': doc, 'source': meta.get('source'), 'page': meta.get('page'), 'score': round(1 - dist, 4)})
    return chunks
