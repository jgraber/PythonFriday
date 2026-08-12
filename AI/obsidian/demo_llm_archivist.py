"""Minimal demo of `llm_archivist`, ending in a real call to the local model.

    uv run python demo_llm_archivist.py

Three parts, in increasing cost:

  1. The module-level parsers, fed the kind of sloppy reply a small model really
     produces. They are pure functions over reply text, so they are the part
     worth watching directly. Instant, deterministic.
  2. `CaseArchivist` driven by a stub model. `llm` is a constructor argument, so
     the whole chunk -> notes -> merge orchestration can be exercised with no
     server running and no waiting.
  3. The same class against LM Studio, using the Holmes script's own configured
     archivist: one `extract_story` and one `describe_entity` over a short
     passage, roughly a minute on a local 20B. Parts 1 and 2 have already run
     and printed by the time this starts, so a server that is down costs
     nothing but the last section.
"""

import time
from types import SimpleNamespace

import openai

from llm_archivist import (
    CaseArchivist,
    parse_chunk_reply,
    parse_facts,
    parse_profile,
    split_chunks,
)

# ---------------------------------------------------------------- the parsers

# Every deviation here is one a local 20B model actually makes: bold markers, a
# bullet, two fields run onto one line, and a comma inside parentheses.
MESSY_REPLY = """\
**WHO:** Sherlock Holmes, Dr. Watson, Mrs. Merrilow
- WHAT: A veiled lodger confesses. HOW: Holmes reads his marginal notes.
WHERE: London streets (Rochester Row, Vauxhall Bridge Road), Baker Street
WHEN: 1896
WHY: to escape an abusive husband
"""

facts = parse_facts(MESSY_REPLY)
print("parse_facts on a messy reply:")
for key, value in facts.items():
    print(f"  {key:6}: {value!r}")

# WHAT and HOW shared a line and both survived; WHERE stayed two entries rather
# than tearing the parenthetical into fragments with unbalanced brackets.
print(f"\n  WHERE split into {len(facts['where'])} entries, not 3")
print(f"  HOW recovered from a run-on line: {facts['how']!r}")

# A reply missing a field simply lacks the key. `extract_story` is what retries
# and then fills "(not extracted)", and reports complete=False so the cache
# refuses to store it.
partial = parse_facts("WHO: Holmes\nWHAT: something happened")
print(f"\n  incomplete reply -> keys {sorted(partial)} (no 'why')")

print("\nparse_chunk_reply splits the SUMMARY line from the notes:")
summary, notes = parse_chunk_reply(
    "SUMMARY: Holmes visits the lodger.\n1. Mrs. Ronder wears a veil\n* a lion escaped"
)
print(f"  summary: {summary!r}")
print(f"  notes  : {notes!r}")

print("\nparse_profile reads a 2-line entity profile, run-on labels and all:")
print(f"  {parse_profile('DESCRIPTION: A detective. IMPORTANCE: He solves it.')}")

# ------------------------------------------------------------- the archivist


class StubModel:
    """Stands in for `ChatOpenAI`: `invoke(messages)` -> object with `.content`."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    def invoke(self, messages: list) -> SimpleNamespace:
        user = messages[1][1]
        if "case file" in user:  # the merge call asks for the 6-line case file
            self.calls.append("merge")
            return SimpleNamespace(
                content=(
                    "WHO: Holmes, Watson\nWHAT: A test case.\nHOW: By deduction.\n"
                    "WHERE: Baker Street\nWHEN: 1896\nWHY: To demonstrate."
                )
            )
        self.calls.append("chunk")
        return SimpleNamespace(content="SUMMARY: Part summary.\n- one fact note")


model = StubModel()
archivist = CaseArchivist(
    model,
    canon="Demo Canon",
    chunk_prompt="You are reading {where}.",
    merge_prompt='Notes from "{title}". Reply with 6 lines.',
    entity_prompt='Profile the {kind} "{name}".',
    chunk_chars=120,  # tiny, so a short story still shows the chunking loop
)

story = [(None, "\n\n".join(f"Paragraph {i} of the story text." for i in range(1, 9)))]
print(
    f"\ncount_chunks: {archivist.count_chunks(story)} "
    f"(split_chunks keeps paragraphs whole under the limit)"
)
print(f"  first chunk: {split_chunks(story[0][1], 120)[0]!r}\n")

facts, summaries, complete = archivist.extract_story("A Test Case", story)
print(f"\nLLM calls made : {model.calls}")
print(f"facts          : {facts}")
print(f"summaries      : {summaries}")
print(f"complete       : {complete}  <- what JsonCache.put() keys off")

# ---------------------------------------------------------- the real model

# Everything above is deterministic. This last part talks to LM Studio, which
# has to be running and serving the model. Borrowing the Holmes script's own
# `archivist` rather than rebuilding one: it already carries the real prompts
# and the configured client, so this is the exact collaborator the pipeline
# uses -- importing it costs nothing but constructing that client.
from sherlock_holmes_import import archivist as holmes

TITLE = "A Scandal in Bohemia (excerpt)"
PASSAGE = """\
To Sherlock Holmes she is always the woman. I have seldom heard him mention her
under any other name. In his eyes she eclipses and predominates the whole of her
sex. It was not that he felt any emotion akin to love for Irene Adler. All
emotions, and that one particularly, were abhorrent to his cold, precise but
admirably balanced mind.

He was, I take it, the most perfect reasoning and observing machine that the
world has seen, but as a lover he would have placed himself in a false position.
He never spoke of the softer passions, save with a gibe and a sneer. They were
admirable things for the observer -- excellent for drawing the veil from men's
motives and actions. And yet for the trained reasoner to admit such intrusions
into his own delicate and finely adjusted temperament was to introduce a
distracting factor.
"""

print("\n" + "=" * 72)
print(f"live call -- {holmes.llm.model_name} @ {holmes.llm.openai_api_base}")
print("=" * 72)

try:
    start = time.perf_counter()
    live_facts, live_summaries, live_complete = holmes.extract_story(
        TITLE, [(None, PASSAGE)]
    )
    extract_seconds = time.perf_counter() - start

    print(f"\nextract_story in {extract_seconds:.1f}s | complete={live_complete}")
    for key in ("who", "what", "how", "where", "when", "why"):
        print(f"  {key.upper():6}: {str(live_facts.get(key))[:150]}")
    print(f"  summary: {live_summaries[0][1][:150]}")

    # The profiler is the module's other public method. It reads the WHAT of
    # every story an entity appears in, so the facts just extracted feed it.
    start = time.perf_counter()
    profile, profile_complete = holmes.describe_entity(
        "character", "Irene Adler", [TITLE], {TITLE: {"facts": live_facts}}
    )
    profile_seconds = time.perf_counter() - start

    print(f"\ndescribe_entity in {profile_seconds:.1f}s | complete={profile_complete}")
    for key in ("description", "importance"):
        print(f"  {key.upper():12}: {profile.get(key, '')[:150]}")

except openai.APIError as exc:
    print(
        f"\nLM Studio did not answer ({type(exc).__name__}).\n"
        "Start it on http://localhost:1234 with openai/gpt-oss-20b loaded, "
        "then re-run. Everything above this line ran without it."
    )
    raise SystemExit(1) from None
