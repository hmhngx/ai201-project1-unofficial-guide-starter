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
        if line.strip() in ('POST:', 'COMMENTS:'):
            continue
        # Remove Reddit attribution prefixes (u/username:)
        line = re.sub(r'^u/\w+:\s*', '', line)
        cleaned.append(line)
    result = re.sub(r'\n{3,}', '\n\n', '\n'.join(cleaned))
    return result.strip()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    pass  # implemented in Task 2


def load_documents(documents_dir: str = 'documents') -> list:
    pass  # implemented in Task 3


def build_chunks(documents_dir: str = 'documents', chunk_size: int = 500, overlap: int = 50) -> list:
    pass  # implemented in Task 4
