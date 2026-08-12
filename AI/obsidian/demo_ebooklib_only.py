"""The same ebook as `demo_gutenberg_epub.py`, printed the same way, ebooklib only.

    uv run python demo_ebooklib_only.py
    uv run python demo_gutenberg_epub.py    # for the side-by-side

Same three sections as the original -- title and spine, the table of contents,
then the unit list with word counts and a preview -- so the two outputs can be
read against each other line by line.

Nothing from `gutenberg_epub` is imported. Where that module would have done the
work this file does it by hand (the toc walker, the tag stripper) or not at all
(no punctuation normalising, no front-matter filter, no heading removal, no
splitting a file at its anchors). The differences land in the output rather than
in commentary.
"""

import re
import sys
from pathlib import Path

from ebooklib import epub

sys.stdout.reconfigure(encoding="utf-8")

BOOK = Path("holmes_books/adventures_of_sherlock_holmes.epub")


def walk(nodes: list, depth: int = 1):
    """Flatten ebooklib's nested toc. `gutenberg_epub._toc_entries` does this."""
    for node in nodes:
        head, kids = node if isinstance(node, tuple) else (node, [])
        children = [(k[0] if isinstance(k, tuple) else k).title or "" for k in kids]
        yield head, depth, children
        yield from walk(kids, depth + 1)


def naive_text(markup: str) -> str:
    """Strip tags. ebooklib returns bytes of XHTML and no text API at all."""
    return re.sub(r"<[^>]+>", "", markup)


raw = epub.read_epub(str(BOOK), options={"ignore_ncx": True})
spine = [raw.get_item_with_id(idref).get_name() for idref, _ in raw.spine]
entries = list(walk(raw.toc))

print(f"{raw.get_metadata('DC', 'title')[0][0]} -- {len(spine)} spine files\n")

print("table of contents:")
for head, depth, children in entries:
    kids = f"   (children: {', '.join(children)})" if children else ""
    print(f"  {'    ' * (depth - 1)}{head.title}{kids}")

# The original lists stories, split at toc anchors. ebooklib cannot cut a file at
# an anchor, so the closest available unit is the spine file -- front matter,
# cover wrapper and licence included, since nothing here judges toc labels.
label_of: dict[str, str] = {}
for head, _depth, _children in entries:
    label_of.setdefault((head.href or "").partition("#")[0], head.title or "")

units = [
    (
        label_of.get(name) or f"<no toc entry: {name}>",
        naive_text(raw.get_item_with_href(name).get_content().decode("utf-8")),
    )
    for name in spine
]

print(f"\n{len(units)} spine files:")
for label, text in units:
    words = text.split()
    print(f"  {label:48} {len(words):>6,} words | {' '.join(words[:9])}...")

# total = sum(len(text.split()) for _, text in units)
# joined = "\n".join(text for _, text in units)
# print(f"""
# {len(units)} units, {total:,} words. The original prints 12 stories: the extra three
# here are the cover wrapper, the front matter and the licence, because nothing in
# this script judges a toc label.

# Run both and read them together -- the rest shows up on its own:
#   - each story's word count runs a few higher, exactly the heading this preview
#     repeats and `strip_heading` removes
#   - punctuation is left as the file has it: {joined.count(chr(8217)):,} curly apostrophes,
#     {joined.count(chr(8212))} em-dashes, {joined.count("&amp;")} undecoded &amp;
#   - titles stay ALL-CAPS: no prettify_caps
#   - "I.", "II." and "III." are listed as toc children, but their text can be
#     neither separated from the story nor kept with it by choice: one file, one
#     blob, and the choice `keep=` exists to make is not on offer
#   - the first unit is the cover wrapper, which has no toc entry at all""")
