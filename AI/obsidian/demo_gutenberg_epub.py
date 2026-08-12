"""Minimal demo of `gutenberg_epub` on one Gutenberg EPUB3.

    uv run python demo_gutenberg_epub.py

Prints the book title, its table of contents, and each story with a preview.
Reads nothing but the EPUB; writes nothing; no LLM involved.

All this script decides is *which toc entries are stories* -- the one judgement
the module deliberately leaves to callers. Everything downstream of that choice
(`merge_leads`, `strip_heading`, `is_front_matter`) comes from the module.
"""

import sys
from pathlib import Path

from gutenberg_epub import (
    EpubBook,
    TocEntry,
    is_front_matter,
    merge_leads,
    prettify_caps,
    strip_heading,
)

sys.stdout.reconfigure(encoding="utf-8")  # labels carry curly quotes and a "™"

BOOK = Path("holmes_books/adventures_of_sherlock_holmes.epub")

with EpubBook(BOOK) as book:

    def is_story(entry: TocEntry) -> bool:
        """One story per top-level toc entry, minus the title page and boilerplate.

        Depth-2 entries here are the numbered scene divisions *inside* a story
        ("I.", "II.", "III."). Rejecting them means they are not treated as
        boundaries, so their text stays with the story that opened -- which is the
        point of `keep` being a predicate rather than a depth number.
        """
        return (
            entry.depth == 1
            and not is_front_matter(entry.label)
            and entry.label.casefold() != book.title.casefold()
        )

    print(f"{book.title} -- {len(book.spine)} spine files\n")

    print("table of contents:")
    for entry in book.toc():
        kids = f"   (children: {', '.join(entry.children)})" if entry.children else ""
        print(f"  {'    ' * (entry.depth - 1)}{entry.label}{kids}")

    stories = list(merge_leads(book.sections(keep=is_story)))

print(f"\n{len(stories)} stories:")
for section in stories:
    words = strip_heading(section.label, section.text).split()
    print(
        f"  {prettify_caps(section.label):48} {len(words):>6,} words "
        f"| {' '.join(words[:9])}..."
    )
