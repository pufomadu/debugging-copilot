"""
Ingest PDF slide decks into a Chroma vector database.

What this script does:
1. Loads PDFs from ./data folder
2. Splits each PDF into small text chunks
3. Converts the chunks into embeddings using OpenAI
4. Saves everything into a persistent Chroma vector database

To run this file:
    python ingest.py
"""

import os
import pathlib
import logging
from typing import List
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.documents import Document

# Load .env variables (e.g., OPENAI_API_KEY)
load_dotenv()  

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found. Did you create a .env file?")


# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
CHROMA_DIR = "./chroma_db"
DATA_DIR = pathlib.Path("./data")
EMBED_MODEL = "text-embedding-ada-002"  # This one avoids 403 access issues

# Load PDF Function

def load_pdf_documents() -> List[Document]:
    """
    Load all PDFs from the ./data directory.
    Each page becomes a separate Document object.
    """
    logger.info("📄 Loading PDFs from ./data folder...")
    loader = PyPDFDirectoryLoader(str(DATA_DIR))
    docs = loader.load()

    for i, doc in enumerate(docs, start=1):
        doc.metadata["page_or_cell"] = f"page-{i}"  # Add a fallback page tag
        doc.metadata["id"] = ""  # Will be added during chunking

    logger.info(f"✅ Loaded {len(docs)} pages from PDFs.")
    return docs

def split_documents(documents: List[Document]) -> List[Document]:
    """
    Split large documents into smaller chunks using a sliding window.
    """
    logger.info("✂️ Splitting documents into smaller chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80
    )
    chunks = splitter.split_documents(documents)
    logger.info(f"✅ Split into {len(chunks)} total chunks.")
    return chunks

def get_embeddings() -> OpenAIEmbeddings:
    """
    Return OpenAI embeddings using a safe default model.
    """
    return OpenAIEmbeddings(model=EMBED_MODEL)

def add_to_chroma(chunks: List[Document]) -> int:
    """
    Store each chunk into the Chroma vector database with unique IDs
        format: <source>::<page_or_cell>::chunk-<n>
    """
    logger.info("🧠 Saving chunks to Chroma vector DB...")
    db = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=get_embeddings()
    )

    counters = {}
    ids = []
    for chunk in chunks:
        src = chunk.metadata.get("source", "unknown")
        page_or_cell = chunk.metadata.get("page_or_cell", "unknown")
        key = (src, page_or_cell)
        counters[key] = counters.get(key, -1) + 1
        chunk_id = f"{src}::{page_or_cell}::chunk-{counters[key]}"
        chunk.metadata["id"] = chunk_id
        ids.append(chunk_id)

    if chunks:
        db.add_documents(chunks, ids=ids)
        logger.info(f"✅ Stored {len(chunks)} chunks to Chroma.")
    else:
        logger.warning("⚠️ No chunks to store!")

    return len(chunks)

# Main 
def main():
    logger.info("Starting ingestion process...")
    try:
        docs = load_pdf_documents()
        if not docs:
            logger.warning("No PDFs found in ./data. Please add slide decks.")
            return
        chunks = split_documents(docs)
        total = add_to_chroma(chunks)
        logger.info(f"🎉 Finished indexing {total} chunks into {CHROMA_DIR}")
    except Exception as e:
        logger.error(f"❌ Ingestion failed: {e}")

if __name__ == "__main__":
    main()
