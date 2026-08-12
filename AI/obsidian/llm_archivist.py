"""Turning story text into 5W1H case files and entity profiles via an LLM.

`CaseArchivist` owns the conversation with the model: chunking a story, asking
for notes on each chunk, condensing when the notes outgrow the merge budget, and
merging them into six facts. It also profiles a character or place from the case
notes of every story it appears in.

Nothing here is author-specific -- the prompts and the canon's name are passed
in, so one implementation serves every author.

The module-level parsers are separate from the class on purpose: they are pure
functions over the model's reply text and are the part most worth testing
directly, since small models format their answers loosely.
"""

import re
import time
from collections.abc import Iterable

import openai

CHUNK_CHARS = 12_000
MERGE_INPUT_CHARS = 20_000
MAX_ATTEMPTS = 3
ENTITY_CONTEXT_MAX_STORIES = 12

FACT_RE = re.compile(r"^(WHO|WHAT|HOW|WHERE|WHEN|WHY)\s*:\s*(.+)$", re.IGNORECASE)
FACT_KEYS = ("who", "what", "how", "where", "when", "why")
LIST_FACT_KEYS = ("who", "where")
PROFILE_RE = re.compile(r"^(DESCRIPTION|IMPORTANCE)\s*:\s*(.+)$", re.IGNORECASE)
PROFILE_KEYS = ("description", "importance")
SUMMARY_RE = re.compile(r"^SUMMARY\s*:\s*(.+)$", re.IGNORECASE)

# Small models sometimes run two fields onto one line. Only ALL-CAPS labels are
# split back out, so ordinary prose ("the question was how: ...") is untouched.
FACT_INLINE_RE = re.compile(r"\b(?:WHO|WHAT|HOW|WHERE|WHEN|WHY)\s*:")
PROFILE_INLINE_RE = re.compile(r"\b(?:DESCRIPTION|IMPORTANCE)\s*:")

NOT_EXTRACTED = "(not extracted)"


def normalize_text(text: str) -> str:
    return (
        text.replace("’", "'")
        .replace("‘", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace("—", "-")
        .replace("–", "-")
        .replace("‑", "-")
        .replace("\xa0", " ")
    )


def isolate_labels(text: str, inline: re.Pattern) -> str:
    """Move run-on field labels onto their own line so the parsers can see them.

    A reply like "DESCRIPTION: a detective. IMPORTANCE: he solves it" would
    otherwise lose everything after the first label, because the field patterns
    are anchored to the start of a line.
    """
    return inline.sub(lambda m: "\n" + m.group(0), normalize_text(text))


def _clean_line(raw: str) -> str:
    """Strip bullets, numbering and bold markers the model may add."""
    return raw.strip().lstrip("-*").lstrip("0123456789.) ").strip().replace("**", "")


def split_chunks(text: str, limit: int = CHUNK_CHARS) -> list[str]:
    """Split on paragraph boundaries, keeping each chunk under `limit` chars."""
    chunks: list[str] = []
    current: list[str] = []
    size = 0
    for para in text.split("\n\n"):
        if len(para) > limit:
            if current:
                chunks.append("\n\n".join(current))
                current, size = [], 0
            chunks.extend(para[i : i + limit] for i in range(0, len(para), limit))
            continue
        if size and size + len(para) > limit:
            chunks.append("\n\n".join(current))
            current, size = [], 0
        current.append(para)
        size += len(para) + 2
    if current:
        chunks.append("\n\n".join(current))
    return chunks


def parse_chunk_reply(text: str) -> tuple[str, str]:
    """Split a chunk reply into its SUMMARY line(s) and the remaining notes."""
    summary_parts: list[str] = []
    notes: list[str] = []
    for raw in normalize_text(text).splitlines():
        line = _clean_line(raw)
        m = SUMMARY_RE.match(line)
        if m:
            summary_parts.append(m.group(1).strip())
        elif line:
            notes.append(line)
    return " ".join(summary_parts), "\n".join(notes)


def split_list(value: str) -> list[str]:
    """Split a comma-separated field, ignoring commas inside brackets.

    Models like to qualify an entry parenthetically -- "London streets (Rochester
    Row, Vauxhall Bridge Road)". Splitting on every comma tears that into two
    fragments with unbalanced brackets, each of which then becomes its own note.
    """
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    for ch in value:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth = max(0, depth - 1)
        if ch == "," and depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(ch)
    parts.append("".join(current))
    return [p.strip(" .") for p in parts if p.strip(" .")]


def parse_facts(text: str) -> dict:
    """Read a 6-line case file. WHO and WHERE become lists."""
    facts: dict[str, object] = {}
    for raw in isolate_labels(text, FACT_INLINE_RE).splitlines():
        line = _clean_line(raw)
        m = FACT_RE.match(line)
        if not m:
            continue
        key, value = m.group(1).lower(), m.group(2).strip()
        facts[key] = split_list(value) if key in LIST_FACT_KEYS else value
    return facts


def parse_profile(text: str) -> dict:
    """Read a 2-line entity profile."""
    profile: dict[str, str] = {}
    for raw in isolate_labels(text, PROFILE_INLINE_RE).splitlines():
        line = _clean_line(raw)
        m = PROFILE_RE.match(line)
        if m:
            profile[m.group(1).lower()] = m.group(2).strip()
    return profile


class CaseArchivist:
    """Asks an LLM for case files and entity profiles.

    `canon` names the body of work in the chunk prompts, e.g. "Agatha Christie"
    or "Sherlock Holmes". The three prompts are supplied by the caller because
    their wording is the one genuinely author-specific part of this stage.
    """

    def __init__(
        self,
        llm,
        *,
        canon: str,
        chunk_prompt: str,
        merge_prompt: str,
        entity_prompt: str,
        chunk_chars: int = CHUNK_CHARS,
        merge_input_chars: int = MERGE_INPUT_CHARS,
        max_attempts: int = MAX_ATTEMPTS,
        entity_context_max_stories: int = ENTITY_CONTEXT_MAX_STORIES,
    ) -> None:
        self.llm = llm
        self.canon = canon
        self.chunk_prompt = chunk_prompt
        self.merge_prompt = merge_prompt
        self.entity_prompt = entity_prompt
        self.chunk_chars = chunk_chars
        self.merge_input_chars = merge_input_chars
        self.max_attempts = max_attempts
        self.entity_context_max_stories = entity_context_max_stories

    def invoke(self, system: str, user: str) -> str:
        """One call to the model, retried on transport errors."""
        for attempt in range(1, self.max_attempts + 1):
            try:
                reply = self.llm.invoke([("system", system), ("user", user)])
                return (
                    reply.content
                    if isinstance(reply.content, str)
                    else str(reply.content)
                )
            except openai.APIError as e:
                print(
                    f"[attempt {attempt}/{self.max_attempts}] "
                    f"LLM call failed ({type(e).__name__}); retrying"
                )
                if attempt == self.max_attempts:
                    raise
                time.sleep(2)
        raise AssertionError("unreachable")

    def chunk_call(self, where: str, chunk: str) -> tuple[str, str]:
        reply = self.invoke(
            self.chunk_prompt.format(where=where),
            f"Story part:\n{chunk}\n\nYour fact notes:",
        )
        return parse_chunk_reply(reply)

    def extract_story(
        self, title: str, sections: list
    ) -> tuple[dict, list[list[str]], bool]:
        """Summarise every chunk of a story, then merge the notes into 6 facts.

        Returns the facts, a per-part summary, and whether the result was clean
        enough to cache.
        """
        plan = []
        for sec_title, sec_text in sections:
            chunks = split_chunks(sec_text, self.chunk_chars)
            for j, chunk in enumerate(chunks, 1):
                plan.append((sec_title, chunk, j, len(chunks)))
        total_chars = sum(len(sec_text) for _, sec_text in sections)
        print(f"[extract] {title} ({total_chars:,} chars, {len(plan)} chunks)")

        notes: list[str] = []
        summaries: list[list[str]] = []
        missing_summary = False
        for g, (sec_title, chunk, j, n) in enumerate(plan, 1):
            print(f"[chunk {g}/{len(plan)}] {title}")
            if sec_title:
                where = (
                    f'part {j} of {n} of the chapter "{sec_title}" '
                    f'of the {self.canon} novel "{title}"'
                )
            else:
                where = f'part {g} of {len(plan)} of the {self.canon} story "{title}"'
            summary, chunk_facts = self.chunk_call(where, chunk)
            notes.append(chunk_facts)
            if not summary:
                summary = NOT_EXTRACTED
                missing_summary = True
            label = sec_title or f"Part {g}"
            if summaries and summaries[-1][0] == label:
                summaries[-1][1] += " " + summary
            else:
                summaries.append([label, summary])

        joined = "\n".join(notes)
        while len(joined) > self.merge_input_chars:
            print(f"[condense] {title}: notes at {len(joined):,} chars")
            slices = split_chunks(joined, self.chunk_chars)
            joined = "\n".join(
                self.chunk_call(
                    f'part {i} of {len(slices)} of the {self.canon} story "{title}"', s
                )[1]
                for i, s in enumerate(slices, 1)
            )

        print(f"[merge] {title}")
        merge_user = f"Fact notes in story order:\n{joined}\n\nThe 6-line case file:"
        system = self.merge_prompt.format(title=title)
        facts = parse_facts(self.invoke(system, merge_user))
        if any(k not in facts for k in FACT_KEYS):
            facts = parse_facts(self.invoke(system, merge_user))

        facts_complete = all(k in facts for k in FACT_KEYS)
        if not facts_complete:
            for key in LIST_FACT_KEYS:
                facts.setdefault(key, [])
            for key in FACT_KEYS:
                facts.setdefault(key, NOT_EXTRACTED)
        elif missing_summary:
            print(f"[warn] {title}: a part summary came back empty")
        return facts, summaries, facts_complete and not missing_summary

    def describe_entity(
        self, kind: str, name: str, titles: list[str], stories_by_title: dict
    ) -> tuple[dict, bool]:
        """Profile one character or place from the cases it appears in."""
        noun = "character" if kind == "character" else "location"
        lines = [
            f"- {title}: {stories_by_title[title]['facts']['what']}"
            for title in titles[: self.entity_context_max_stories]
        ]
        if len(titles) > self.entity_context_max_stories:
            extra = len(titles) - self.entity_context_max_stories
            lines.append(f"(and {extra} more stories)")
        system = self.entity_prompt.format(kind=noun, name=name)
        user = "Case notes:\n" + "\n".join(lines) + "\n\nThe 2-line profile:"
        profile = parse_profile(self.invoke(system, user))
        if any(k not in profile for k in PROFILE_KEYS):
            profile = parse_profile(self.invoke(system, user))
        complete = all(k in profile for k in PROFILE_KEYS)
        if not complete:
            for key in PROFILE_KEYS:
                profile.setdefault(key, NOT_EXTRACTED)
        return profile, complete

    def count_chunks(self, sections: Iterable[tuple]) -> int:
        return sum(len(split_chunks(text, self.chunk_chars)) for _, text in sections)
