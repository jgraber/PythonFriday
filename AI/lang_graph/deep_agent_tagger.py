"""Auto-tag a Markdown note's frontmatter with a Deep Agents coordinator.

Reads a Markdown file's frontmatter + body, delegates to two Deep Agents
subagents (keyword_scout -> tag_normalizer) to propose and clean up keywords,
then overwrites the frontmatter `tags` field with the top 5 single-word tags.
If the first pass returns fewer than 5 usable single-word tags, it notes this
to the console and retries once with all fenced code blocks stripped.

Run:
    uv pip install deepagents langchain-openai python-frontmatter
    uv run deep_agent_tagger.py                  # tag the bundled sample_note.md
    uv run deep_agent_tagger.py path/to/note.md  # tag a real file in place
    uv run deep_agent_tagger.py reset            # delete sample_note.md

Important:
    The local model must support OpenAI-compatible tool calling because the
    coordinator delegates work through Deep Agents' built-in task tool.
    gpt-oss-20b behind LM Studio trips this intermittently (a "peg-native
    format" 400 or a recursion-limit loop), so each agent turn is retried.
"""

import re
import sys
import warnings
from pathlib import Path
from typing import Any

import frontmatter
import openai
from langchain_openai import ChatOpenAI
from langgraph.errors import GraphRecursionError

warnings.filterwarnings("ignore", message=".*allowed_objects.*")

from deepagents import create_deep_agent

sys.stdout.reconfigure(encoding="utf-8")

llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="openai/gpt-oss-20b",
    temperature=0.1,
)

SAMPLE_FILE = Path("sample_note.md")
TAG_COUNT = 5
MAX_ATTEMPTS = 3


SCOUT_SYSTEM = (
    "You extract the key topics of a document. Read the supplied Markdown "
    "content and list up to 10 concrete concepts, technologies, or themes it "
    "actually covers. Return one candidate per line, with no numbering and no "
    "preamble. Short phrases are fine at this stage."
)

NORMALIZER_SYSTEM = (
    "You turn candidate topics into clean tags. Convert each supplied "
    "candidate into a single lowercase tag: join multi-word concepts with a "
    "hyphen (machine-learning), never a space. Drop duplicates and "
    "near-duplicates. Return one tag per line, with no numbering and no "
    "preamble."
)

COORDINATOR_SYSTEM = f"""You assign tags to a Markdown document.

You MUST use the task tool exactly twice, in this order:

1. Call keyword_scout with the full document content, asking for candidate
   topics.
2. Call tag_normalizer with the scout's candidates, asking for clean single
   word tags.

Then choose the {TAG_COUNT} tags that best fit the document. Return EXACTLY
{TAG_COUNT} lines, one tag per line, with:
- no numbering, bullets, headings, markdown fences, or preamble
- each line a single token: lowercase, no spaces (hyphens are allowed)

Output nothing except the {TAG_COUNT} tag lines.
"""


subagents = [
    {
        "name": "keyword_scout",
        "description": (
            "Reads document content and lists up to ten candidate topics or "
            "themes it covers. Use for the first delegation."
        ),
        "system_prompt": SCOUT_SYSTEM,
        "model": llm,
    },
    {
        "name": "tag_normalizer",
        "description": (
            "Turns candidate topics into clean, deduplicated single-word tags. "
            "Use for the second delegation."
        ),
        "system_prompt": NORMALIZER_SYSTEM,
        "model": llm,
    },
]


tagger_agent = create_deep_agent(
    model=llm,
    system_prompt=COORDINATOR_SYSTEM,
    subagents=subagents,
)


def message_text(message: Any) -> str:
    """Extract plain text from a LangChain message."""
    content = getattr(message, "content", message)

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text", "")))
        return "\n".join(part for part in parts if part).strip()

    return str(content).strip()


CODE_BLOCK_RE = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)
TAG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def strip_code_blocks(text: str) -> str:
    """Remove fenced code blocks so the model tags the prose, not the code."""
    return CODE_BLOCK_RE.sub("", text)


def parse_tags(text: str) -> list[str]:
    """Keep only single-token lines (the 'tags as single words' contract)."""
    tags: list[str] = []
    for raw in text.splitlines():
        line = raw.strip().lstrip("-*#> ").lstrip("0123456789.) ").strip()
        line = line.strip("\"'`").lower()
        if TAG_RE.match(line) and line not in tags:
            tags.append(line)
    return tags[:TAG_COUNT]


# gpt-oss-20b behind LM Studio intermittently fails a deep-agent turn: the
# tool-calling grammar trips ("peg-native format" 400) or the coordinator loops
# until the recursion limit. Both are transient, so retry the whole invoke.
TRANSIENT_ERRORS = (openai.APIError, GraphRecursionError)


def generate_tags(content: str) -> list[str]:
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            result = tagger_agent.invoke(
                {
                    "messages": [
                        {"role": "user", "content": f"Tag this document:\n\n{content}"}
                    ]
                },
                {"recursion_limit": 40},
            )
            return parse_tags(message_text(result["messages"][-1]))
        except TRANSIENT_ERRORS as error:
            print(
                f"[attempt {attempt}/{MAX_ATTEMPTS}] local model failed "
                f"({type(error).__name__}); retrying."
            )
    print(f"[give up] local model kept failing after {MAX_ATTEMPTS} attempts.")
    return []


def tag_document(content: str) -> list[str]:
    tags = generate_tags(content)
    if len(tags) < TAG_COUNT:
        print(
            f"[retry] Got {len(tags)} single-word tag(s); "
            f"stripping code blocks and trying again."
        )
        retry = generate_tags(strip_code_blocks(content))
        if len(retry) >= len(tags):
            tags = retry
    return tags


def main() -> None:
    path = Path(sys.argv[1])

    png_bytes = tagger_agent.get_graph(xray=1).draw_mermaid_png()
    with open("deep_agent_tagger.png", "wb") as file:
        file.write(png_bytes)

    post = frontmatter.load(str(path))
    print(f"--- TAGGING --- {path}")
    print(
        f"content: {len(post.content)} chars, "
        f"existing tags: {post.get('tags', [])}"
    )

    tags = tag_document(post.content)

    if not tags:
        print("[error] No single-word tags produced after retry; "
              "leaving file unchanged.")
        return

    post["tags"] = tags
    frontmatter.dump(post, str(path))

    print("\n--- TAGS WRITTEN ---")
    for tag in tags:
        print(f"  {tag}")
    print(f"--- saved to {path} ---")


if __name__ == "__main__":
    main()
