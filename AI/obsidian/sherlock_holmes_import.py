import datetime
import hashlib
import re
import sys
import time
import urllib.request
from collections.abc import Iterable
from pathlib import Path
from typing import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from gutenberg_epub import (
    EpubBook,
    Section,
    TocEntry,
    is_front_matter,
    merge_leads,
    prettify_caps,
    safe_filename,
)
from json_cache import JsonCache
from llm_archivist import CaseArchivist
from vault import NameCanonicalizer, VaultWriter, slug

sys.stdout.reconfigure(encoding="utf-8")

llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="openai/gpt-oss-20b",
    temperature=0.1,
)

# =====================================================================
# Settings & Configuration
# =====================================================================

BOOKS_DIR = Path("holmes_books")
VAULT = Path("Sherlock_Holmes_Canon")
CACHE_FILE = Path("holmes_extractions.json")
ENTITY_CACHE_FILE = Path("holmes_entities.json")
UA = {"User-Agent": "Mozilla/5.0"}
CREATED = datetime.datetime.now(tz=datetime.UTC).astimezone().date().isoformat()

MIN_STORY_WORDS = 1000

BOOKS = {
    "study_in_scarlet.epub": "https://www.gutenberg.org/ebooks/244.epub3.images",
    "sign_of_the_four.epub": "https://www.gutenberg.org/ebooks/2097.epub3.images",
    "adventures_of_sherlock_holmes.epub": "https://www.gutenberg.org/ebooks/1661.epub3.images",
    "memoirs_of_sherlock_holmes.epub": "https://www.gutenberg.org/ebooks/834.epub3.images",
    "hound_of_the_baskervilles.epub": "https://www.gutenberg.org/ebooks/2852.epub3.images",
    "return_of_sherlock_holmes.epub": "https://www.gutenberg.org/ebooks/108.epub3.images",
    "valley_of_fear.epub": "https://www.gutenberg.org/ebooks/3289.epub3.images",
    "his_last_bow.epub": "https://www.gutenberg.org/ebooks/2350.epub3.images",
    "case_book_of_sherlock_holmes.epub": "https://www.gutenberg.org/ebooks/69700.epub3.images",
}

CHAPTER_RE = re.compile(r"^chapter\s+[ivxlc\d]+\b", re.IGNORECASE)
NOVEL_PART_RE = re.compile(
    r"^(chapter|part|prologue|epilogue|introduction)\b", re.IGNORECASE
)
SUB_ENTRY_RE = re.compile(
    r"^([ivxlc]+\.?|part\s+[ivxlc\d]+\.?|chapter\s+[ivxlc\d]+.*|\d+\..*)$",
    re.IGNORECASE,
)
ROMAN_PREFIX_RE = re.compile(r"^[IVXLC]+\.?\s+")
MIN_SECTION_WORDS = 20

HONORIFICS = {
    "mr",
    "mrs",
    "ms",
    "miss",
    "dr",
    "doctor",
    "sir",
    "lord",
    "lady",
    "inspector",
    "colonel",
    "major",
    "professor",
}
PERSON_ALIASES = {
    "holmes": "Sherlock Holmes",
    "sherlock": "Sherlock Holmes",
    "sherlock holmes": "Sherlock Holmes",
    "watson": "Dr. Watson",
    "john watson": "Dr. Watson",
    "john h. watson": "Dr. Watson",
    "lestrade": "Inspector Lestrade",
    "g. lestrade": "Inspector Lestrade",
}
PLACE_ALIASES = {
    "221b": "221B Baker Street",
    "baker street": "221B Baker Street",
    "221b baker street": "221B Baker Street",
}

names = NameCanonicalizer(HONORIFICS, PERSON_ALIASES, PLACE_ALIASES)

# =====================================================================
# Prompts
# =====================================================================

CHUNK_PROMPT = """\
You are reading {where}.
Write about ONLY what this part states. Reply with one SUMMARY line followed
by fact notes, nothing else, no preamble:
SUMMARY: <two to ten sentences: what happens in this part>
Then AT MOST 8 more lines, one fact per line, each under 20 words, no
numbering. Cover, if present in this part: characters and their roles, the
crime or mystery, locations, dates or time references, key clues, and any
revelation of who did it, how it was done, or why.
"""

MERGE_PROMPT = """\
You are a case archivist. Below are sequential fact notes from the Sherlock
Holmes story "{title}". Combine them into one case file. Reply with EXACTLY
6 lines in this format and nothing else, no numbering, no preamble:
WHO: <up to 10 most important characters, comma-separated, full names>
WHAT: <three to 10 sentences: the crime or mystery of the case>
HOW: <one to five sentence: how Holmes solved it or how the crime was done>
WHERE: <2 to 7 key locations, comma-separated>
WHEN: <the time period or dates mentioned, one short phrase>
WHY: <one to five sentences: the culprit's motive>
"""

ENTITY_PROMPT = """\
You are a Sherlock Holmes canon archivist. Below are case notes from every
story in which the {kind} "{name}" appears. Reply with EXACTLY 2 lines in
this format and nothing else, no preamble:
DESCRIPTION: <2-5 sentences: who this character is / what this place is>
IMPORTANCE: <1-5 sentences: why this {kind} matters in these stories>
Base your answer on the notes plus well-known canon facts. Even when the
notes say little, never leave a line empty - state what kind of {kind} this
is and its brief role in the story.
"""

# =====================================================================
# State & Helpers
# =====================================================================


class VaultState(TypedDict):
    books_data: dict[str, list]
    cache: dict[str, dict]
    entities: dict[str, dict]
    vault_status: str


def looks_like_novel(entries: Iterable[TocEntry]) -> bool:
    """Doyle's editions are uniform enough to tell a novel from a collection.

    A handful of "Chapter N" entries means the whole book is one case; a list of
    story titles means it is a collection.
    """
    return sum(1 for e in entries if CHAPTER_RE.match(e.label)) >= 3


def group_novel(book_title: str, sections: Iterable[Section]) -> list[list]:
    """Fold every section of a novel into one story unit, chapter by chapter."""
    stories: list[list] = []
    pending = ""

    for section in sections:
        if section.is_lead:
            # `merge_leads` already folded every lead that had a section to join,
            # so anything still flagged came before chapter one: hold it for it.
            pending = f"{pending}\n\n{section.text}".strip()
            continue

        seg = section.text
        if len(seg.split()) < MIN_SECTION_WORDS:
            pending = f"{pending}\n\n{seg}".strip()
            continue
        if pending:
            seg = f"{pending}\n\n{seg}"
            pending = ""
        if not stories:
            stories.append([safe_filename(book_title), []])
        stories[0][1].append([prettify_caps(section.label), seg])
    return stories


def group_stories(sections: Iterable[Section]) -> list[list]:
    """Split a collection into one story unit per top-level toc entry."""
    stories: list[list] = []
    for section in sections:
        if section.is_lead:
            continue  # a lead `merge_leads` could not place has no story to join
        if SUB_ENTRY_RE.match(section.label) and stories:
            # A sub-entry continues the story above it rather than starting one.
            stories[-1][1][-1][1] += "\n\n" + section.text
        else:
            title = prettify_caps(ROMAN_PREFIX_RE.sub("", section.label))
            stories.append([safe_filename(title), [[None, section.text]]])
    return stories


def read_epub(path: Path) -> tuple[str, list[tuple[str, str]]]:
    with EpubBook(path) as book:
        book_title = book.title
        booklow = book_title.lower().strip(" .")

        def wanted(entry: TocEntry) -> bool:
            return (
                not is_front_matter(entry.label)
                and entry.label.lower().strip(" .") != booklow
            )

        is_novel = looks_like_novel(e for e in book.toc() if wanted(e))
        if is_novel:

            def keep(entry: TocEntry) -> bool:
                return wanted(entry) and bool(NOVEL_PART_RE.match(entry.label))
        else:
            keep = wanted

        sections = merge_leads(book.sections(keep=keep))
        stories = (
            group_novel(book_title, sections) if is_novel else group_stories(sections)
        )

    result = []
    for title, story_sections in stories:
        words = sum(len(text.split()) for _, text in story_sections)
        if words < MIN_STORY_WORDS:
            print(f"[skip] {title} ({words} words, under {MIN_STORY_WORDS})")
            continue
        result.append((title, story_sections))
    return book_title, result


def download_books() -> None:
    BOOKS_DIR.mkdir(exist_ok=True)
    for filename, url in BOOKS.items():
        target = BOOKS_DIR / filename
        if not target.exists() or target.stat().st_size == 0:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as resp:
                target.write_bytes(resp.read())
            time.sleep(1)


# =====================================================================
# Nodes
# =====================================================================

archivist = CaseArchivist(
    llm,
    canon="Sherlock Holmes",
    chunk_prompt=CHUNK_PROMPT,
    merge_prompt=MERGE_PROMPT,
    entity_prompt=ENTITY_PROMPT,
)


def ingestion_agent_node(state: VaultState) -> VaultState:
    """Ingestion Agent downloads canon books and parses EPUB structure."""
    print("--- [Agent: Ingestion] Fetching & Reading EPUB files ---")
    download_books()

    # Iterate BOOKS rather than globbing the directory: the glob imported any
    # stray epub sitting there and ignored BOOKS entirely, and it ordered books
    # alphabetically by filename instead of by publication date.
    parsed_books = {}
    for filename in BOOKS:
        book_title, book_stories = read_epub(BOOKS_DIR / filename)
        parsed_books[book_title] = book_stories
        print(f"[book] {book_title}: {len(book_stories)} stories found")

    state["books_data"] = parsed_books
    return state


def extraction_agent_node(state: VaultState) -> VaultState:
    """Extraction Agent extracts 5W1H facts and generates extractions.json cache."""
    print("--- [Agent: Extractor] Synthesizing 5W1H Case Files ---")
    cache = JsonCache(CACHE_FILE)

    for book_title, book_stories in state["books_data"].items():
        for title, sections in book_stories:
            key = f"{slug(book_title)}/{slug(title)}"
            full_text = "\n\n".join(text for _, text in sections)
            digest = hashlib.sha1(full_text.encode("utf-8")).hexdigest()

            entry = cache.get(key)
            if entry and entry.get("text_sha1") == digest and "summary" in entry:
                print(f"[cache] {title} (skip LLM)")
                continue

            facts, summary, complete = archivist.extract_story(title, sections)
            cache.put(
                key,
                {
                    "book": book_title,
                    "title": title,
                    "text_sha1": digest,
                    "chunks": archivist.count_chunks(sections),
                    "facts": facts,
                    "summary": summary,
                },
                complete=complete,
            )

    state["cache"] = cache.data
    return state


def entity_profiler_agent_node(state: VaultState) -> VaultState:
    """Entity Profiler Agent builds character/location profiles and saves entities.json."""
    print("--- [Agent: Entity Profiler] Canonicalizing entities & descriptions ---")
    stories = list(state["cache"].values())
    stories_by_title = {s["title"]: s for s in stories}

    char_apps: dict[str, list[str]] = {}
    place_apps: dict[str, list[str]] = {}

    for story in stories:
        story["who_links"] = names.people(story["facts"]["who"])
        story["where_links"] = names.places(story["facts"]["where"])
        for name in story["who_links"]:
            char_apps.setdefault(name, []).append(story["title"])
        for name in story["where_links"]:
            place_apps.setdefault(name, []).append(story["title"])

    entity_cache = JsonCache(ENTITY_CACHE_FILE)
    profiles: dict[str, dict] = {"character": {}, "place": {}}
    for kind, apps in (("character", char_apps), ("place", place_apps)):
        for name, titles in apps.items():
            ckey = f"{kind}/{slug(name)}"
            cached_item = entity_cache.get(ckey)
            if cached_item and cached_item.get("appearances") == titles:
                profiles[kind][name] = cached_item["profile"]
                continue
            profile, complete = archivist.describe_entity(
                kind, name, titles, stories_by_title
            )
            profiles[kind][name] = profile
            entity_cache.put(
                ckey,
                {
                    "kind": kind,
                    "name": name,
                    "appearances": titles,
                    "profile": profile,
                },
                complete=complete,
            )

    state["entities"] = {
        "char_apps": char_apps,
        "place_apps": place_apps,
        "profiles": profiles,
    }
    return state


def vault_architect_node(state: VaultState) -> VaultState:
    """Vault Architect Agent writes Markdown files into the vault."""
    print("--- [Agent: Vault Architect] Writing Obsidian Vault ---")
    writer = VaultWriter(VAULT, CREATED)
    writer.build(list(state["cache"].values()), state["entities"], names)
    print(f"[vault] Complete! Built Obsidian Vault in {VAULT}/")
    state["vault_status"] = "COMPLETE"
    return state


# =====================================================================
# Workflow Graph Construction
# =====================================================================


def build_vault_workflow() -> StateGraph:
    workflow = StateGraph(VaultState)

    workflow.add_node("ingestion_agent", ingestion_agent_node)
    workflow.add_node("extraction_agent", extraction_agent_node)
    workflow.add_node("entity_profiler_agent", entity_profiler_agent_node)
    workflow.add_node("vault_architect", vault_architect_node)

    workflow.set_entry_point("ingestion_agent")
    workflow.add_edge("ingestion_agent", "extraction_agent")
    workflow.add_edge("extraction_agent", "entity_profiler_agent")
    workflow.add_edge("entity_profiler_agent", "vault_architect")
    workflow.add_edge("vault_architect", END)

    return workflow.compile()


if __name__ == "__main__":
    app = build_vault_workflow()
    png_bytes = app.get_graph(xray=1).draw_mermaid_png()
    with open("sherlock_holmes_import.png", "wb") as file:
        file.write(png_bytes)
    initial_state: VaultState = {
        "books_data": {},
        "cache": {},
        "entities": {},
        "vault_status": "STARTING",
    }
    app.invoke(initial_state)
