import base64
import datetime
import hashlib
import json
import posixpath
import re
import shutil
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
import zlib
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional, TypedDict

import frontmatter
import openai
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field

sys.stdout.reconfigure(encoding="utf-8")

# =====================================================================
# Settings & Configuration
# =====================================================================

BOOKS_DIR = Path("holmes_books")
VAULT = Path("Sherlock_Holmes_Canon")
CACHE_FILE = Path("holmes_extractions.json")
ENTITY_CACHE_FILE = Path("holmes_entities.json")
PNG_FILE = "holmes_epub_to_vault.png"
UA = {"User-Agent": "Mozilla/5.0"}
CREATED = datetime.date.today().isoformat()

CHUNK_CHARS = 12_000
MERGE_INPUT_CHARS = 20_000
MIN_STORY_WORDS = 1000
HUB_MIN_STORIES = 2
MAP_UBIQUITY_CUTOFF = 0.5
MAP_MAX_HUBS = 15
MAX_ATTEMPTS = 3

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

SKIP_LABELS = re.compile(r"contents|title page|copyright|project gutenberg|illustration|preface", re.I)
CHAPTER_RE = re.compile(r"^chapter\s+[ivxlc\d]+\b", re.I)
NOVEL_PART_RE = re.compile(r"^(chapter|part|prologue|epilogue|introduction)\b", re.I)
SUB_ENTRY_RE = re.compile(r"^([ivxlc]+\.?|part\s+[ivxlc\d]+\.?|chapter\s+[ivxlc\d]+.*|\d+\..*)$", re.I)
ROMAN_PREFIX_RE = re.compile(r"^[IVXLC]+\.?\s+")
SUMMARY_RE = re.compile(r"^SUMMARY\s*:\s*(.+)$", re.I)
PROFILE_RE = re.compile(r"^(DESCRIPTION|IMPORTANCE)\s*:\s*(.+)$", re.I)
PROFILE_KEYS = ("description", "importance")
MIN_SECTION_WORDS = 20
ENTITY_CONTEXT_MAX_STORIES = 12
FACT_RE = re.compile(r"^(WHO|WHAT|HOW|WHERE|WHEN|WHY)\s*:\s*(.+)$", re.I)
FACT_KEYS = ("who", "what", "how", "where", "when", "why")

HONORIFICS = {"mr", "mrs", "ms", "miss", "dr", "doctor", "sir", "lord", "lady", "inspector", "colonel", "major", "professor"}
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

llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="openai/gpt-oss-20b",
    temperature=0.1,
)

# Prompts
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
    books_data: Dict[str, List]
    cache: Dict[str, dict]
    entities: Dict[str, dict]
    vault_status: str

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

def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def safe_filename(title: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', "", title)

def prettify_caps(text: str) -> str:
    if not text.isupper():
        return text
    words = [
        w.upper() if re.fullmatch(r"[ivxlc]+\.?", w) else w.capitalize()
        for w in text.lower().split()
    ]
    return " ".join(words)

BLOCK_TAGS = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "div", "li", "blockquote", "tr"}

class _TextExtractor(HTMLParser):
    def __init__(self, track_ids: set[str] | None = None) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.positions: dict[str, int] = {}
        self._track = track_ids or set()
        self._length = 0
        self._skip_depth = 0

    def _append(self, text: str) -> None:
        self.parts.append(text)
        self._length += len(text)

    def handle_starttag(self, tag: str, attrs: list) -> None:
        for key, value in attrs:
            if key in ("id", "name") and value in self._track and value not in self.positions:
                self.positions[value] = self._length
        if tag in ("style", "script", "head"):
            self._skip_depth += 1
        elif tag == "br":
            self._append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("style", "script", "head") and self._skip_depth:
            self._skip_depth -= 1
        elif tag in BLOCK_TAGS:
            self._append("\n\n")

    def handle_data(self, data: str) -> None:
        if not self._skip_depth:
            self._append(data)

def extract_text(xhtml: str, track_ids: set[str] | None = None) -> tuple[str, dict[str, int]]:
    extractor = _TextExtractor(track_ids)
    extractor.feed(xhtml)
    return "".join(extractor.parts), extractor.positions

def clean_text(raw: str) -> str:
    text = normalize_text(raw)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" ?\n ?", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def read_epub(path: Path) -> tuple[str, list[tuple[str, str]]]:
    with zipfile.ZipFile(path) as zf:
        container = ET.fromstring(zf.read("META-INF/container.xml"))
        opf_path = container.find(
            ".//{urn:oasis:names:tc:opendocument:xmlns:container}rootfile"
        ).attrib["full-path"]
        opf_dir = posixpath.dirname(opf_path)
        opf = ET.fromstring(zf.read(opf_path))

        ns = {"opf": "http://www.idpf.org/2007/opf", "dc": "http://purl.org/dc/elements/1.1/"}
        book_title = normalize_text(opf.findtext(".//dc:title", namespaces=ns).strip())

        manifest: dict[str, str] = {}
        nav_path = None
        for item in opf.iterfind(".//opf:manifest/opf:item", ns):
            href = posixpath.normpath(posixpath.join(opf_dir, item.attrib["href"]))
            manifest[item.attrib["id"]] = href
            if "nav" in item.attrib.get("properties", "").split():
                nav_path = href
        if nav_path is None:
            raise ValueError(f"{path.name}: no nav document (epub3 required)")

        spine = [manifest[ref.attrib["idref"]] for ref in opf.iterfind(".//opf:spine/opf:itemref", ns)]

        nav = ET.fromstring(zf.read(nav_path))
        nav_dir = posixpath.dirname(nav_path)
        xhtml_ns = "{http://www.w3.org/1999/xhtml}"
        toc_nav = None
        for el in nav.iter(xhtml_ns + "nav"):
            if el.attrib.get("{http://www.idpf.org/2007/ops}type") == "toc":
                toc_nav = el
                break
        if toc_nav is None:
            raise ValueError(f"{path.name}: no toc nav (epub3 required)")

        toc: list[tuple[str, str, str]] = []
        for a in toc_nav.iter(xhtml_ns + "a"):
            base, _, frag = a.attrib.get("href", "").partition("#")
            target = posixpath.normpath(posixpath.join(nav_dir, base))
            label = normalize_text(" ".join("".join(a.itertext()).split()))
            if label:
                toc.append((target, frag, label))

        booklow = book_title.lower().strip(" .")
        kept = [
            (target, frag, label)
            for target, frag, label in toc
            if not SKIP_LABELS.search(label) and label.lower().strip(" .") != booklow
        ]

        is_novel = sum(1 for _, _, label in kept if CHAPTER_RE.match(label)) >= 3
        if is_novel:
            kept = [e for e in kept if NOVEL_PART_RE.match(e[2])]

        by_file: dict[str, list[tuple[str, str]]] = {}
        for target, frag, label in kept:
            by_file.setdefault(target, []).append((frag, label))

        stories: list[list] = []
        pending = ""
        for fname in [f for f in spine if f in by_file]:
            entries = by_file[fname]
            raw, positions = extract_text(
                zf.read(fname).decode("utf-8"), {frag for frag, _ in entries if frag}
            )
            starts = [positions.get(frag, 0) for frag, _ in entries]
            ends = starts[1:] + [len(raw)]
            for (frag, label), start, end in zip(entries, starts, ends):
                seg = clean_text(raw[start:end])
                if is_novel:
                    if len(seg.split()) < MIN_SECTION_WORDS:
                        pending = f"{pending}\n\n{seg}".strip()
                        continue
                    if pending:
                        seg = f"{pending}\n\n{seg}"
                        pending = ""
                    if not stories:
                        stories.append([safe_filename(book_title), []])
                    stories[0][1].append([prettify_caps(label), seg])
                elif SUB_ENTRY_RE.match(label) and stories:
                    stories[-1][1][-1][1] += "\n\n" + seg
                else:
                    title = prettify_caps(ROMAN_PREFIX_RE.sub("", label))
                    stories.append([safe_filename(title), [[None, seg]]])

        result = []
        for title, sections in stories:
            words = sum(len(text.split()) for _, text in sections)
            if words < MIN_STORY_WORDS:
                print(f"[skip] {title} ({words} words, under {MIN_STORY_WORDS})")
                continue
            result.append((title, sections))
        return book_title, result

def invoke_llm(system: str, user: str) -> str:
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            reply = llm.invoke([("system", system), ("user", user)])
            return reply.content if isinstance(reply.content, str) else str(reply.content)
        except openai.APIError as e:
            print(f"[attempt {attempt}/{MAX_ATTEMPTS}] LLM call failed ({type(e).__name__}); retrying")
            if attempt == MAX_ATTEMPTS:
                raise
            time.sleep(2)

def split_chunks(text: str) -> list[str]:
    chunks: list[str] = []
    current: list[str] = []
    size = 0
    for para in text.split("\n\n"):
        if len(para) > CHUNK_CHARS:
            if current:
                chunks.append("\n\n".join(current))
                current, size = [], 0
            chunks.extend(para[i : i + CHUNK_CHARS] for i in range(0, len(para), CHUNK_CHARS))
            continue
        if size and size + len(para) > CHUNK_CHARS:
            chunks.append("\n\n".join(current))
            current, size = [], 0
        current.append(para)
        size += len(para) + 2
    if current:
        chunks.append("\n\n".join(current))
    return chunks

def parse_chunk_reply(text: str) -> tuple[str, str]:
    summary_parts: list[str] = []
    notes: list[str] = []
    for raw in normalize_text(text).splitlines():
        line = raw.strip().lstrip("-*").lstrip("0123456789.) ").strip().replace("**", "")
        m = SUMMARY_RE.match(line)
        if m:
            summary_parts.append(m.group(1).strip())
        elif line:
            notes.append(line)
    return " ".join(summary_parts), "\n".join(notes)

def chunk_call(where: str, chunk: str) -> tuple[str, str]:
    reply = invoke_llm(CHUNK_PROMPT.format(where=where), f"Story part:\n{chunk}\n\nYour fact notes:")
    return parse_chunk_reply(reply)

def parse_facts(text: str) -> dict:
    facts: dict[str, object] = {}
    for raw in normalize_text(text).splitlines():
        line = raw.strip().lstrip("-*").lstrip("0123456789.) ").strip().replace("**", "")
        m = FACT_RE.match(line)
        if not m:
            continue
        key, value = m.group(1).lower(), m.group(2).strip()
        if key in ("who", "where"):
            facts[key] = [p.strip(" .") for p in value.split(",") if p.strip(" .")]
        else:
            facts[key] = value
    return facts

def extract_story(title: str, sections: list) -> tuple[dict, list[list[str]], bool]:
    plan = []
    for sec_title, sec_text in sections:
        chunks = split_chunks(sec_text)
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
            where = f'part {j} of {n} of the chapter "{sec_title}" of the Sherlock Holmes novel "{title}"'
        else:
            where = f'part {g} of {len(plan)} of the Sherlock Holmes story "{title}"'
        summary, chunk_facts = chunk_call(where, chunk)
        notes.append(chunk_facts)
        if not summary:
            summary = "(not extracted)"
            missing_summary = True
        label = sec_title or f"Part {g}"
        if summaries and summaries[-1][0] == label:
            summaries[-1][1] += " " + summary
        else:
            summaries.append([label, summary])

    joined = "\n".join(notes)
    while len(joined) > MERGE_INPUT_CHARS:
        print(f"[condense] {title}: notes at {len(joined):,} chars")
        slices = split_chunks(joined)
        joined = "\n".join(
            chunk_call(f'part {i} of {len(slices)} of the Sherlock Holmes story "{title}"', s)[1]
            for i, s in enumerate(slices, 1)
        )

    print(f"[merge] {title}")
    merge_user = f"Fact notes in story order:\n{joined}\n\nThe 6-line case file:"
    facts = parse_facts(invoke_llm(MERGE_PROMPT.format(title=title), merge_user))
    if any(k not in facts for k in FACT_KEYS):
        facts = parse_facts(invoke_llm(MERGE_PROMPT.format(title=title), merge_user))

    facts_complete = all(k in facts for k in FACT_KEYS)
    if not facts_complete:
        facts.setdefault("who", [])
        facts.setdefault("where", [])
        for key in ("what", "how", "when", "why"):
            facts.setdefault(key, "(not extracted)")
    elif missing_summary:
        print(f"[warn] {title}: a part summary came back empty")
    return facts, summaries, facts_complete and not missing_summary

def canonical_name(raw: str, aliases: dict[str, str], strip_the: bool = False) -> str | None:
    name = normalize_text(re.sub(r"\([^)]*\)", "", raw)).strip().strip(".")
    words = name.split()
    if not words or len(words) > 5:
        return None
    while len(words) > 1 and words[0].lower().strip(".") in HONORIFICS and words[1][:1].isupper():
        words = words[1:]
    if strip_the and len(words) > 1 and words[0].lower() == "the":
        words = words[1:]
    fixed = []
    for i, w in enumerate(words):
        if i and w.lower() in ("of", "the", "and"):
            fixed.append(w.lower())
        elif w.isalpha() and (w.islower() or w.isupper()):
            fixed.append(w.capitalize())
        else:
            fixed.append(w)
    name = safe_filename(" ".join(fixed))
    return aliases.get(name.lower(), name)

def dedup(names: list) -> list[str]:
    seen: list[str] = []
    for name in names:
        if name and name not in seen:
            seen.append(name)
    return seen

def parse_profile(text: str) -> dict:
    profile: dict[str, str] = {}
    for raw in normalize_text(text).splitlines():
        line = raw.strip().lstrip("-*").lstrip("0123456789.) ").strip().replace("**", "")
        m = PROFILE_RE.match(line)
        if m:
            profile[m.group(1).lower()] = m.group(2).strip()
    return profile

def describe_entity(kind: str, name: str, titles: list[str], stories_by_title: dict) -> tuple[dict, bool]:
    noun = "character" if kind == "character" else "location"
    lines = [
        f"- {title}: {stories_by_title[title]['facts']['what']}"
        for title in titles[:ENTITY_CONTEXT_MAX_STORIES]
    ]
    if len(titles) > ENTITY_CONTEXT_MAX_STORIES:
        lines.append(f"(and {len(titles) - ENTITY_CONTEXT_MAX_STORIES} more stories)")
    system = ENTITY_PROMPT.format(kind=noun, name=name)
    user = "Case notes:\n" + "\n".join(lines) + "\n\nThe 2-line profile:"
    profile = parse_profile(invoke_llm(system, user))
    if any(k not in profile for k in PROFILE_KEYS):
        profile = parse_profile(invoke_llm(system, user))
    complete = all(k in profile for k in PROFILE_KEYS)
    if not complete:
        for key in PROFILE_KEYS:
            profile.setdefault(key, "(not extracted)")
    return profile, complete

# =====================================================================
# Deep Agent Nodes
# =====================================================================

def ingestion_agent_node(state: VaultState) -> VaultState:
    """Ingestion Agent downloads canon books and parses EPUB structure."""
    print("--- [Agent: Ingestion] Fetching & Reading EPUB files ---")
    BOOKS_DIR.mkdir(exist_ok=True)
    for filename, url in BOOKS.items():
        target = BOOKS_DIR / filename
        if not target.exists() or target.stat().st_size == 0:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as resp:
                target.write_bytes(resp.read())
            time.sleep(1)

    epubs = sorted(BOOKS_DIR.glob("*.epub"))
    parsed_books = {}
    for epub in epubs:
        book_title, book_stories = read_epub(epub)
        parsed_books[book_title] = book_stories
        print(f"[book] {book_title}: {len(book_stories)} stories found")

    state["books_data"] = parsed_books
    return state

def extraction_agent_node(state: VaultState) -> VaultState:
    """Extraction Agent extracts 5W1H facts and generates extractions.json cache."""
    print("--- [Agent: Extractor] Synthesizing 5W1H Case Files ---")
    cache = {}
    if CACHE_FILE.exists():
        cache = json.loads(CACHE_FILE.read_text(encoding="utf-8"))

    stories_processed = {}
    for book_title, book_stories in state["books_data"].items():
        for title, sections in book_stories:
            key = f"{slug(book_title)}/{slug(title)}"
            full_text = "\n\n".join(text for _, text in sections)
            digest = hashlib.sha1(full_text.encode("utf-8")).hexdigest()

            entry = cache.get(key)
            if entry and entry.get("text_sha1") == digest and "summary" in entry:
                print(f"[cache] {title} (skip LLM)")
                facts, summary = entry["facts"], entry["summary"]
            else:
                facts, summary, complete = extract_story(title, sections)
                if complete:
                    cache[key] = {
                        "book": book_title,
                        "title": title,
                        "text_sha1": digest,
                        "chunks": sum(len(split_chunks(text)) for _, text in sections),
                        "facts": facts,
                        "summary": summary,
                    }
                    CACHE_FILE.write_text(json.dumps(cache, indent=2), encoding="utf-8")
            stories_processed[title] = {"book": book_title, "title": title, "facts": facts, "summary": summary}

    state["cache"] = cache
    return state

def entity_profiler_agent_node(state: VaultState) -> VaultState:
    """Entity Profiler Agent builds character/location profiles and saves entities.json."""
    print("--- [Agent: Entity Profiler] Canonicalizing entities & descriptions ---")
    cache = state["cache"]
    stories = list(cache.values())
    stories_by_title = {s["title"]: s for s in stories}

    char_apps: dict[str, list[str]] = {}
    place_apps: dict[str, list[str]] = {}

    for story in stories:
        story["who_links"] = dedup([canonical_name(w, PERSON_ALIASES) for w in story["facts"]["who"]])
        story["where_links"] = dedup([canonical_name(w, PLACE_ALIASES, strip_the=True) for w in story["facts"]["where"]])
        for name in story["who_links"]:
            char_apps.setdefault(name, []).append(story["title"])
        for name in story["where_links"]:
            place_apps.setdefault(name, []).append(story["title"])

    entity_cache = {}
    if ENTITY_CACHE_FILE.exists():
        entity_cache = json.loads(ENTITY_CACHE_FILE.read_text(encoding="utf-8"))

    profiles = {"character": {}, "place": {}}
    for kind, apps in (("character", char_apps), ("place", place_apps)):
        for name, titles in apps.items():
            ckey = f"{kind}/{slug(name)}"
            cached_item = entity_cache.get(ckey)
            if cached_item and cached_item.get("appearances") == titles:
                profiles[kind][name] = cached_item["profile"]
            else:
                profile, complete = describe_entity(kind, name, titles, stories_by_title)
                profiles[kind][name] = profile
                if complete:
                    entity_cache[ckey] = {"kind": kind, "name": name, "appearances": titles, "profile": profile}
                    ENTITY_CACHE_FILE.write_text(json.dumps(entity_cache, indent=2), encoding="utf-8")

    state["entities"] = {"char_apps": char_apps, "place_apps": place_apps, "profiles": profiles}
    return state

def vault_architect_node(state: VaultState) -> VaultState:
    """Vault Architect Agent writes Markdown files into holmes_vault/ using python-frontmatter."""
    print("--- [Agent: Vault Architect] Writing Obsidian Vault ---")
    if VAULT.exists():
        shutil.rmtree(VAULT)
    (VAULT / "stories").mkdir(parents=True, exist_ok=True)
    (VAULT / "characters").mkdir(parents=True, exist_ok=True)
    (VAULT / "places").mkdir(parents=True, exist_ok=True)

    cache = state["cache"]
    entities = state["entities"]

    def write_markdown_file(path: Path, title: str, tags: list[str], body: str) -> None:
        post = frontmatter.Post(
            content=body,
            title=title,
            tags=tags,
            created=CREATED
        )
        path.write_text(frontmatter.dumps(post), encoding="utf-8")

    # Write stories
    for story in cache.values():
        facts = story["facts"]
        lines = [f"From *{story['book']}*.", "", "## Who"]
        who_links = dedup([canonical_name(w, PERSON_ALIASES) for w in facts["who"]])
        lines += [f"- [[{n}]]" for n in who_links] or ["- (not extracted)"]
        lines += ["", "## What", facts["what"], "", "## How", facts["how"], "", "## Where"]
        where_links = dedup([canonical_name(w, PLACE_ALIASES, strip_the=True) for w in facts["where"]])
        lines += [f"- [[{n}]]" for n in where_links] or ["- (not extracted)"]
        lines += ["", "## When", facts["when"], "", "## Why", facts["why"], "", "## Summary"]
        lines += [f"- **{label}**: {text}" for label, text in story["summary"]]
        body = normalize_text("\n".join(lines))
        
        file_path = VAULT / "stories" / f"{safe_filename(story['title'])}.md"
        write_markdown_file(file_path, story["title"], ["story", slug(story["book"])], body)

    # Write entity hubs
    entity_keys = {
        "character": ("char_apps", VAULT / "characters"),
        "place": ("place_apps", VAULT / "places")
    }

    for kind, (apps_key, folder) in entity_keys.items():
        apps = entities[apps_key]
        profiles = entities["profiles"][kind]
        for name, titles in apps.items():
            profile = profiles[name]
            plural = "story" if len(titles) == 1 else "stories"
            body = "\n".join([
                profile["description"], "", "## Significance", profile["importance"], "",
                f"## Appears in ({len(titles)} {plural})"
            ] + [f"- [[{title}]]" for title in titles])
            
            file_path = folder / f"{safe_filename(name)}.md"
            write_markdown_file(file_path, name, [kind], body)

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