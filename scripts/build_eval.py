"""
Milestone 4 integration: build real index + run eval queries.
Run with: python scripts/build_eval.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.ingest import build_chunks
from scripts.embed import build_index
from scripts.retrieve import retrieve

EVAL_QUERIES = [
    "What do students say about the workload in CS 61B?",
    "Is CS 170 considered one of the harder upper-division CS courses?",
    "Which CS 61A professor is known for clear explanations?",
]

def main():
    print("Building chunks...")
    chunks = build_chunks()
    print(f"  -> {len(chunks)} chunks")
    assert len(chunks) == 147, f"Expected 147 chunks, got {len(chunks)}"

    print("Building index...")
    collection = build_index(chunks)
    print(f"  -> {collection.count()} documents indexed")

    print("\nRunning eval queries:")
    all_pass = True
    for query in EVAL_QUERIES:
        results = retrieve(query, collection, k=5)
        top_dist = results[0]["distance"]
        top_src = results[0]["source"]
        status = "PASS" if top_dist < 0.5 else "FAIL"
        if top_dist >= 0.5:
            all_pass = False
        print(f"  {status} [{top_dist:.4f}] {query[:60]}")
        print(f"      source={top_src}  text={results[0]['text'][:80]!r}")

    if all_pass:
        print("\nAll eval queries passed (distance < 0.5)")
    else:
        print("\nSome eval queries FAILED (distance >= 0.5)")
        sys.exit(1)

if __name__ == "__main__":
    main()
