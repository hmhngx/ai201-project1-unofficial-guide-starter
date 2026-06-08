import pytest
from unittest.mock import patch, MagicMock
from scripts.generate import generate, SYSTEM_PROMPT

SAMPLE_CHUNKS = [
    {
        "text": "Professor DeNero is known for clear lecture videos in CS 61A.",
        "source": "rmp",
        "file_path": "documents/rmp/cs_professors.txt",
        "distance": 0.3,
    },
    {
        "text": "Josh Hug teaches CS 61B and is highly rated by students.",
        "source": "rmp",
        "file_path": "documents/rmp/cs_professors.txt",
        "distance": 0.35,
    },
    {
        "text": "CS 61B projects take 15-25 hours each according to student reviews.",
        "source": "reddit",
        "file_path": "documents/reddit/cs61b_discussion.txt",
        "distance": 0.4,
    },
]


def _mock_response(content: str):
    mock = MagicMock()
    mock.choices[0].message.content = content
    return mock


def test_generate_returns_answer_and_sources():
    with patch("scripts.generate.Groq") as MockGroq:
        MockGroq.return_value.chat.completions.create.return_value = _mock_response(
            "DeNero is known for clear lecture videos."
        )
        result = generate("Who teaches CS 61A?", SAMPLE_CHUNKS)
    assert "answer" in result
    assert "sources" in result
    assert isinstance(result["answer"], str)
    assert isinstance(result["sources"], list)


def test_generate_sources_come_from_chunks():
    with patch("scripts.generate.Groq") as MockGroq:
        MockGroq.return_value.chat.completions.create.return_value = _mock_response(
            "DeNero teaches 61A."
        )
        result = generate("Who teaches CS 61A?", SAMPLE_CHUNKS)
    assert "rmp" in result["sources"]
    assert "reddit" in result["sources"]


def test_generate_sources_are_deduplicated():
    # SAMPLE_CHUNKS has two chunks with source="rmp" — must appear only once
    with patch("scripts.generate.Groq") as MockGroq:
        MockGroq.return_value.chat.completions.create.return_value = _mock_response(
            "DeNero teaches 61A."
        )
        result = generate("Who teaches CS 61A?", SAMPLE_CHUNKS)
    assert result["sources"].count("rmp") == 1


def test_generate_empty_chunks_returns_no_info():
    # No Groq call needed — function must return early
    result = generate("What is quantum mechanics?", [])
    assert "don't have enough information" in result["answer"].lower()
    assert result["sources"] == []


def test_generate_system_prompt_enforces_grounding():
    # System prompt must contain strong grounding instruction and the fallback phrase
    assert "ONLY" in SYSTEM_PROMPT
    assert "I don't have enough information" in SYSTEM_PROMPT


def test_generate_user_message_contains_query_and_context():
    with patch("scripts.generate.Groq") as MockGroq:
        mock_create = MockGroq.return_value.chat.completions.create
        mock_create.return_value = _mock_response("DeNero teaches 61A.")
        generate("Who teaches CS 61A?", SAMPLE_CHUNKS)
        call_kwargs = mock_create.call_args.kwargs
        messages = call_kwargs["messages"]
        user_content = next(m["content"] for m in messages if m["role"] == "user")
        assert "Who teaches CS 61A?" in user_content
        assert "DeNero" in user_content  # chunk text must be in the injected context
