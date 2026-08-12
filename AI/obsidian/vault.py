"""Naming canon entities and writing them out as an Obsidian vault.

`NameCanonicalizer` decides what a character or place is *called*, which matters
more than it sounds: the name it returns becomes both a filename and a
`[[wikilink]]` target, so two spellings of one character silently produce two
half-empty hub notes instead of one good one.

`VaultWriter` renders the vault. It is deliberately ignorant of which author it
is writing about -- every per-author difference lives in the note contents it is
handed.
"""

import re
import shutil
from pathlib import Path

import frontmatter

from gutenberg_epub import normalize_text, safe_filename

MAX_NAME_WORDS = 5
LOWERCASE_PARTICLES = ("of", "the", "and")


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def dedup(names: list) -> list[str]:
    """Drop blanks and repeats, preserving first-seen order."""
    seen: list[str] = []
    for name in names:
        if name and name not in seen:
            seen.append(name)
    return seen


class NameCanonicalizer:
    """Folds the many ways a model names someone into one canonical form.

    Honorifics are stripped *before* the alias table is consulted, so alias keys
    must be given in stripped, lowercased form: "marple" maps to "Miss Marple"
    and "watson" to "Dr. Watson", whereas keys of "miss marple" or "dr watson"
    could never be reached. The constructor rejects those rather than let them
    sit in the table doing nothing.

    Note which way the honorific travels. "Dr. Watson" arrives, is stripped to
    "Watson", and the alias puts the title back; stripping alone would file him
    under plain "Watson". So the table is what settles the canonical form, not
    just what catches nicknames -- which is also how "Inspector Lestrade",
    "lestrade" and "G. Lestrade" all land on one note.
    """

    def __init__(
        self,
        honorifics: set[str],
        person_aliases: dict[str, str],
        place_aliases: dict[str, str],
    ) -> None:
        self.honorifics = honorifics
        self.person_aliases = person_aliases
        self.place_aliases = place_aliases
        for label, table in (
            ("person", person_aliases),
            ("place", place_aliases),
        ):
            unreachable = [k for k in table if self._starts_with_honorific(k)]
            if unreachable:
                raise ValueError(
                    f"{label} alias keys start with an honorific that is stripped "
                    f"before lookup, so they can never match: {sorted(unreachable)}"
                )

    def _starts_with_honorific(self, key: str) -> bool:
        first, *rest = key.split()
        return bool(rest) and first.strip(".") in self.honorifics

    def _canonical(
        self, raw: str, aliases: dict[str, str], *, strip_the: bool
    ) -> str | None:
        name = normalize_text(re.sub(r"\([^)]*\)", "", raw)).strip().strip(".")
        words = name.split()
        if not words or len(words) > MAX_NAME_WORDS:
            return None
        while (
            len(words) > 1
            and words[0].lower().strip(".") in self.honorifics
            and words[1][:1].isupper()
        ):
            words = words[1:]
        if strip_the and len(words) > 1 and words[0].lower() == "the":
            words = words[1:]
        fixed = []
        for i, w in enumerate(words):
            if i and w.lower() in LOWERCASE_PARTICLES:
                fixed.append(w.lower())
            elif w.isalpha() and (w.islower() or w.isupper()):
                fixed.append(w.capitalize())
            else:
                fixed.append(w)
        name = safe_filename(" ".join(fixed))
        return aliases.get(name.lower(), name)

    def person(self, raw: str) -> str | None:
        return self._canonical(raw, self.person_aliases, strip_the=False)

    def place(self, raw: str) -> str | None:
        return self._canonical(raw, self.place_aliases, strip_the=True)

    def people(self, raws: list) -> list[str]:
        return dedup([self.person(r) for r in raws])

    def places(self, raws: list) -> list[str]:
        return dedup([self.place(r) for r in raws])


class VaultWriter:
    """Writes stories/, characters/ and places/ notes with frontmatter."""

    FOLDERS = ("stories", "characters", "places")

    def __init__(self, root: Path, created: str) -> None:
        self.root = root
        self.created = created

    def reset(self) -> None:
        """Delete and recreate the vault; it is rebuilt from cache every run."""
        if self.root.exists():
            shutil.rmtree(self.root)
        for folder in self.FOLDERS:
            (self.root / folder).mkdir(parents=True, exist_ok=True)

    def write_note(self, path: Path, title: str, tags: list[str], body: str) -> None:
        post = frontmatter.Post(
            content=body, title=title, tags=tags, created=self.created
        )
        path.write_text(frontmatter.dumps(post), encoding="utf-8")

    def write_story(self, story: dict, names: NameCanonicalizer) -> None:
        facts = story["facts"]
        lines = [f"From *{story['book']}*.", "", "## Who"]
        lines += [f"- [[{n}]]" for n in names.people(facts["who"])] or [
            "- (not extracted)"
        ]
        lines += [
            "",
            "## What",
            facts["what"],
            "",
            "## How",
            facts["how"],
            "",
            "## Where",
        ]
        lines += [f"- [[{n}]]" for n in names.places(facts["where"])] or [
            "- (not extracted)"
        ]
        lines += [
            "",
            "## When",
            facts["when"],
            "",
            "## Why",
            facts["why"],
            "",
            "## Summary",
        ]
        lines += [f"- **{label}**: {text}" for label, text in story["summary"]]
        body = normalize_text("\n".join(lines))

        path = self.root / "stories" / f"{safe_filename(story['title'])}.md"
        self.write_note(path, story["title"], ["story", slug(story["book"])], body)

    def write_entity(
        self, kind: str, folder: str, name: str, titles: list[str], profile: dict
    ) -> None:
        plural = "story" if len(titles) == 1 else "stories"
        body = "\n".join(
            [
                profile["description"],
                "",
                "## Significance",
                profile["importance"],
                "",
                f"## Appears in ({len(titles)} {plural})",
            ]
            + [f"- [[{title}]]" for title in titles]
        )
        path = self.root / folder / f"{safe_filename(name)}.md"
        self.write_note(path, name, [kind], body)

    def build(self, stories: list, entities: dict, names: NameCanonicalizer) -> None:
        self.reset()
        for story in stories:
            self.write_story(story, names)
        for kind, (apps_key, folder) in (
            ("character", ("char_apps", "characters")),
            ("place", ("place_apps", "places")),
        ):
            apps = entities[apps_key]
            profiles = entities["profiles"][kind]
            for name, titles in apps.items():
                self.write_entity(kind, folder, name, titles, profiles[name])
