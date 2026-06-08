import pytest
from unittest.mock import patch, MagicMock
from scripts.query import ask

MOCK_CHUNKS = [
    {
        "text": "DeNero teaches CS 61A.",
        "source": "rmp",
        "file_path": "documents/rmp/cs_professors.txt",
        "distance": 0.3,
    }
]
MOCK_GENERATE_RESULT = {"answer": "DeNero teaches CS 61A.", "sources": ["rmp"]}


def test_ask_returns_required_keys():
    mock_col = MagicMock()
    with patch("scripts.query.retrieve", return_value=MOCK_CHUNKS), \
         patch("scripts.query.generate", return_value=dict(MOCK_GENERATE_RESULT)):
        result = ask("Who teaches CS 61A?", collection=mock_col)
    assert "answer" in result
    assert "sources" in result
    assert "chunks" in result


def test_ask_passes_question_to_retrieve():
    mock_col = MagicMock()
    with patch("scripts.query.retrieve", return_value=MOCK_CHUNKS) as mock_retrieve, \
         patch("scripts.query.generate", return_value=dict(MOCK_GENERATE_RESULT)):
        ask("Who teaches CS 61A?", collection=mock_col)
    assert mock_retrieve.call_args.args[0] == "Who teaches CS 61A?"


def test_ask_passes_chunks_to_generate():
    mock_col = MagicMock()
    with patch("scripts.query.retrieve", return_value=MOCK_CHUNKS), \
         patch("scripts.query.generate", return_value=dict(MOCK_GENERATE_RESULT)) as mock_gen:
        ask("Who teaches CS 61A?", collection=mock_col)
    assert mock_gen.call_args.args[1] == MOCK_CHUNKS
