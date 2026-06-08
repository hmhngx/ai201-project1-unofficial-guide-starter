import os
import re


def clean_text(text: str) -> str:
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        # Remove pure metadata lines
        if re.match(r'^(SOURCE|URL|TITLE):\s', line):
            continue
        # Remove pure separator lines (---, ===, --------) but NOT === Professor: X === lines
        if re.match(r'^[-=]{3,}$', line.strip()):
            continue
        # Remove POST: and COMMENTS: label lines
        if line.strip() in ('POST:', 'COMMENTS:', 'REVIEWS:') or re.match(r'^NOTE:\s', line):
            continue
        # Remove Reddit attribution prefixes (u/username:)
        line = re.sub(r'^u/[\w-]+:\s*', '', line)
        cleaned.append(line)
    result = re.sub(r'\n{3,}', '\n\n', '\n'.join(cleaned))
    return result.strip()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    paragraphs = [p.strip() for p in re.split(r'\n\n+', text) if p.strip()]
    chunks = []
    buffer = ''

    for para in paragraphs:
        if len(para) > chunk_size:
            # Flush buffer first
            if buffer and len(buffer) >= 50:
                chunks.append(buffer)
                buffer = ''
            # Split large paragraph by characters with overlap
            start = 0
            while start < len(para):
                chunk = para[start:start + chunk_size].strip()
                if len(chunk) >= 50:
                    chunks.append(chunk)
                start += chunk_size - overlap
            continue

        candidate = (buffer + '\n\n' + para).strip() if buffer else para
        if len(candidate) > chunk_size:
            if buffer and len(buffer) >= 50:
                chunks.append(buffer)
            # Seed new buffer with overlap tail + current paragraph
            tail = buffer[-overlap:].strip() if len(buffer) >= overlap else buffer.strip()
            seeded = (tail + ' ' + para).strip() if tail else para
            if len(seeded) > chunk_size:
                # seeded buffer itself exceeds limit — character-split it
                start = 0
                while start < len(seeded):
                    chunk = seeded[start:start + chunk_size].strip()
                    if len(chunk) >= 50:
                        chunks.append(chunk)
                    start += chunk_size - overlap
                buffer = ''
            else:
                buffer = seeded
        else:
            buffer = candidate

    if buffer and len(buffer.strip()) >= 50:
        chunks.append(buffer.strip())

    return chunks


def load_documents(documents_dir: str = 'documents') -> list:
    pass  # implemented in Task 3


def build_chunks(documents_dir: str = 'documents', chunk_size: int = 500, overlap: int = 50) -> list:
    pass  # implemented in Task 4
