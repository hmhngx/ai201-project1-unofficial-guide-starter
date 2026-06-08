# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

UC Berkeley CS professor and course reviews — student-generated opinions on teaching style, exam difficulty, workload, and course sequencing shared on Reddit, Rate My Professors, and course-specific forums. This knowledge is valuable because official sources like the course catalog describe content but never reflect what it's actually like to take the course or learn from a specific instructor. It's hard to find because it's fragmented across dozens of subreddits and buried in old threads with no unified search.

---

## Documents

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Rate My Professors — UC Berkeley CS | Short professor reviews (2–5 sentences each) | https://www.ratemyprofessors.com/school/1072 |
| 2 | r/berkeley — CS 61A professor thread | Reddit thread: student recommendations for CS 61A instructors | https://www.reddit.com/r/berkeley (search: "CS 61A professor") |
| 3 | r/cs61a — advice and megathread | Reddit: tips, workload, exam advice for CS 61A | https://www.reddit.com/r/cs61a |
| 4 | r/cs61b — professor and exam discussion | Reddit: CS 61B workload, projects, professor opinions | https://www.reddit.com/r/cs61b |
| 5 | r/berkeley — CS 170 difficulty thread | Reddit thread on CS 170 exams and difficulty | https://www.reddit.com/r/berkeley (search: "CS 170") |
| 6 | r/berkeley — best CS professors thread | Reddit: general recommendations for CS professors | https://www.reddit.com/r/berkeley (search: "best CS professors") |
| 7 | HKN Course Guide — CS 61A | Long-form student-written course guide | https://hkn.eecs.berkeley.edu/courseguides |
| 8 | HKN Course Guide — CS 61B | Long-form student-written course guide | https://hkn.eecs.berkeley.edu/courseguides |
| 9 | HKN Course Guide — CS 170 | Long-form student-written course guide | https://hkn.eecs.berkeley.edu/courseguides |
| 10 | Berkeleytime reviews — CS 189 (Machine Learning) | Aggregated student course reviews | https://berkeleytime.com |
| 11 | Berkeleytime reviews — CS 61C | Aggregated student course reviews | https://berkeleytime.com |
| 12 | r/berkeley — CS workload tier list | Reddit thread ranking CS courses by workload | https://www.reddit.com/r/berkeley (search: "CS workload tier list") |
| 13 | r/berkeley — enrollment and course selection tips | Reddit thread on course sequencing and registration advice | https://www.reddit.com/r/berkeley (search: "CS course selection") |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about the workload in CS 61B? | Heavy but manageable; projects take 15–25 hrs each; exams are fair if you keep up with projects |
| 2 | Is CS 170 considered one of the harder upper-division CS courses? | Yes — consistently described as theory-heavy with difficult exams; students recommend taking it with a study group |
| 3 | Which CS 61A professor is known for clear explanations? | Specific instructor names drawn from RMP and Reddit reviews |
| 4 | What do HKN guides say about how to prepare for CS 61B exams? | Study past exams, understand runtime complexity, don't skip labs |
| 5 | Do students recommend taking CS 189 before or after CS 170? | Most say after — linear algebra and probability need to be solid first (implicit across multiple sources, no single document states this directly) |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
