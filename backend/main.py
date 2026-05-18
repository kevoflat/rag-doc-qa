import os, uuid, shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chunker import chunk_pdf
from embedder import embed_chunks
from retriever import retrieve
from llm import generate_answer

app = FastAPI(title='RAG Document Q&A API')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

UPLOAD_DIR = './uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

class QueryRequest(BaseModel):
    question: str
    top_k: int = 5

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.post('/upload')
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, 'Only PDF files are supported.')
    doc_id = str(uuid.uuid4())[:8]
    save_path = f"{UPLOAD_DIR}/{doc_id}_{file.filename}"
    with open(save_path, 'wb') as f:
        shutil.copyfileobj(file.file, f)
    chunks = chunk_pdf(save_path)
    count = embed_chunks(chunks, doc_id)
    return {'doc_id': doc_id, 'filename': file.filename, 'chunks_indexed': count}

@app.post('/query')
def query(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(400, 'Question cannot be empty.')
    chunks = retrieve(req.question, top_k=req.top_k)
    if not chunks:
        return {'answer': 'No documents uploaded yet.', 'sources': []}
    return generate_answer(req.question, chunks)
