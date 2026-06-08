"""
Milestone 6 evaluation — run all 5 planning.md test questions through the full RAG pipeline.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.query import ask

EVAL_QUESTIONS = [
    {
        "id": 1,
        "question": "What do students say about the workload in CS 61B?",
        "expected": "Heavy but manageable; projects take 15–25 hrs each; exams are fair if you keep up with projects",
    },
    {
        "id": 2,
        "question": "Is CS 170 considered one of the harder upper-division CS courses at Berkeley?",
        "expected": "Yes — consistently described as theory-heavy with difficult exams; students recommend taking it with a study group",
    },
    {
        "id": 3,
        "question": "Which CS 61A professor is known for clear explanations?",
        "expected": "John DeNero is most consistently praised; his lecture videos are the most frequently recommended resource",
    },
    {
        "id": 4,
        "question": "What do HKN guides say about how to prepare for CS 61B exams?",
        "expected": "Study past exams, understand runtime complexity, don't skip labs",
    },
    {
        "id": 5,
        "question": "Do students recommend taking CS 189 before or after CS 170?",
        "expected": "Most say after 170 — linear algebra and probability need to be solid first",
    },
    {
        "id": 6,
        "question": "What dining hall at UC Berkeley has the best vegetarian options?",
        "expected": "[OUT OF DOMAIN — system should decline to answer]",
    },
]


def main():
    for q in EVAL_QUESTIONS:
        print(f"\n{'='*70}")
        print(f"Q{q['id']}: {q['question']}")
        print(f"Expected: {q['expected']}")
        print("-" * 70)
        result = ask(q["question"])
        print(f"ANSWER:\n{result['answer']}")
        print(f"\nSOURCES: {result['sources']}")
        print(f"\nTOP CHUNKS (distance, source, text[:120]):")
        for c in result["chunks"]:
            print(f"  [{c['distance']:.4f}] ({c['source']}) {c['text'][:120]!r}")


if __name__ == "__main__":
    main()
