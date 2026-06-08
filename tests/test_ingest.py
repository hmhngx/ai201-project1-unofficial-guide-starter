import pytest
from scripts.ingest import clean_text, chunk_text, load_documents, build_chunks


# --- clean_text ---

def test_clean_text_removes_source_and_url_lines():
    raw = "SOURCE: reddit.com/r/berkeley\nURL: https://example.com\n\nActual content here."
    result = clean_text(raw)
    assert "SOURCE:" not in result
    assert "URL:" not in result
    assert "Actual content here." in result


def test_clean_text_removes_title_line():
    raw = "TITLE: Which professor should I take?\n\nPost body text."
    result = clean_text(raw)
    assert "TITLE:" not in result
    assert "Post body text." in result


def test_clean_text_removes_pure_separator_lines():
    raw = "Some review text.\n---\nAnother review."
    result = clean_text(raw)
    assert "---" not in result
    assert "Some review text." in result
    assert "Another review." in result


def test_clean_text_removes_hkn_underline_separators():
    raw = "Overview\n--------\nCS 61A is about abstraction."
    result = clean_text(raw)
    assert "--------" not in result
    assert "Overview" in result
    assert "CS 61A is about abstraction." in result


def test_clean_text_removes_reddit_attribution_prefix():
    raw = "u/berkCS_junior: This professor is great.\n\nu/eecs_sophomore: Agree with above."
    result = clean_text(raw)
    assert "u/berkCS_junior:" not in result
    assert "u/eecs_sophomore:" not in result
    assert "This professor is great." in result
    assert "Agree with above." in result


def test_clean_text_removes_post_and_comments_labels():
    raw = "POST:\nSome post text.\n\nCOMMENTS:\nFirst comment."
    result = clean_text(raw)
    assert "POST:" not in result
    assert "COMMENTS:" not in result
    assert "Some post text." in result
    assert "First comment." in result


def test_clean_text_preserves_professor_header_line():
    raw = "=== Professor: Dan Garcia | Rating: 3.7/5 ===\nGreat professor overall."
    result = clean_text(raw)
    assert "Dan Garcia" in result
    assert "3.7/5" in result
    assert "Great professor overall." in result


def test_clean_text_preserves_course_line():
    raw = "COURSE: CS 61A - Structure and Interpretation of Computer Programs\n\nOverview text."
    result = clean_text(raw)
    assert "COURSE: CS 61A" in result
    assert "Overview text." in result


def test_clean_text_normalizes_multiple_blank_lines():
    raw = "Para one.\n\n\n\n\nPara two."
    result = clean_text(raw)
    assert "\n\n\n" not in result
    assert "Para one." in result
    assert "Para two." in result


def test_clean_text_strips_leading_trailing_whitespace():
    raw = "\n\n  Some content.  \n\n"
    result = clean_text(raw)
    assert result == result.strip()


def test_clean_text_removes_reviews_label():
    raw = "REVIEWS:\nCS 189 is very math heavy."
    result = clean_text(raw)
    assert "REVIEWS:" not in result
    assert "CS 189 is very math heavy." in result


def test_clean_text_removes_note_label():
    raw = "NOTE: Berkeleytime is a React app and blocks scraping.\n\nActual review text."
    result = clean_text(raw)
    assert "NOTE:" not in result
    assert "Actual review text." in result


def test_clean_text_removes_hyphenated_reddit_username():
    raw = "u/some-user: Great class overall."
    result = clean_text(raw)
    assert "u/some-user:" not in result
    assert "Great class overall." in result


def test_clean_text_removes_bare_equals_separator():
    raw = "Section content.\n===\nNext section."
    result = clean_text(raw)
    assert "\n===\n" not in result
    assert "Section content." in result
    assert "Next section." in result


def test_clean_text_strips_whitespace_produces_clean_result():
    raw = "\n\n  Some content here.  \n\n"
    result = clean_text(raw)
    assert result == "Some content here."


# --- chunk_text ---

def test_chunk_text_no_chunk_exceeds_size_limit():
    # Single large paragraph — tests character-split path
    text = "x" * 1200
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    for chunk in chunks:
        assert len(chunk) <= 500, f"Chunk too long: {len(chunk)}"

    # Two large paragraphs — tests paragraph-flush + overlap-seed path
    text2 = "A" * 460 + "\n\n" + "B" * 460
    chunks2 = chunk_text(text2, chunk_size=500, overlap=50)
    for chunk in chunks2:
        assert len(chunk) <= 500, f"Chunk too long after paragraph flush: {len(chunk)}"


def test_chunk_text_no_empty_or_whitespace_only_chunks():
    text = "Short para.\n\n\n\nAnother short para.\n\n   \n\nThird para."
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    for chunk in chunks:
        assert chunk.strip() != ""


def test_chunk_text_enforces_minimum_length():
    text = "Hi.\n\n" + "y" * 200
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    for chunk in chunks:
        assert len(chunk) >= 50, f"Chunk too short: {len(chunk)!r}"


def test_chunk_text_preserves_all_content():
    text = "Professor DeNero is excellent.\n\nHis lectures are clear and well-structured."
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    combined = " ".join(chunks)
    assert "Professor DeNero is excellent." in combined
    assert "His lectures are clear and well-structured." in combined


def test_chunk_text_splits_text_longer_than_chunk_size():
    text = "a" * 1500
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    assert len(chunks) >= 2


def test_chunk_text_short_text_produces_one_chunk():
    text = "This is a short review. " * 5  # ~120 chars, well under 500
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    assert len(chunks) == 1


def test_chunk_text_overlap_provides_continuity():
    para_a = "A" * 400
    para_b = "B" * 400
    text = para_a + "\n\n" + para_b
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    assert len(chunks) >= 2
    assert "A" in chunks[1]


# --- load_documents ---

def test_load_documents_returns_list_of_dicts(tmp_path):
    (tmp_path / "rmp").mkdir()
    (tmp_path / "rmp" / "reviews.txt").write_text(
        "Some review content here that is long enough.", encoding="utf-8"
    )
    docs = load_documents(str(tmp_path))
    assert isinstance(docs, list)
    assert len(docs) == 1
    assert "text" in docs[0]
    assert "source" in docs[0]
    assert "file_path" in docs[0]


def test_load_documents_source_is_subdir_name(tmp_path):
    (tmp_path / "reddit").mkdir()
    (tmp_path / "reddit" / "thread.txt").write_text("Reddit thread content.", encoding="utf-8")
    docs = load_documents(str(tmp_path))
    assert docs[0]["source"] == "reddit"


def test_load_documents_file_path_ends_with_filename(tmp_path):
    (tmp_path / "hkn").mkdir()
    (tmp_path / "hkn" / "guide.txt").write_text("Guide content.", encoding="utf-8")
    docs = load_documents(str(tmp_path))
    assert docs[0]["file_path"].endswith("guide.txt")


def test_load_documents_only_loads_txt_files(tmp_path):
    (tmp_path / "rmp").mkdir()
    (tmp_path / "rmp" / "reviews.txt").write_text("Review content.", encoding="utf-8")
    (tmp_path / "rmp" / ".gitkeep").write_text("", encoding="utf-8")
    (tmp_path / "rmp" / "notes.md").write_text("Markdown content.", encoding="utf-8")
    docs = load_documents(str(tmp_path))
    assert len(docs) == 1
    assert docs[0]["file_path"].endswith("reviews.txt")


def test_load_documents_text_matches_file_content(tmp_path):
    (tmp_path / "berkeleytime").mkdir()
    content = "CS 189 review: very math heavy."
    (tmp_path / "berkeleytime" / "cs189.txt").write_text(content, encoding="utf-8")
    docs = load_documents(str(tmp_path))
    assert docs[0]["text"] == content


def test_load_documents_loads_all_13_real_documents():
    docs = load_documents("documents")
    assert len(docs) == 13, f"Expected 13 documents, got {len(docs)}"
