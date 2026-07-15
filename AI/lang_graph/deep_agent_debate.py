"""Optimist vs pessimist debate implemented with Deep Agents.

A Deep Agents coordinator delegates four ordered turns:
optimist -> pessimist -> optimist rebuttal -> pessimist rebuttal.
It then returns exactly two opportunities, two risks, and one verdict.

Run:
    uv pip install deepagents langchain-openai
    uv run deep_agent_debate.py
    uv run deep_agent_debate.py "<topic>"

Important:
    The local model must support OpenAI-compatible tool calling because the
    coordinator delegates work through Deep Agents' built-in task tool.
"""

import sys
import warnings
from typing import Any

from langchain_openai import ChatOpenAI

warnings.filterwarnings("ignore", message=".*allowed_objects.*")

from deepagents import create_deep_agent

sys.stdout.reconfigure(encoding="utf-8")

# Same LM Studio initialization as the original script.
llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="openai/gpt-oss-20b",
    temperature=0.1,
)


OPTIMIST_SYSTEM = (
    "You are an extreme optimist in a structured debate. Argue the maximum "
    "upside, growth, and opportunity of the topic. When earlier pessimistic "
    "points are included in the task, rebut them directly. Return EXACTLY "
    "3 short points, one per line, with no numbering and no preamble."
)

PESSIMIST_SYSTEM = (
    "You are an extreme pessimist in a structured debate. Argue the severe "
    "risks, hidden costs, and technical bottlenecks of the topic. When earlier "
    "optimistic points are included in the task, rebut them directly. Return "
    "EXACTLY 3 short points, one per line, with no numbering and no preamble."
)

COORDINATOR_SYSTEM = """You run a four-turn optimist-versus-pessimist debate.

You MUST use the task tool exactly four times and in this order:

1. Call the optimist with the topic and ask for its initial 3 points.
2. Call the pessimist with the topic plus the optimist's exact points, asking
   for 3 risks or rebuttals.
3. Call the optimist again with the complete debate so far, asking for 3
   rebuttals or additional opportunities.
4. Call the pessimist again with the complete debate so far, asking for 3
   rebuttals or additional risks.

Do not skip a turn. Pass previous points into every later task so each speaker
can respond to what is already on the table.

After all four task calls, act as a neutral judge. Return EXACTLY 5 lines,
with no numbering, headings, markdown fences, or preamble:

Lines 1-2: the two strongest opportunities, each beginning with [+]
Lines 3-4: the two most serious risks, each beginning with [-]
Line 5: begin with [>] and state either:
- PROCEED, followed by a one-clause reason, or
- REVISIT, followed by a one-clause reason explaining why the risks should
  be addressed first.

Judge importance rather than simply counting claims. Do not mention agents,
delegation, task calls, or the debate process in the final five lines.
"""


subagents = [
    {
        "name": "optimist",
        "description": (
            "Produces exactly three concise opportunities or optimistic "
            "rebuttals for an idea. Use for turns 1 and 3."
        ),
        "system_prompt": OPTIMIST_SYSTEM,
        "model": llm,
    },
    {
        "name": "pessimist",
        "description": (
            "Produces exactly three concise risks or pessimistic rebuttals "
            "for an idea. Use for turns 2 and 4."
        ),
        "system_prompt": PESSIMIST_SYSTEM,
        "model": llm,
    },
]


debate_agent = create_deep_agent(
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


def is_valid_summary(text: str) -> bool:
    """Check the same five-line conclusion contract as the old script."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return (
        len(lines) == 5
        and all(line.startswith("[+]") for line in lines[:2])
        and all(line.startswith("[-]") for line in lines[2:4])
        and lines[4].startswith("[>]")
        and ("PROCEED" in lines[4] or "REVISIT" in lines[4])
    )


def repair_summary(text: str, topic: str) -> str:
    """Use the same local LLM to enforce the output format if needed."""
    response = llm.invoke(
        [
            (
                "system",
                "Reformat the supplied conclusion into EXACTLY 5 non-empty "
                "lines, with no numbering or preamble. Lines 1-2 must begin "
                "with [+] and contain the two strongest opportunities. Lines "
                "3-4 must begin with [-] and contain the two most serious "
                "risks. Line 5 must begin with [>] and contain either PROCEED "
                "or REVISIT plus a one-clause reason. Preserve the meaning and "
                "do not add unsupported claims.",
            ),
            (
                "user",
                f"Topic: {topic}\n\nConclusion to reformat:\n{text}",
            ),
        ]
    )
    return message_text(response)


def run_debate(topic: str) -> str:
    result = debate_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"Debate this topic and produce the required final "
                        f"five-line conclusion:\n\n{topic}"
                    ),
                }
            ]
        },
        {"recursion_limit": 40},
    )

    summary = message_text(result["messages"][-1])
    if not is_valid_summary(summary):
        summary = repair_summary(summary, topic)

    return summary


def main() -> None:
    topic = sys.argv[1] if len(sys.argv) > 1 else (
        "Migrating a legacy monolith to a fully decentralized "
        "AI-agent architecture."
    )
    
    png_bytes = debate_agent.get_graph(xray=1).draw_mermaid_png()
    with open("multi_agent_debate.png", "wb") as file:
        file.write(png_bytes)

    print(f"--- DEBATE --- {topic}")
    summary = run_debate(topic)

    print("\n\n--- SUMMARY ---")
    print(summary)
    print("--- /SUMMARY ---")


if __name__ == "__main__":
    main()
