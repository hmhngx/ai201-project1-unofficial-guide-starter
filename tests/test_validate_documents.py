import os
import pytest
from scripts.validate_documents import load_document_manifest, validate_documents

MANIFEST = load_document_manifest()


def test_manifest_has_thirteen_entries():
    assert len(MANIFEST) == 13


def test_all_documents_exist(tmp_path):
    fake = tmp_path / "fake.txt"
    fake.write_text("x" * 200)
    result = validate_documents([str(fake)])
    assert result["missing"] == []
    assert result["too_short"] == []


def test_missing_document_detected(tmp_path):
    missing = str(tmp_path / "nonexistent.txt")
    result = validate_documents([missing])
    assert missing in result["missing"]


def test_short_document_detected(tmp_path):
    short = tmp_path / "short.txt"
    short.write_text("hi")
    result = validate_documents([str(short)])
    assert str(short) in result["too_short"]
