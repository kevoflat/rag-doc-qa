# RAG Document Q&A

An end-to-end AI system that lets you upload any PDF and ask natural language questions with cited answers sourced directly from the document.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Python 3.12 |
| PDF Parsing | pdfplumber |
| Embeddings | Sentence Transformers |
| Vector Store | ChromaDB |
| LLM | Groq Llama 3.1 |
| Frontend | React + Vite + Tailwind CSS |

## Getting Started

### Prerequisites
- Python 3.12
- Node.js 18+
- Groq API key — free at console.groq.com

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /health | Server status |
| POST | /upload | Upload and index a PDF |
| POST | /query | Ask a question, get cited answer |

## Author
Built by Kevin Mwangi