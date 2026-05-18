import pdfplumber
from pathlib import Path

def chunk_pdf(file_path: str, chunk_size: int = 500, overlap: int = 50) -> list[dict]:
    chunks = []
    source = Path(file_path).name
    with pdfplumber.open(file_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue
            words = text.split()
            i = 0
            chunk_index = 0
            while i < len(words):
                chunk_text = ' '.join(words[i : i + chunk_size]).strip()
                if chunk_text:
                    chunks.append({'text': chunk_text, 'page': page_num + 1, 'chunk_index': chunk_index, 'source': source})
                    chunk_index += 1
                i += chunk_size - overlap
    return chunks
