"""Minimal demo of `vault`: the same story written twice, badly and well.

    uv run python demo_vault.py

`vault`'s docstring names the failure it exists to prevent -- "two spellings of
one character silently produce two half-empty hub notes instead of one good
one". So this builds the vault twice from identical facts, once with an empty
alias table and once with a populated one, and diffs the two.

Both builds go to temporary directories and leave nothing behind. The entity
tables are assembled here the way `entity_profiler_agent_node` assembles them in
the real pipeline, so the fragmentation propagates exactly as it would there.
"""

import tempfile
from pathlib import Path

from vault import NameCanonicalizer, VaultWriter

HONORIFICS = {"mr", "mrs", "miss", "dr", "doctor", "inspector"}
# Keys must already be stripped of honorifics -- see the closing note.
PERSON_ALIASES = {
    "holmes": "Sherlock Holmes",
    "sherlock": "Sherlock Holmes",
    "watson": "Dr. Watson",
}
PLACE_ALIASES = {"baker street": "221B Baker Street", "221b": "221B Baker Street"}

# One story, with `who` and `where` exactly as a model tends to write them:
# the same two people four ways, the same address twice.
STORY = {
    "book": "The Adventures of Sherlock Holmes",
    "title": "A Scandal in Bohemia",
    "facts": {
        "who": ["Mr. Sherlock Holmes", "holmes", "SHERLOCK", "Dr. Watson", "watson"],
        "what": "A photograph is used to blackmail a king.",
        "how": "Holmes fakes a fire to make her reveal the hiding place.",
        "where": ["the Baker Street", "221b", "Briony Lodge"],
        "when": "1888",
        "why": "Irene Adler keeps the photograph as protection.",
    },
    "summary": [["Part 1", "Holmes is engaged by the King."]],
}


def entities_for(names: NameCanonicalizer) -> dict:
    """Build the entity tables the way the pipeline's profiler node does."""
    char_apps: dict[str, list[str]] = {}
    place_apps: dict[str, list[str]] = {}
    for name in names.people(STORY["facts"]["who"]):
        char_apps.setdefault(name, []).append(STORY["title"])
    for name in names.places(STORY["facts"]["where"]):
        place_apps.setdefault(name, []).append(STORY["title"])
    profile = {"description": "A profile.", "importance": "Why it matters."}
    return {
        "char_apps": char_apps,
        "place_apps": place_apps,
        "profiles": {
            "character": dict.fromkeys(char_apps, profile),
            "place": dict.fromkeys(place_apps, profile),
        },
    }


def build(label: str, names: NameCanonicalizer, root: Path) -> int:
    """Write the vault and report how many entity notes it ended up with."""
    entities = entities_for(names)
    VaultWriter(root, created="2026-08-09").build([STORY], entities, names)

    print(f"\n{label}")
    print(f"  who   -> {names.people(STORY['facts']['who'])}")
    print(f"  where -> {names.places(STORY['facts']['where'])}")
    total = 0
    for folder in ("characters", "places"):
        notes = sorted(p.name for p in (root / folder).glob("*.md"))
        total += len(notes)
        print(f"  {folder:11}: {len(notes)} notes  {notes}")
    return total


with tempfile.TemporaryDirectory() as tmp:
    # No aliases: every spelling survives as its own entity.
    bare = NameCanonicalizer(HONORIFICS, {}, {})
    fragmented = build("without an alias table", bare, Path(tmp) / "bare")

    # With aliases: the spellings collapse onto one canonical name each.
    aliased = NameCanonicalizer(HONORIFICS, PERSON_ALIASES, PLACE_ALIASES)
    canonical = build("with an alias table", aliased, Path(tmp) / "good")

    note = Path(tmp) / "good" / "stories" / "A Scandal in Bohemia.md"
    print(f"\n--- {note.name}, as written by the second build ---")
    print(note.read_text(encoding="utf-8"))

print(f"""
Same facts, same writer, different vaults: {fragmented} entity notes against
{canonical}. The extra {fragmented - canonical} are half-empty duplicates of notes that already
exist, and nothing warns you -- which is why the alias tables earn their keep.""")

# The alias table has one sharp edge: honorifics are stripped before the lookup,
# so a key that starts with one could never be reached. The constructor refuses
# it rather than letting it sit there silently doing nothing.
try:
    NameCanonicalizer(HONORIFICS, {"miss marple": "Miss Marple"}, {})
except ValueError as exc:
    print(f"\nrejected at construction: {str(exc)[:88]}...")
