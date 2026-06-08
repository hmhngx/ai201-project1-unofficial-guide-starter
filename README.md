# The Unofficial Guide — Project 1

---

## Domain

UC Berkeley CS professor and course reviews — student-generated opinions on teaching style,
exam difficulty, workload, and course sequencing shared on Reddit, Rate My Professors,
HKN course guides, and Berkeleytime. This knowledge is valuable because official sources
like the course catalog describe content but never reflect what it's actually like to take
the course or learn from a specific instructor. It's hard to find because it's fragmented
across dozens of subreddits and buried in old threads with no unified search.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Rate My Professors — UC Berkeley CS | Short professor reviews | https://www.ratemyprofessors.com/school/1072 |
| 2 | r/berkeley — CS 61A professor thread | Reddit thread | https://www.reddit.com/r/berkeley |
| 3 | r/cs61a — advice megathread | Reddit thread | https://www.reddit.com/r/cs61a |
| 4 | r/cs61b — professor and exam discussion | Reddit thread | https://www.reddit.com/r/cs61b |
| 5 | r/berkeley — CS 170 difficulty thread | Reddit thread | https://www.reddit.com/r/berkeley |
| 6 | r/berkeley — best CS professors thread | Reddit thread | https://www.reddit.com/r/berkeley |
| 7 | HKN Course Guide — CS 61A | Long-form student guide | https://hkn.eecs.berkeley.edu/courseguides |
| 8 | HKN Course Guide — CS 61B | Long-form student guide | https://hkn.eecs.berkeley.edu/courseguides |
| 9 | HKN Course Guide — CS 170 | Long-form student guide | https://hkn.eecs.berkeley.edu/courseguides |
| 10 | Berkeleytime — CS 189 reviews | Aggregated course reviews | https://berkeleytime.com |
| 11 | Berkeleytime — CS 61C reviews | Aggregated course reviews | https://berkeleytime.com |
| 12 | r/berkeley — CS workload tier list | Reddit thread | https://www.reddit.com/r/berkeley |
| 13 | r/berkeley — CS course selection tips | Reddit thread | https://www.reddit.com/r/berkeley |

---

## Chunking Strategy

**Chunk size:** 500 characters

**Overlap:** 50 characters

**Why these choices fit your documents:**

The corpus contains three structurally different document types that pull in different
directions. RMP and Berkeleytime reviews are short (150–400 chars each) and self-contained:
one professor or one course per comment. Reddit comments are similar in length. HKN guides
are long-form (500–2000 words) with section headings and continuous prose. A 500-character
chunk fits one complete short review and about 3–4 sentences of guide text — large enough
to capture a complete thought, small enough to isolate individual opinions and avoid mixing
two separate professors in one chunk.

Splitting strategy is paragraph-first (on `\n\n`) before falling back to character count.
This keeps each Reddit comment and each review sentence in its own chunk without mid-sentence
cuts. The 50-character overlap bridges chunk boundaries in HKN guides, where a key fact
(e.g. "exams focus on runtime analysis") might span the end of one chunk and the start of the
next. Short reviews don't benefit from overlap, but the HKN long-form content does — 50 chars
is the compromise that handles both without excessive duplication.

Preprocessing (`clean_text()`) strips structural boilerplate from every document:
`SOURCE:`, `URL:`, and `TITLE:` header lines; section dividers (`---`, `===`);
Reddit username prefixes (`u/username:`); and thread-structure labels
(`POST:`, `COMMENTS:`, `REVIEWS:`, `NOTE:`). This prevents metadata fragments from
landing in chunks where they would confuse the embedding model.

**Final chunk count:** 147 chunks across 13 documents.

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers` (local, no API cost).
Produces 384-dimensional embeddings. Our 500-character chunks average roughly 100–130 tokens,
well within the model's 256-token context limit.

**Production tradeoff reflection:**

For a real deployment with no cost constraint, the main tradeoffs are accuracy vs. latency
vs. domain fit. `text-embedding-3-large` (OpenAI) offers noticeably better semantic accuracy
on English prose — particularly for paraphrase recognition — but adds per-call API cost and
network latency that would be unacceptable in an interactive UI. `e5-large-v2` runs locally
with stronger retrieval performance than MiniLM (higher BEIR benchmark scores) at the cost of
a heavier model download and ~4× slower inference on CPU. Neither model was fine-tuned on
CS course review text, so both would likely struggle with jargon ("Gitlet", "NP-reduction",
"HKN") that doesn't appear in their training corpora.

The core limitation of `all-MiniLM-L6-v2` for this specific task is **attribution sensitivity**:
when a professor's name is stripped from the surrounding chunk context (because the review
header was cleaned away), the model has no way to encode "this chunk is about DeNero" — it
encodes only the review text. A fine-tuned model or one with longer context could preserve
that connection.

---

## Grounded Generation

**System prompt grounding instruction:**

The system prompt enforces grounding with explicit prohibitions — not just suggestions:

> "Answer the question using ONLY the information provided in the context documents below.
> Do not use any knowledge outside of the provided context.
> If the context does not contain enough information to answer the question, you MUST respond
> with exactly: 'I don't have enough information on that.'
> Do not guess. Do not infer. Do not use general knowledge. Every factual claim in your answer
> must come directly from the context."

The word "ONLY" is bolded in the internal constant, the fallback phrase is prescribed verbatim,
and the instruction lists four specific prohibited behaviors (guess, infer, general knowledge,
unsupported claims). This is a hard prohibition, not a soft suggestion.

**How source attribution is surfaced in the response:**

Source attribution is **programmatic** — it does not rely on the LLM to produce citations.
Before the Groq API call, `generate()` extracts the `source` field from every retrieved chunk
via `list(dict.fromkeys(c["source"] for c in chunks))`. This list is deduplicated (preserving
insertion order) and returned as `result["sources"]` alongside the answer. The Gradio UI
displays it in a separate "Sources" panel beneath the answer. Even if the model generates an
answer that omits attribution, the sources field is always populated from the retrieval
metadata — the model cannot suppress or fabricate it.

---

## Evaluation Report

The following results were produced by running `scripts/run_eval.py` against the live system
(Groq `llama-3.3-70b-versatile`, ChromaDB with 147 chunks, top-k=5). All responses are
verbatim from the system output; source lists and top-chunk distances are recorded from the
retrieval metadata.

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about the workload in CS 61B? | Heavy but manageable; projects take 15–25 hrs each; exams are fair if you keep up with projects | "I don't have enough information on that." Sources: reddit, hkn. Top chunk (0.3380): CS 61B thread intro text, not workload specifics. | Partially relevant | Inaccurate |
| 2 | Is CS 170 considered one of the harder upper-division CS courses at Berkeley? | Yes — theory-heavy; difficult exams; study groups recommended | "According to the context, some people say CS 170 is 'the hardest proof-based class in the CS department'..." Sources: hkn, reddit, berkeleytime. Top chunk distance 0.20. | Relevant | Accurate |
| 3 | Which CS 61A professor is known for clear explanations? | John DeNero; lecture videos most frequently recommended | "I don't have enough information on that." Sources: rmp, reddit. Top chunk (0.4162): About Prof. Shewchuk / CS 189, not DeNero. DeNero chunk appeared at rank 4 (0.4597). | Off-target | Inaccurate |
| 4 | What do HKN guides say about how to prepare for CS 61B exams? | Study past exams; understand runtime complexity; don't skip labs | "I don't have enough information on that." Sources: reddit, berkeleytime, hkn. Top HKN chunk (0.4534) is the CS 61B course overview header, not the exam prep section. | Partially relevant | Inaccurate |
| 5 | Do students recommend taking CS 189 before or after CS 170? | Most say after CS 170 — linear algebra and probability must be solid first | "I don't have enough information on that." Sources: reddit, hkn, berkeleytime. Chunks mention CS 189 and CS 170 in proximity but never directly address sequencing. | Partially relevant | Inaccurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

**Overall:** 1 of 5 questions answered correctly (Q2). The system correctly declined the
out-of-domain dining-hall query ("I don't have enough information on that.") with retrieval
distances of 0.59–0.67 — significantly higher than in-domain queries (0.20–0.47) — showing
that the distance signal is a useful proxy for domain coverage even when not used as a filter.

---

## Failure Case Analysis

**Question that failed:**

Q3: "Which CS 61A professor is known for clear explanations?"

**What the system returned:**

> "I don't have enough information on that."

Sources returned: `['rmp', 'reddit']`. The relevant DeNero content *was* retrieved — a chunk
at rank 4 (distance 0.4597) containing: *"be afraid of office hours: DeNero is awesome." From
a tutoring perspective, the single most common mistake students make"* — but the system still
declined.

**Root cause (tied to a specific pipeline stage):**

The failure occurs at two pipeline stages simultaneously:

1. **Ingestion / clean_text() — attribution context loss.** The RMP document stores reviews
   under structural headers like `=== Professor: John DeNero ===`. The `clean_text()` function
   was designed to strip boilerplate lines, and it correctly strips separator lines matching
   `^[-=]{3,}$`. However, this means the professor name appearing *as part of a separator
   header* is not preserved in any chunk. A chunk containing DeNero's review text ("His lecture
   videos are so good", "makes everything super clear") is embedded without the words "John
   DeNero" or "CS 61A professor" appearing in it. The embedding for that chunk encodes *the
   sentiment of the review*, not *who the review is about*.

2. **Retrieval — wrong top result due to missing attribution.** When the query "Which CS 61A
   professor is known for clear explanations?" is embedded and compared to the collection, the
   top result (distance 0.4162) is a chunk from the RMP file about **Professor Shewchuk** (CS
   189): *"made himself available during office hours. CS189 is hard but Prof. Shewchuk was a
   great lecturer for this course."* This chunk explicitly names the professor and course in its
   text, so its embedding strongly encodes "professor + lecturer + good". The DeNero chunks
   don't include his name in the chunk text, so they rank lower. The LLM receives a context
   dominated by Shewchuk/CS189 content and correctly identifies that this doesn't answer the
   question about CS 61A, so it declines.

This is precisely the "Anticipated Challenge #2" from `planning.md`: *"Short review chunks
losing attribution context. A review saying 'He's the best — explains everything clearly' is
useless without the professor's name from the surrounding header."* The spec anticipated the
problem but the fix (prepending professor/course context to each chunk) was not implemented.

**What you would change to fix it:**

In `build_chunks()` in `scripts/ingest.py`, detect `=== Professor: X ===` and `=== Course: X ===`
headers before stripping them, and prepend their content to every chunk produced from that
document section. For example, a DeNero review chunk would become:
`"[Professor: John DeNero, CS 61A] His lecture videos are so good that the official course page
says to watch them at the bare minimum..."`. This keeps the professor name in the chunk text,
so the embedding encodes it, so queries about DeNero rank DeNero chunks first.

---

## Spec Reflection

**One way the spec helped you during implementation:**

The `planning.md` Chunking Strategy section forced an explicit decision about paragraph-first
splitting before implementation began. That decision directly shaped `chunk_text()`: the
function tries to split on `\n\n` before falling back to character-level cutting, which is
why short Reddit comments and RMP reviews almost always land in their own chunks rather than
being fused with unrelated content. Without writing down the reasoning — "Reddit comments are
independent opinions; splitting mid-comment loses meaning" — it would have been easy to default
to a simple character-split loop. The spec made the tradeoff explicit and concrete, so the
implementation followed a deliberate design rather than an accidental one.

**One way your implementation diverged from the spec, and why:**

The spec's Anticipated Challenge #2 identified attribution loss as a known risk and proposed
prepending header context to chunks as the fix: *"The fix is to prepend each chunk with its
source file and professor/course context at ingestion time."* The implementation did not do
this. The `clean_text()` function strips separator headers (`=== Professor: X ===`) without
extracting and forwarding the professor name into the downstream chunks. The reason the fix
wasn't applied is that the ingestion pipeline was built incrementally through TDD — each
function was tested in isolation, and the test suite for `chunk_text()` used synthetic
single-document inputs that didn't exercise the cross-section attribution problem. The
integration test (`build_chunks()` producing 147 chunks with correct text) didn't catch it
because no test verified that professor names were preserved in the output text. The evaluation
surfaced this gap exactly as anticipated.

---

## AI Usage

**Instance 1: Generating the ingestion pipeline from the chunking strategy**

- *What I gave the AI:* The complete Chunking Strategy section from `planning.md` (chunk size
  500 chars, overlap 50, paragraph-first splitting, motivation for each choice) plus the actual
  format of the `.txt` documents (showing the `=== Professor: X ===` header format, `---`
  separators, and `u/username:` Reddit prefixes). I asked Claude to implement `clean_text()`,
  `chunk_text()`, and `load_documents()` matching those exact specifications.

- *What it produced:* A complete `scripts/ingest.py` with all three functions, plus an initial
  test suite. The core paragraph-split logic was correct. However, the initial `chunk_text()`
  had an overflow bug: when the overlap tail plus a new paragraph produced a buffer exactly
  512 characters (exceeding the 500-char limit), no extra split was applied. The initial
  `clean_text()` also missed Berkeleytime-specific labels (`REVIEWS:`, `NOTE:`) and had a
  regex too narrow for hyphenated Reddit usernames (`\w+` vs `[\w-]+`).

- *What I changed or overrode:* I directed Claude to fix each bug one at a time through a TDD
  loop: write the failing test first, then patch the specific case. The overflow fix required
  adding a guard that checks whether a seeded buffer already exceeds `chunk_size` before
  entering the overlap-concatenation path. The username fix required expanding the regex
  character class. These were targeted corrections to specific failure modes the test suite
  surfaced — not rewrites.

**Instance 2: Generating the Groq generation layer from the grounding requirement**

- *What I gave the AI:* The Grounded Generation requirement ("answer ONLY from retrieved
  context, cite source for every claim, say 'I don't have enough information' if context is
  insufficient"), the `retrieve()` output schema (`list[dict]` with `text/source/file_path/
  distance`), and a description of how source attribution should be programmatic rather than
  LLM-generated.

- *What it produced:* A complete `scripts/generate.py` with `SYSTEM_PROMPT`, `generate()`,
  and mocked tests. The system prompt used the correct "ONLY" language. Source extraction
  via `dict.fromkeys()` was present. The initial draft used `temperature=0.0`, which I changed
  to `temperature=0.1` to avoid degenerate repetition that occasionally appears at zero
  temperature with instruction-tuned models. The initial draft also initialized `Groq()` with
  `api_key=os.environ["GROQ_API_KEY"]` (hard KeyError if .env not loaded), which I changed
  to `os.environ.get("GROQ_API_KEY", "")` so that tests using mocked Groq don't require a
  real environment variable to be set.
