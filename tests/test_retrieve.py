import pytest
import chromadb
from scripts.embed import build_index
from scripts.retrieve import retrieve

SAMPLE_CHUNKS = [
    {"text": "Professor DeNero teaches CS 61A at UC Berkeley and is known for clear lecture videos.", "source": "rmp", "file_path": "documents/rmp/cs_professors.txt"},
    {"text": "Josh Hug is the main instructor for CS 61B and is highly rated by students.", "source": "rmp", "file_path": "documents/rmp/cs_professors.txt"},
    {"text": "CS 170 is considered one of the hardest upper-division CS courses at Berkeley.", "source": "reddit", "file_path": "documents/reddit/berkeley_cs170_difficulty.txt"},
    {"text": "HKN course guides recommend starting CS 61B projects at least one week early.", "source": "hkn", "file_path": "documents/hkn/cs61b_guide.txt"},
    {"text": "Students say CS 189 requires strong linear algebra and probability before enrolling.", "source": "berkeleytime", "file_path": "documents/berkeleytime/cs189_reviews.txt"},
    {"text": "CS 61B workload is described as heavy but manageable if you start projects early.", "source": "reddit", "file_path": "documents/reddit/cs61b_discussion.txt"},
    {"text": "DeNero's office hours are extremely helpful and he encourages students to attend.", "source": "rmp", "file_path": "documents/rmp/cs_professors.txt"},
]


@pytest.fixture(scope="module")
def collection(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("chroma")
    return build_index(SAMPLE_CHUNKS, persist_dir=str(tmp))


def test_retrieve_returns_list(collection):
    results = retrieve("CS 61A professor", collection)
    assert isinstance(results, list)


def test_retrieve_returns_k_results(collection):
    results = retrieve("CS 61A professor", collection, k=3)
    assert len(results) == 3


def test_retrieve_default_k_is_5(collection):
    results = retrieve("Berkeley CS courses", collection)
    assert len(results) == 5


def test_retrieve_result_has_required_keys(collection):
    results = retrieve("CS 61A professor", collection)
    for r in results:
        assert "text" in r
        assert "source" in r
        assert "file_path" in r
        assert "distance" in r


def test_retrieve_distance_is_float(collection):
    results = retrieve("CS 61A professor", collection)
    for r in results:
        assert isinstance(r["distance"], float)


def test_retrieve_top_result_is_relevant(collection):
    results = retrieve("Who teaches CS 61A?", collection)
    top_texts = " ".join(r["text"] for r in results[:2])
    assert "DeNero" in top_texts or "61A" in top_texts


def test_retrieve_returns_source_metadata(collection):
    results = retrieve("CS 61A professor", collection)
    sources = [r["source"] for r in results]
    assert "rmp" in sources
