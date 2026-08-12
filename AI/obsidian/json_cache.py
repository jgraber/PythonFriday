"""A write-through JSON cache for expensive LLM results.

Both pipeline stages cache to JSON so a re-run skips the model for work already
done. The invariant worth stating once is in `put`: an incomplete result is
never stored, so the next run retries it instead of inheriting a half-parsed
answer. Deleting the file forces a full, expensive rebuild.

Every accepted entry is flushed immediately rather than at the end, so a run
that dies partway -- a dropped connection, a killed process -- keeps everything
it had already earned.
"""

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any


class JsonCache:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.data: dict[str, Any] = {}
        if path.exists():
            self.data = json.loads(path.read_text(encoding="utf-8"))

    def get(self, key: str) -> Any | None:
        return self.data.get(key)

    def put(self, key: str, value: Any, *, complete: bool = True) -> None:
        """Store an entry and flush, unless it is incomplete.

        Incomplete results are dropped on purpose: caching a bad parse would
        make it permanent, since later runs would treat it as a hit.
        """
        if not complete:
            return
        self.data[key] = value
        self.flush()

    def flush(self) -> None:
        self.path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")

    def values(self) -> Iterator[Any]:
        return iter(self.data.values())

    def __contains__(self, key: str) -> bool:
        return key in self.data

    def __len__(self) -> int:
        return len(self.data)
