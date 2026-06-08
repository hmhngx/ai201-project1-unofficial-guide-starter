import os

DOCUMENTS = [
    "documents/rmp/cs_professors.txt",
    "documents/reddit/berkeley_cs61a_professor.txt",
    "documents/reddit/cs61a_megathread.txt",
    "documents/reddit/cs61b_discussion.txt",
    "documents/reddit/berkeley_cs170_difficulty.txt",
    "documents/reddit/berkeley_best_cs_professors.txt",
    "documents/hkn/cs61a_guide.txt",
    "documents/hkn/cs61b_guide.txt",
    "documents/hkn/cs170_guide.txt",
    "documents/berkeleytime/cs189_reviews.txt",
    "documents/berkeleytime/cs61c_reviews.txt",
    "documents/reddit/berkeley_cs_workload_tier_list.txt",
    "documents/reddit/berkeley_cs_course_selection.txt",
]

MIN_CHARS = 200


def load_document_manifest():
    return DOCUMENTS


def validate_documents(paths=None):
    if paths is None:
        paths = DOCUMENTS
    missing = []
    too_short = []
    for path in paths:
        if not os.path.exists(path):
            missing.append(path)
        elif len(open(path, encoding="utf-8").read().strip()) < MIN_CHARS:
            too_short.append(path)
    return {"missing": missing, "too_short": too_short}


if __name__ == "__main__":
    results = validate_documents()
    if results["missing"]:
        print("MISSING:")
        for f in results["missing"]:
            print(f"  {f}")
    if results["too_short"]:
        print("TOO SHORT (< 200 chars):")
        for f in results["too_short"]:
            print(f"  {f}")
    if not results["missing"] and not results["too_short"]:
        print("All 13 documents present and non-empty.")
