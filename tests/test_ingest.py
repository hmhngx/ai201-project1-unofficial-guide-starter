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
