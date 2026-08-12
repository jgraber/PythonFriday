"""Minimal demo of `json_cache` -- what it stores, and what it refuses to.

    uv run python demo_json_cache.py

Runs in a temporary directory, so it leaves nothing behind. The behaviour worth
watching is the `complete=False` put: it is a no-op on purpose, because caching a
bad parse would make it permanent -- every later run would treat it as a hit.
"""

import tempfile
from pathlib import Path

from json_cache import JsonCache

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "extractions.json"

    cache = JsonCache(path)
    print(f"new cache          : {len(cache)} entries, file on disk: {path.exists()}")

    # A good result is stored and flushed immediately, not at the end of the run.
    cache.put("holmes/veiled-lodger", {"title": "The Veiled Lodger", "chunks": 2})
    print(f"after a good put   : {len(cache)} entries, file on disk: {path.exists()}")

    # A half-parsed result is dropped, so the next run retries it instead of
    # inheriting the bad answer.
    cache.put("holmes/valley-of-fear", {"title": "half-parsed"}, complete=False)
    print(f"after incomplete   : {len(cache)} entries")
    print(f"  get()            : {cache.get('holmes/valley-of-fear')}")
    print(f"  in cache         : {'holmes/valley-of-fear' in cache}")

    # Write-through: a run killed at this point keeps everything it had earned.
    reopened = JsonCache(path)
    print(f"reopened from disk : {len(reopened)} entries -> {list(reopened.values())}")

    print(f"\n{path.name} contains:\n{path.read_text(encoding='utf-8')}")
