"""
ingest.py — Load docs from /docs, chunk them, embed, and store in ChromaDB.
Run this once (or re-run) whenever you add/update files in /docs.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

DOCS_DIR = Path("docs")
CHROMA_DIR = Path("chroma_db")
EMBED_MODEL = "all-MiniLM-L6-v2"  # fast, local, no API key needed


def load_documents():
    docs = []

    # PDFs
    for pdf in DOCS_DIR.glob("**/*.pdf"):
        print(f"  Loading PDF: {pdf.name}")
        loader = PyPDFLoader(str(pdf))
        docs.extend(loader.load())

    # Text / Markdown files
    for ext in ("*.txt", "*.md"):
        for f in DOCS_DIR.glob(f"**/{ext}"):
            print(f"  Loading text: {f.name}")
            loader = TextLoader(str(f), encoding="utf-8")
            docs.extend(loader.load())

    return docs


def main():
    print("Loading documents...")
    docs = load_documents()
    print(f"  {len(docs)} page(s) loaded.\n")

    print("Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )
    chunks = splitter.split_documents(docs)
    print(f"  {len(chunks)} chunks created.\n")

    print(f"Embedding with '{EMBED_MODEL}' (downloading on first run)...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    print(f"Storing in ChromaDB at '{CHROMA_DIR}'...")
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name="rag_docs",
    )

    print(f"\nDone! {db._collection.count()} vectors stored in '{CHROMA_DIR}'.")


if __name__ == "__main__":
    main()
