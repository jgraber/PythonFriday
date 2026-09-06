"""The shared Chroma index behind the vault RAG examples: ObsidianLoader in, LM Studio embeddings, one collection on disk.

`vault_rag_chroma.py` and `deep_agent_rag.py` ask the same vault in the same way
and differ only in who picks the query -- a graph that retrieves once, or a Deep
Agents coordinator calling a retriever tool as often as it likes. Everything
below that choice lives here: reading the notes with `ObsidianLoader`, chunking
them with `MarkdownHeaderTextSplitter`, embedding them against LM Studio, and
persisting the result as one Chroma collection. Embedding the vault costs ~35s,
so whichever example runs first pays it and the other one starts in a tenth of
a second.

Importable and runnable. As a module it exports `load_or_build_store(rebuild)`
and `search(store, query, k)`; run on its own it builds the index -- or reports
on the one already there -- and searches it once as a self-test.

    uv run vault_index.py
    uv run vault_index.py --rebuild
    uv run vault_index.py reset
"""

import re
import shutil
import sys
import time
import warnings
from collections import Counter
from pathlib import Path

import chromadb
import openai
from langchain_openai import OpenAIEmbeddings

warnings.filterwarnings("ignore", message=".*allowed_objects.*")  # langchain_core (imported above) re-enables this; suppress before langgraph import emits it
warnings.filterwarnings("ignore", message=".*langchain-community.*")  # the loader lives in a package upstream has marked as sunset; noted in the docstring, not worth printing every run

from langchain_chroma import Chroma
from langchain_community.document_loaders import ObsidianLoader
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

sys.stdout.reconfigure(encoding="utf-8")

EMBED_MODEL = "text-embedding-nomic-embed-text-v1.5"

embeddings = OpenAIEmbeddings(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model=EMBED_MODEL,
    # Mandatory against LM Studio: with the default True, langchain-openai
    # tokenizes with tiktoken and posts token-ID arrays, and LM Studio answers
    # 400 "'input' field must be a string or an array of strings".
    check_embedding_ctx_length=False,
)

VAULT = Path("Sherlock_Holmes_Canon")
CHROMA_DIR = Path("vault_chroma")
COLLECTION = "holmes"
KIND_BY_FOLDER = {"stories": "story", "characters": "character", "places": "place"}

CHUNK_CHARS = 1200
CHUNK_OVERLAP = 150
EMBED_BATCH = 128
MAX_ATTEMPTS = 3

SAMPLE_QUERY = "a snake used as a murder weapon"
SAMPLE_K = 3

# Sections that hold nothing but [[links]]: they are edges of the graph, not
# prose. Embedding a bare list of names lets an entity note answer with its
# story's title for the wrong reason. Same exclusion as vault_rag.py -- but the
# links themselves ride along as Chroma metadata (see MAX_LINKS), because a
# retrieved note that cannot name the story it belongs to invites the model to
# guess one.
LINK_SECTIONS = {"who", "where", "appears in"}
MAX_LINKS = 8
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def is_link_section(heading: str) -> bool:
    return heading.split("(")[0].strip().lower() in LINK_SECTIONS


def link_targets(text: str) -> list[str]:
    targets: list[str] = []
    for match in LINK_RE.findall(text):
        target = match.split("|")[0].strip()
        if target and target not in targets:
            targets.append(target)
    return targets


def load_chunks() -> list[Document]:
    # ObsidianLoader globs **/*.md with no exclude hook, so it walks .obsidian/
    # too -- keep only the three note folders.
    raw = [
        doc
        for doc in ObsidianLoader(str(VAULT), collect_metadata=True).load()
        if Path(doc.metadata["path"]).parent.name in KIND_BY_FOLDER
    ]
    print(f"[load] {len(raw)} notes via ObsidianLoader")
    # A story note shows the two things worth knowing about the loader's output:
    # frontmatter is unpacked over the file-stat keys (so `created` is this
    # vault's YAML string, not the stat float), and the `tags` list arrives
    # comma-joined into one string, built from a set so the order is unstable.
    example = next(doc for doc in raw if Path(doc.metadata["path"]).parent.name == "stories")
    print(f"[load] loader metadata example: {example.metadata}")

    headers = MarkdownHeaderTextSplitter(headers_to_split_on=[("##", "section")], strip_headers=True)
    overflow = RecursiveCharacterTextSplitter(chunk_size=CHUNK_CHARS, chunk_overlap=CHUNK_OVERLAP)

    chunks: list[Document] = []
    for doc in raw:
        path = Path(doc.metadata["path"])
        kind = KIND_BY_FOLDER[path.parent.name]
        # Identity is the filename, not the frontmatter title: wikilinks resolve
        # by filename, and places/Meiringen.md carries `title: Meiringen)`.
        title = path.stem

        sections: list[tuple[str, str]] = []
        links: list[str] = []
        for part in headers.split_text(doc.page_content):
            # The preamble before the first `## ` comes back with no section key.
            section = part.metadata.get("section", "Intro")
            if is_link_section(section):
                links += [t for t in link_targets(part.page_content) if t not in links]
                continue
            # A story's preamble is one boilerplate attribution line, and the 60
            # of them share just 9 distinct strings -- 60 chunks, 9 vectors. BM25
            # discounted that for free via idf; cosine does not, so a cluster of
            # identical vectors sits at one score and crowds real answers out of
            # the top k. The collection name survives in the `tags` metadata.
            if kind == "story" and section == "Intro":
                continue
            sections.append((section, part.page_content.strip()))

        # An entity note is 78 words across Intro + Significance; splitting that
        # in two helps nobody, so it stays one chunk.
        if kind != "story":
            merged = "\n\n".join(text for _, text in sections if text)
            sections = [("Note", merged)] if merged else []

        for section, text in sections:
            if not text:
                continue
            pieces = overflow.split_text(text) if len(text) > CHUNK_CHARS else [text]
            for i, piece in enumerate(pieces):
                chunks.append(
                    Document(
                        page_content=piece,
                        metadata={
                            "chunk_id": f"{kind}/{title}::{section}::{i}",
                            "title": title,
                            "kind": kind,
                            "section": section,
                            "path": str(path),
                            "links": ", ".join(links[:MAX_LINKS]),
                        },
                    )
                )
    return chunks


def add_batch(store: Chroma, batch: list[Document]) -> None:
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            store.add_documents(batch, ids=[doc.metadata["chunk_id"] for doc in batch])
            return
        except openai.APIError as e:
            # The first call against a cold embedding model loses a JIT-load
            # race and 400s with "Failed to load model ... Operation canceled".
            print(f"[attempt {attempt}/{MAX_ATTEMPTS}] embedding call failed ({type(e).__name__}); retrying")
            if attempt == MAX_ATTEMPTS:
                raise
            time.sleep(2)


def report_staleness(collection) -> None:
    indexed = {meta["path"] for meta in collection.get(include=["metadatas"])["metadatas"]}
    on_disk = {str(path) for folder in KIND_BY_FOLDER for path in (VAULT / folder).glob("*.md")}
    if indexed == on_disk:
        print(f"[index] {len(on_disk)} notes on disk, all indexed")
        return
    print(
        f"[index] WARNING {len(on_disk)} notes on disk vs {len(indexed)} indexed "
        f"({len(on_disk - indexed)} missing, {len(indexed - on_disk)} stale) -- run --rebuild"
    )


def load_or_build_store(rebuild: bool) -> Chroma:
    t0 = time.perf_counter()
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    if rebuild:
        try:
            client.delete_collection(COLLECTION)
            print(f"[index] --rebuild: dropped collection '{COLLECTION}'")
        except Exception:
            print(f"[index] --rebuild: no collection '{COLLECTION}' to drop")

    # Chroma defaults to l2, and langchain-chroma then scores relevance with
    # 1 - distance/sqrt(2), which assumes unit-normalised vectors -- nomic-embed
    # output is not. Cosine makes the score a usable 0..1 number, which the
    # callers' score floors depend on. It reads the LIVE collection config, so
    # this has to be collection_configuration (not collection_metadata), and the
    # space is baked in at creation: changing it later needs --rebuild.
    store = Chroma(
        client=client,
        collection_name=COLLECTION,
        embedding_function=embeddings,
        collection_configuration={"hnsw": {"space": "cosine"}},
    )
    collection = client.get_collection(COLLECTION)

    if collection.count():
        print(f"[index] reusing {collection.count()} chunks from {CHROMA_DIR}/ ({time.perf_counter() - t0:.2f}s, no embedding calls)")
        report_staleness(collection)
        return store

    chunks = load_chunks()
    print(f"[index] embedding {len(chunks)} chunks with {EMBED_MODEL} -- this is the slow run")
    for start in range(0, len(chunks), EMBED_BATCH):
        batch = chunks[start : start + EMBED_BATCH]
        add_batch(store, batch)
        print(f"[index] embedded {start + len(batch)}/{len(chunks)}")
    print(f"[index] built {collection.count()} chunks in {time.perf_counter() - t0:.1f}s -> {CHROMA_DIR}/")
    report_staleness(collection)
    return store


def search(store: Chroma, query: str, k: int) -> list[dict]:
    return [
        {
            "title": doc.metadata["title"],
            "kind": doc.metadata["kind"],
            "section": doc.metadata["section"],
            "links": doc.metadata["links"],
            "text": doc.page_content,
            "score": round(score, 3),
        }
        for doc, score in store.similarity_search_with_relevance_scores(query, k=k)
    ]


def main() -> None:
    # Importing this module must have no side effects, so unlike the examples
    # that import it, the CLI guards live in main() rather than at module level.
    if "reset" in sys.argv:
        shutil.rmtree(CHROMA_DIR, ignore_errors=True)
        print(f"[reset] removed {CHROMA_DIR}/ -- the next run re-embeds the vault")
        return

    if not VAULT.is_dir():
        sys.exit(f"vault not found: {VAULT} -- build it first with: uv run holmes_workflow.py")

    store = load_or_build_store(rebuild="--rebuild" in sys.argv)

    kinds = Counter(meta["kind"] for meta in store.get(include=["metadatas"])["metadatas"])
    print(f"--- CHUNKS BY KIND --- {dict(sorted(kinds.items()))}")

    print(f"--- SELF-TEST --- {SAMPLE_QUERY}")
    for hit in search(store, SAMPLE_QUERY, SAMPLE_K):
        print(f"  {hit['score']:6.3f}  {hit['title'][:42]:42} {hit['kind']:10} > {hit['section']}")


if __name__ == "__main__":
    main()
