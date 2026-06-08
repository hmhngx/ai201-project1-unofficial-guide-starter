"""
Collects sample chunks and retrieval/generation results for README.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.ingest import build_chunks
from scripts.embed import build_index, load_collection
from scripts.retrieve import retrieve
from scripts.query import ask

SEP = "=" * 70

# ── Sample chunks ────────────────────────────────────────────────────────────
chunks = build_chunks()

print(SEP)
print("SAMPLE CHUNKS (one per source type)")
print(SEP)

# Find first chunk from each source
seen = {}
for c in chunks:
    src = c["source"]
    if src not in seen:
        seen[src] = c

for src, c in seen.items():
    print(f"\n[source: {src}]  file: {c['file_path']}")
    print(f"text ({len(c['text'])} chars):")
    print(c["text"][:500])
    print("---")

# Show a 6th chunk from reddit that has actual content (not a thread header)
for c in chunks:
    if c["source"] == "reddit" and len(c["text"]) > 200 and "workload" in c["text"].lower():
        print(f"\n[source: reddit (workload sample)]  file: {c['file_path']}")
        print(f"text ({len(c['text'])} chars):")
        print(c["text"][:500])
        print("---")
        break

# ── Retrieval test queries ───────────────────────────────────────────────────
collection = load_collection()

RETRIEVAL_QUERIES = [
    "Is CS 170 considered one of the harder upper-division CS courses at Berkeley?",
    "What do students say about CS 61B projects and workload?",
    "What should I know before taking CS 189?",
]

print("\n" + SEP)
print("RETRIEVAL TEST RESULTS")
print(SEP)

for q in RETRIEVAL_QUERIES:
    results = retrieve(q, collection, k=5)
    print(f"\nQUERY: {q}")
    for i, r in enumerate(results, 1):
        print(f"  Rank {i} [{r['distance']:.4f}] (source: {r['source']}, file: {r['file_path'].split('/')[-1]})")
        print(f"    {r['text'][:200]!r}")
    print()

# ── Example grounded responses ───────────────────────────────────────────────
RESPONSE_QUERIES = [
    "Is CS 170 considered one of the harder upper-division CS courses at Berkeley?",
    "What should students know before enrolling in CS 189?",
    "What is the best pizza place near UC Berkeley campus?",  # out-of-domain
]

print(SEP)
print("EXAMPLE RESPONSES")
print(SEP)

for q in RESPONSE_QUERIES:
    result = ask(q)
    print(f"\nQUESTION: {q}")
    print(f"ANSWER:\n{result['answer']}")
    print(f"SOURCES: {result['sources']}")
    print()
