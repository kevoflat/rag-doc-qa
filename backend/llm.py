import os
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = "You are a helpful document assistant. Answer using ONLY the context provided. Cite sources like [filename, p.3]. If you cannot find the answer say so."

def generate_answer(query: str, chunks: list[dict]) -> dict:
    context = "\n\n".join([f"[{c['source']}, p.{c['page']}]\n{c['text']}" for c in chunks])
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ],
        temperature=0.2,
        max_tokens=500,
    )
    
    answer = completion.choices[0].message.content
    sources = list({(c["source"], c["page"]) for c in chunks})
    return {"answer": answer, "sources": [{"file": s[0], "page": s[1]} for s in sources]}