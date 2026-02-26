# uv pip install chromadb langchain-text-splitters

import re
import sys
import uuid
from pathlib import Path
import pprint

import chromadb
from chromadb.config import Settings
from langchain_text_splitters import MarkdownHeaderTextSplitter


def process_markdown_metadata(md_text: str):
    """Extract the metadata in the header and replace it with the title as level 1 header."""
    
    # Extract header
    header_match = re.search(r"^---\n(.*?)\n---", md_text, re.DOTALL)
    if not header_match:
        raise ValueError("No header section found")

    header = header_match.group(1)

    categories = []
    tags = []
    title = None
    published_on = None
    current_key = None

    for line in header.splitlines():
        line = line.strip()

        if line.startswith("title:"):
            title = line.split("title:", 1)[1].strip().strip('"')

        elif line.startswith("date:"):
            published_on = line.split("date:", 1)[1].strip()

        elif line.startswith("categories:"):
            current_key = "categories"

        elif line.startswith("tags:"):
            current_key = "tags"

        elif line.startswith("-") and current_key:
            value = line.lstrip("-").strip().strip('"')
            if current_key == "categories":
                categories.append(value)
            elif current_key == "tags":
                tags.append(value)

        else:
            current_key = None

    # Build dictionary with joined strings
    meta_dict = {
        "categories": " | ".join(categories),
        "tags": " | ".join(tags),
        "published_on": published_on,
    }

    # Replace header section with title header
    new_md = re.sub(
        r"^---\n.*?\n---",
        f"# {title}",
        md_text,
        flags=re.DOTALL
    )
    
    match_id = re.match(r"#(\d+)", title)
    if match_id:
        meta_dict["No"] = match_id.group(1)
    else:
        meta_dict["No"] = str(uuid.uuid4())
    
    new_md = new_md.replace("<!-- more -->", "", 1)

    return meta_dict, new_md


def add_reference(d: dict) -> dict:
    """Generate a reference out of Header 1 / Header 2 sections"""
    parts = []
    # pprint.pp(d)
    if "Header 1" in d:
        parts.append(d["Header 1"])
    if "Header 2" in d:
        parts.append(d["Header 2"])
        
    if parts:
        d["Reference"] = " / ".join(parts)
    # print(d["Reference"])
    return d


def get_markdown_splitter():
    """"Create a MarkdownHeaderTextSplitter with the header list to split on."""
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]

    return MarkdownHeaderTextSplitter(headers_to_split_on)


def split_file(path, splitter):
    """Splits a file into parts and adds metadata."""
    with open(path, 'r', encoding="utf-8") as file_content:
        document = file_content.read()
    
    basic_metadata, document = process_markdown_metadata(document)
    md_splits = splitter.split_text(document)
    
    part = 1
    for entry in md_splits:
        entry.metadata = add_reference(entry.metadata) | basic_metadata
        entry.metadata["Id"] = entry.metadata["No"] + "-" + str(part)
        part += 1
        
    return md_splits


def process_files(path, markdown_splitter):
    document_splits = []  
    
    if path.is_dir():
        md_files = sorted(path.rglob("*.md"))
        for md_file in md_files:
            print(md_file)
            document_splits.extend(split_file(md_file, markdown_splitter))

    elif path.is_file():
        print(path)
        document_splits.extend(split_file(path, markdown_splitter))

    else:
        raise FileNotFoundError(f"Path does not exist or is not a file/directory: {path}")
    
    
    return document_splits
    
    # for doc in document_splits:
    #     print(f"{doc.metadata["Reference"]} - {doc.metadata["No"]} - {doc.metadata["Id"]}")
    # print(f"Total splits: {len(document_splits)}")
    # ids = [doc.metadata["Id"] for doc in document_splits]
    # pprint.pp(ids)


def store_splits(splits):
    """Store the document splits in ChromaDB"""
    ids = [doc.metadata["Id"] for doc in splits]
    docs = [doc.page_content for doc in splits]
    metadatas = [doc.metadata for doc in splits]
    # pprint.pp(ids)
    # pprint.pp(docs)
    # pprint.pp(metadata)
    telemetry_off = Settings(anonymized_telemetry=False)
    client = chromadb.PersistentClient(path="PythonFridayRAG.chroma", settings=telemetry_off)

    # create a collection
    collection = client.get_or_create_collection(name="posts")

    # add a few documents
    collection.upsert(
        documents = docs,
        ids=ids,
        metadatas=metadatas,
    )

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Usage: python pf_rag_index.py <file-or-folder>")
    
    path = Path(sys.argv[1])
    
    splitter = get_markdown_splitter()
    splits = process_files(path, splitter)
    store_splits(splits)
    
