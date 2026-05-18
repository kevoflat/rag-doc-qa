from fastapi import FastAPI

app = FastAPI(title="RAG Document Q&A")

@app.get("/")
def home():
    return {"status": "RAG API running"}