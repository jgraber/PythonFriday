"""Reading Project Gutenberg EPUB3 files into labelled blocks of text.

This module owns the mechanics that every book shares: opening the archive,
walking the nav document's table of contents, and splitting each spine file into
sections at its anchor ids. ebooklib does the container/OPF/manifest/spine work
and hands over a parsed table of contents; BeautifulSoup flattens the XHTML.

What it deliberately does not own is how those sections are *grouped* into
stories, because that differs per author. Doyle's Gutenberg editions follow one
convention and can be inferred; Christie's span six and are declared per book.
Callers pass a `keep` predicate to select table-of-contents entries, then group
the resulting `Section` stream themselves.

    with EpubBook(path) as book:
        for section in book.sections(keep=lambda e: e.depth == 1):
            ...

Choosing *what counts as a story* is the caller's, but the chores that follow from
that choice are not, so the module provides them rather than leaving each caller
to rediscover them: `is_front_matter` for the boilerplate toc labels every
Gutenberg edition carries, `merge_leads` to fold pre-anchor text into the section
it continues, and `strip_heading` to drop the heading a section opens by
repeating. `demo_gutenberg_epub.py` is the short worked example.

`spike/` holds the frozen pre-ebooklib implementation plus harnesses that assert
this module still yields identical sections and identical story grouping on all
23 books. Run them after changing anything here.
"""

import re
from collections.abc import Callable, Iterable, Iterator
from pathlib import Path
from types import TracebackType
from typing import NamedTuple, Self

from bs4 import BeautifulSoup, NavigableString, Tag
from ebooklib import epub

# Spine files are XHTML, so parse them as XML. "lxml" and "html.parser" yield
# byte-identical sections on the whole corpus but make bs4 raise
# XMLParsedAsHTMLWarning; bs4 strips the default XHTML namespace either way, so
# the plain `soup("p")` lookups below work under all three.
PARSER = "lxml-xml"

# Tags the flattener ends with a blank line, i.e. treats as block-level.
BLOCK_TAGS = ["p", "h1", "h2", "h3", "h4", "h5", "h6", "div", "li", "blockquote", "tr"]
SKIP_TAGS = ["style", "script", "head"]

# Boilerplate toc labels every Gutenberg edition carries. Author-specific extras
# (a pen name, a cast list, a transcriber's note) stay with the caller -- see
# `EXTRA_SKIP_LABELS` in `agatha_christie_import.py`, which is tested alongside
# this; the Holmes script needs nothing beyond these.
FRONT_MATTER = re.compile(
    r"contents|title page|copyright|project gutenberg|illustration|preface",
    re.IGNORECASE,
)


class TocEntry(NamedTuple):
    """One anchor in the nav document's table of contents."""

    target: str  # spine file the anchor points into, relative to the OPF
    frag: str  # anchor id within that file, "" if the link had none
    label: str  # link text, whitespace-collapsed
    depth: int  # 1 for a top-level entry, 2 for a nested one, ...
    children: tuple[str, ...]  # labels of this entry's own sub-entries


class Section(NamedTuple):
    """A run of text delimited by table-of-contents anchors."""

    label: str  # the entry's label, "" for lead text
    depth: int  # 0 for lead text
    children: tuple[str, ...]
    text: str
    is_lead: bool  # text found before this spine file's first anchor


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


def safe_filename(title: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', "", title)


def prettify_caps(text: str) -> str:
    """Turn an ALL-CAPS heading into title case, leaving roman numerals alone."""
    if not text.isupper():
        return text
    words = [
        w.upper() if re.fullmatch(r"[ivxlc]+\.?", w) else w.capitalize()
        for w in text.lower().split()
    ]
    return " ".join(words)


def clean_text(raw: str) -> str:
    text = normalize_text(raw)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" ?\n ?", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def is_front_matter(label: str) -> bool:
    """True for a toc label that is Gutenberg boilerplate rather than content."""
    return bool(FRONT_MATTER.search(label))


def strip_heading(label: str, text: str) -> str:
    """`text` minus the `label` heading it opens by repeating.

    A toc anchor sits *on* the heading element, so a section's text starts with
    its own label. The heading can span several blocks -- Doyle's editions put the
    numeral and the title in separate elements ("I." then "A SCANDAL IN BOHEMIA")
    -- so leading paragraphs are peeled while they are still building towards the
    label, and cut only once they add up to exactly it. Text that does not start
    with its heading is returned unchanged, so this can never eat real prose.

    Takes the two strings rather than a `Section` because callers apply it to
    accumulated text that no longer matches any single section's `.text`.
    """
    wanted = [w.casefold() for w in label.split()]
    paragraphs = text.split("\n\n")
    seen: list[str] = []
    for taken, paragraph in enumerate(paragraphs, start=1):
        seen += [w.casefold() for w in paragraph.split()]
        if len(seen) > len(wanted):
            break
        if seen == wanted:
            return "\n\n".join(paragraphs[taken:]).lstrip()
    return text


def merge_leads(sections: Iterable[Section]) -> Iterator[Section]:
    """Fold each `is_lead` section into the section it continues.

    `sections()` cannot do this itself: whether lead text continues the previous
    section depends on how the caller grouped things, and the module does not do
    the grouping. But "append it to whatever was still open" is what every caller
    wants, so here it is once.

    A lead with nothing before it -- the Gutenberg header at the top of a book --
    has no section to join and is yielded unchanged, still flagged `is_lead`,
    rather than silently dropped.
    """
    pending: Section | None = None
    for section in sections:
        if section.is_lead and pending is not None:
            pending = pending._replace(text=f"{pending.text}\n\n{section.text}".strip())
            continue
        if pending is not None:
            yield pending
        pending = section
    if pending is not None:
        yield pending


def _runs(xhtml: str, frags: set[str]) -> list[tuple[str, str]]:
    """Split one spine file into `(frag, text)` runs, in document order.

    The first run is keyed `""` and holds the text before the first tracked
    anchor. Every tracked anchor opens a new run, so a file arrives already
    split and no caller has to do offset arithmetic. Being order-driven rather
    than offset-driven also means a table of contents whose entries are not in
    document order still yields each entry its own text.
    """
    soup = BeautifulSoup(xhtml, PARSER)

    for junk in soup(SKIP_TAGS):
        junk.decompose()
    for br in soup("br"):
        br.replace_with("\n")
    for block in soup(BLOCK_TAGS):
        block.append("\n\n")  # end-of-block separator, as a real text node

    runs: list[tuple[str, list[str]]] = [("", [])]
    seen: set[str] = set()
    for node in soup.descendants:
        if isinstance(node, Tag):
            anchor = node.get("id") or node.get("name")
            if anchor in frags and anchor not in seen:
                seen.add(anchor)  # a repeated id is not a second boundary
                runs.append((anchor, []))
        elif type(node) is NavigableString:
            # `type(...) is` on purpose: Comment, Doctype and CData subclass
            # NavigableString and must not contribute text.
            runs[-1][1].append(str(node))

    return [(frag, "".join(parts)) for frag, parts in runs]


def _toc_entries(book: epub.EpubBook) -> list[TocEntry]:
    """Flatten ebooklib's nested table of contents into a depth-tagged stream.

    ebooklib yields `Link` objects and `(Section, [children])` tuples. Nesting
    carries meaning a flat scan loses: some books hang their chapters off a
    book-title node, and others hang a story's real title off a bare
    "Chapter N" node, so both `depth` and `children` are recorded.
    """
    entries: list[TocEntry] = []

    def label_of(node: object) -> str:
        head = node[0] if isinstance(node, tuple) else node
        return normalize_text(" ".join((getattr(head, "title", "") or "").split()))

    def walk(nodes: list, depth: int) -> None:
        for node in nodes:
            head, kids = node if isinstance(node, tuple) else (node, [])
            label = label_of(head)
            if label:
                base, _, frag = (head.href or "").partition("#")
                entries.append(
                    TocEntry(
                        base,  # OPF-relative, matching item.get_name()
                        frag,
                        label,
                        depth,
                        tuple(lbl for kid in kids if (lbl := label_of(kid))),
                    )
                )
            walk(list(kids), depth + 1)

    walk(book.toc, 1)
    return entries


class EpubBook:
    """An EPUB3 archive, read through ebooklib.

    Still a context manager, but `close()` is a no-op: ebooklib reads the whole
    archive up front and closes the zip itself.
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        self._book = epub.read_epub(str(path), options={"ignore_ncx": True})

        # ebooklib falls back to a legacy NCX when there is no nav document and
        # returns a plausible-looking toc; `ignore_ncx` only picks nav *when nav
        # exists*. Check explicitly, so a bad download fails loudly instead of
        # quietly mis-grouping stories.
        if not any(isinstance(i, epub.EpubNav) for i in self._book.get_items()):
            raise ValueError(f"{path.name}: no nav document (epub3 required)")

        self.title = normalize_text(
            self._book.get_metadata("DC", "title")[0][0].strip()
        )
        self._files = {item.get_name(): item for item in self._book.get_items()}
        self.spine = [
            item.get_name()
            for idref, _linear in self._book.spine
            if (item := self._book.get_item_with_id(idref)) is not None
        ]

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        pass

    def toc(self) -> list[TocEntry]:
        """Walk the nav document's toc, in reading order, keeping nesting depth."""
        return _toc_entries(self._book)

    def sections(
        self, keep: Callable[[TocEntry], bool] | None = None
    ) -> Iterator[Section]:
        """Yield the text between successive toc anchors, in spine order.

        `keep` selects which toc entries count as section boundaries; entries it
        rejects are not treated as breaks, so their text stays with the section
        that precedes them.

        Gutenberg splits long books across several files, sometimes immediately
        after a heading. Text before a file's first anchor is therefore yielded
        as its own `is_lead` section rather than dropped -- it belongs to
        whatever section was left open, and discarding it loses whole chapters.
        """
        kept = [e for e in self.toc() if keep is None or keep(e)]
        by_file: dict[str, list[TocEntry]] = {}
        for entry in kept:
            by_file.setdefault(entry.target, []).append(entry)

        for name in [f for f in self.spine if f in by_file]:
            entries = by_file[name]
            xhtml = self._files[name].get_content().decode("utf-8")
            texts = dict(_runs(xhtml, {e.frag for e in entries if e.frag}))

            # An entry with no fragment, or one whose anchor is missing from the
            # file, starts at the top and so claims the lead run.
            orphans = [e for e in entries if e.frag not in texts]
            lead = clean_text(texts[""])
            if lead and not orphans:
                yield Section("", 0, (), lead, is_lead=True)

            for entry in entries:
                raw = texts[""] if entry in orphans else texts[entry.frag]
                yield Section(
                    entry.label,
                    entry.depth,
                    entry.children,
                    clean_text(raw),
                    is_lead=False,
                )
