"""RAG over an Obsidian vault with Chroma: one retrieve hop, a score floor, and an abstain branch.

The library version of `vault_rag.py`. Where that file hand-rolls everything --
`frontmatter.load` + glob to read, a regex to chunk, BM25 to score, nothing on
disk -- this one hands each layer to a library: `ObsidianLoader` reads,
`MarkdownHeaderTextSplitter` chunks, `OpenAIEmbeddings` against LM Studio scores,
and Chroma persists. That whole index layer lives in `vault_index.py`, shared
with `deep_agent_rag.py`; what reads top to bottom here is the graph above it.
Embedding the vault costs ~35s, so the index is built once and then reused: only
`--rebuild` pays that cost again.

Embeddings buy synonymy, which is exactly what BM25 could not do. `vault_rag.py`
answers "which case did a woman outwit Holmes?" with A Case Of Identity; this one
retrieves Irene Adler.

What they cost is a usable abstain signal. BM25 scores term overlap, so a
question about Kubernetes matches nothing and scores near zero; cosine similarity
always has a nearest neighbour, and unrelated English prose still lands around
0.5. Measured here, real questions score 0.661-0.806 and junk 0.453-0.611 -- a
0.05 margin, against BM25's 2.5-vs-8.2. `MIN_SCORE` still works on this vault,
but it is a knife edge, not a comfortable floor.

    uv run vault_rag_chroma.py
    uv run vault_rag_chroma.py --rebuild
    uv run vault_rag_chroma.py ask "which case did a woman outwit Holmes?"
    uv run vault_rag_chroma.py reset
"""

import shutil
import sys
import time
import warnings
from typing import TypedDict

import openai
from langchain_openai import ChatOpenAI

warnings.filterwarnings("ignore", message=".*allowed_objects.*")  # langchain_core (imported above) re-enables this; suppress before langgraph import emits it

from langgraph.graph import START, END, StateGraph

from vault_index import CHROMA_DIR, VAULT, load_or_build_store, search

sys.stdout.reconfigure(encoding="utf-8")

llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="openai/gpt-oss-20b",
    temperature=0.1,
)

DEFAULT_QUESTION = "which story involves a snake as a murder weapon?"

TOP_K = 6
# Measured over 15 real and 8 junk questions: real questions top out at
# 0.661-0.806, junk at 0.453-0.611. A floor of 0.635 splits them, but the margin
# is only 0.05 wide -- see the docstring. vault_rag.py's BM25 had 2.5 vs 8.2.
MIN_SCORE = 0.635
MAX_ATTEMPTS = 3

ANSWER_PROMPT = """\
You answer questions about a Sherlock Holmes vault of notes. Use ONLY the notes
in CONTEXT, never outside knowledge. Reply with at most 5 sentences and no
preamble. Cite every note you relied on inline as its [[...]] link, copied from
CONTEXT character for character; never cite by number, never put anything but the
note title inside the brackets, and never copy the "-- kind, section" header that
follows a link in CONTEXT. If CONTEXT does not answer the question, reply with
exactly: NOT IN VAULT
"""


class State(TypedDict):
    question: str
    hits: list[dict]
    answer: str


def invoke_llm(system: str, user: str) -> str:
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            reply = llm.invoke([("system", system), ("user", user)])
            return reply.content if isinstance(reply.content, str) else str(reply.content)
        except openai.APIError as e:
            print(f"[attempt {attempt}/{MAX_ATTEMPTS}] LLM call failed ({type(e).__name__}); retrying")
            if attempt == MAX_ATTEMPTS:
                raise
            time.sleep(2)


def format_chunks(chunks: list[dict]) -> str:
    # The title goes into the context already wrapped as a wikilink: the model
    # copies what it sees, and a citation like [[Note (place) > Note]] would not
    # resolve when the answer is pasted back into Obsidian. The note's own links
    # come along for the same reason -- without them the model knows Irene Adler
    # outwitted Holmes but has to invent the story that happened in.
    blocks = []
    for chunk in chunks:
        block = f"[[{chunk['title']}]] -- {chunk['kind']}, section {chunk['section']}\n{chunk['text']}"
        if chunk["links"]:
            linked = ", ".join(f"[[{target}]]" for target in chunk["links"].split(", "))
            block += f"\nlinked notes: {linked}"
        blocks.append(block)
    return "\n\n".join(blocks)


def print_chunks(header: str, chunks: list[dict]) -> None:
    print(f"--- {header} ---")
    for chunk in chunks:
        print(f"  {chunk['score']:6.3f}  {chunk['title'][:42]:42} {chunk['kind']:10} > {chunk['section']}")


def retrieve(state: State) -> State:
    print(f"[retrieve] cosine search for {TOP_K} chunks in {CHROMA_DIR}/")
    hits = search(store, state["question"], TOP_K)
    print_chunks(f"TOP {len(hits)} CHUNKS", hits)
    return {"hits": hits}


def route(state: State) -> str:
    top = state["hits"][0]["score"] if state["hits"] else 0.0
    dest = "answer" if top >= MIN_SCORE else "abstain"
    print(f"[route] top score {top:.3f} vs floor {MIN_SCORE} -> {dest}")
    return dest


def abstain(state: State) -> State:
    print("[abstain] no chunk clears the floor; the vault does not cover this, not calling the LLM")
    return {"answer": ""}


def answer(state: State) -> State:
    print(f"[answer] {len(state['hits'])} chunks -> LLM")
    reply = invoke_llm(ANSWER_PROMPT, f"QUESTION: {state['question']}\n\nCONTEXT:\n{format_chunks(state['hits'])}")
    print("\n--- ANSWER ---")
    print(reply.strip())
    return {"answer": reply.strip()}


if "reset" in sys.argv:
    shutil.rmtree(CHROMA_DIR, ignore_errors=True)
    print(f"[reset] removed {CHROMA_DIR}/ -- the next run re-embeds the vault")
    sys.exit(0)

if not VAULT.is_dir():
    sys.exit(f"vault not found: {VAULT} -- build it first with: uv run holmes_workflow.py")

store = load_or_build_store(rebuild="--rebuild" in sys.argv)

workflow = StateGraph(State)

workflow.add_node("retrieve", retrieve)
workflow.add_node("abstain", abstain)
workflow.add_node("answer", answer)

workflow.add_edge(START, "retrieve")
workflow.add_conditional_edges("retrieve", route, {"abstain": "abstain", "answer": "answer"})
workflow.add_edge("abstain", END)
workflow.add_edge("answer", END)

graph = workflow.compile()
png_bytes = graph.get_graph(xray=1).draw_mermaid_png()
with open("vault_rag_chroma.png", "wb") as f:
    f.write(png_bytes)


def main() -> None:
    args = [arg for arg in sys.argv[1:] if arg != "--rebuild"]
    if args and args[0] == "ask":
        args = args[1:]
    question = " ".join(args) if args else DEFAULT_QUESTION

    print(f"--- QUESTION --- {question}")
    graph.invoke({"question": question, "hits": [], "answer": ""})


if __name__ == "__main__":
    main()
