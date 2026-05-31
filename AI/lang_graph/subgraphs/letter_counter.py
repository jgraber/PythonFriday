"""Reusable subgraph in its own module: a letter-counting helper.

LLMs famously fumble "how many r are in raspberry?". This module wraps that
task in a tiny LangGraph subgraph you can import and drop into ANY graph. The
LLM only does the fuzzy parsing (pull the letter and word out of free-form
text); Python does the exact counting, so the answer is always right.

`make_letter_counter(input_key, output_key)` is a factory: it builds the
subgraph with a dynamically-constructed `TypedDict`, so the boundary keys
match whatever state keys the parent graph already uses. A ready-made
`letter_counter_subgraph` (keys `question`/`answer`) is exported for the
trivial drop-in case. `handles(text)` lets a parent graph ask "can you answer
this?" without knowing how the helper detects its inputs.

    uv run letter_counter.py                          # self-test, default question
    uv run letter_counter.py "how many s in mississippi?"
"""

import re
import sys
from typing import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import START, END, StateGraph

sys.stdout.reconfigure(encoding="utf-8")


LETTER_COUNT_RE = re.compile(
    r"how many ['\"]?(\w)['\"]?'?s?\s+(?:are |is )?in\s+(?:the word )?['\"]?(\w+)",
    re.IGNORECASE,
)


def handles_letter_counter(text: str) -> bool:
    """True if this helper can answer `text` (a 'how many <letter> in <word>' question)."""
    return LETTER_COUNT_RE.search(text) is not None


def make_letter_counter(llm: ChatOpenAI, input_key: str = "question", output_key: str = "answer"):
    State = TypedDict(
        "LetterCounterState",
        {input_key: str, "letter": str, "word": str, "count": int, output_key: str},
    )

    def parse_question(state: State) -> dict:
        question = state[input_key]
        print(f"[parse_question] LLM extracting (letter, word) from: {question!r}")
        response = llm.invoke([
            ("system", "Extract the single letter and the single word the user "
                       "wants counted. Reply with EXACTLY the letter, a space, "
                       "then the word. No quotes, no extra text. "
                       "Example: 'how many r in raspberry?' -> r raspberry"),
            ("user", question),
        ])
        parts = response.content.strip().split()
        if len(parts) == 2 and len(parts[0]) == 1 and parts[1].isalpha():
            letter, word = parts[0], parts[1]
        else:
            m = LETTER_COUNT_RE.search(question)
            if not m:
                raise ValueError(f"Could not parse a letter and word from: {question!r}")
            print("[parse_question] LLM output unusable, used regex fallback")
            letter, word = m.group(1), m.group(2)
        return {"letter": letter, "word": word}

    def count_letter(state: State) -> dict:
        letter = state["letter"]
        word = state["word"]
        count = word.lower().count(letter.lower())
        print(f"[count_letter] Python counted {letter!r} in {word!r}: {count}")
        return {"count": count}

    def format_answer(state: State) -> dict:
        letter = state["letter"]
        word = state["word"]
        count = state["count"]
        sentence = f"There are {count} '{letter.lower()}'s in '{word.lower()}'."
        print(f"[format_answer] {sentence}")
        return {output_key: sentence}

    g = StateGraph(State)

    g.add_node("parse_question", parse_question)
    g.add_node("count_letter", count_letter)
    g.add_node("format_answer", format_answer)

    g.add_edge(START, "parse_question")
    g.add_edge("parse_question", "count_letter")
    g.add_edge("count_letter", "format_answer")
    g.add_edge("format_answer", END)

    return g.compile()

def main() -> None:
    llm = ChatOpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio",
        model="openai/gpt-oss-20b",
        temperature=0.1,
    )
    
    letter_counter_subgraph = make_letter_counter(llm)
    
    question = sys.argv[1] if len(sys.argv) > 1 else "how many r are in raspberry?"

    result = letter_counter_subgraph.invoke({"question": question})

    print("\n--- ANSWER ---")
    print(result["answer"])
    print("--- /ANSWER ---")


if __name__ == "__main__":
    main()
