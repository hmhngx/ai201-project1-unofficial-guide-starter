import os
import pytest
import chromadb
from scripts.embed import build_index, load_collection

SAMPLE_CHUNKS = [
    {"text": "Professor DeNero teaches CS 61A at UC Berkeley and is known for clear lecture videos.", "source": "rmp", "file_path": "documents/rmp/cs_professors.txt"},
    {"text": "Josh Hug is the main instructor for CS 61B and is highly rated by students.", "source": "rmp", "file_path": "documents/rmp/cs_professors.txt"},
    {"text": "CS 170 is considered one of the hardest upper-division CS courses at Berkeley.", "source": "reddit", "file_path": "documents/reddit/berkeley_cs170_difficulty.txt"},
    {"text": "HKN course guides recommend starting CS 61B projects at least one week early.", "source": "hkn", "file_path": "documents/hkn/cs61b_guide.txt"},
    {"text": "Students say CS 189 requires strong linear algebra and probability before enrolling.", "source": "berkeleytime", "file_path": "documents/berkeleytime/cs189_reviews.txt"},
]


def test_build_index_returns_collection(tmp_path):
    collection = build_index(SAMPLE_CHUNKS, persist_dir=str(tmp_path))
    assert collection is not None
    assert collection.count() == len(SAMPLE_CHUNKS)


def test_build_index_stores_source_metadata(tmp_path):
    build_index(SAMPLE_CHUNKS, persist_dir=str(tmp_path))
    client = chromadb.PersistentClient(path=str(tmp_path))
    col = client.get_collection("documents")
    result = col.get(ids=["chunk_0"], include=["metadatas"])
    assert result["metadatas"][0]["source"] == "rmp"


def test_build_index_stores_file_path_metadata(tmp_path):
    build_index(SAMPLE_CHUNKS, persist_dir=str(tmp_path))
    client = chromadb.PersistentClient(path=str(tmp_path))
    col = client.get_collection("documents")
    result = col.get(ids=["chunk_2"], include=["metadatas"])
    assert "documents/reddit" in result["metadatas"][0]["file_path"]


def test_build_index_overwrites_existing_collection(tmp_path):
    build_index(SAMPLE_CHUNKS, persist_dir=str(tmp_path))
    build_index(SAMPLE_CHUNKS, persist_dir=str(tmp_path))
    client = chromadb.PersistentClient(path=str(tmp_path))
    col = client.get_collection("documents")
    assert col.count() == len(SAMPLE_CHUNKS)


def test_load_collection_returns_existing_collection(tmp_path):
    build_index(SAMPLE_CHUNKS, persist_dir=str(tmp_path))
    col = load_collection(persist_dir=str(tmp_path))
    assert col.count() == len(SAMPLE_CHUNKS)


def test_build_index_handles_more_than_100_chunks(tmp_path):
    large_chunks = [
        {"text": f"Chunk number {i} about UC Berkeley CS professors and courses.", "source": "rmp", "file_path": f"documents/rmp/file_{i}.txt"}
        for i in range(120)
    ]
    collection = build_index(large_chunks, persist_dir=str(tmp_path))
    assert collection.count() == 120
