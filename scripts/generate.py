import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions about UC Berkeley CS courses "
    "and professors.\n\n"
    "Answer the question using ONLY the information provided in the context documents "
    "below. Do not use any knowledge outside of the provided context.\n\n"
    "If the context does not contain enough information to answer the question, you "
    "MUST respond with exactly: \"I don't have enough information on that.\"\n\n"
    "Do not guess. Do not infer. Do not use general knowledge. Every factual claim in "
    "your answer must come directly from the context."
)


def generate(query: str, chunks: list) -> dict:
    """
    Generate a grounded answer from retrieved chunks.

    Args:
        query:  The user's question.
        chunks: List of dicts with keys: text, source, file_path, distance.

    Returns:
        {"answer": str, "sources": list[str]}
        Sources are deduplicated, in order of first appearance.
    """
    if not chunks:
        return {"answer": "I don't have enough information on that.", "sources": []}

    # Programmatic source extraction — not left to the LLM
    sources = list(dict.fromkeys(c["source"] for c in chunks))

    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        context_parts.append(f"[{i}] (source: {chunk['source']})\n{chunk['text']}")
    context = "\n\n".join(context_parts)

    user_message = (
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\n"
        "Answer (using ONLY the context above):"
    )

    client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.1,
        max_tokens=512,
    )

    answer = response.choices[0].message.content.strip()
    return {"answer": answer, "sources": sources}
