import pytest
from src import ingest

def test_ingest_load_documents():
    docs = ingest.load_pdf_documents()
    assert isinstance(docs, list)

def test_ingest_split_documents():
    docs = ingest.load_pdf_documents()
    chunks = ingest.split_documents(docs)
    assert all(hasattr(c, "page_content") for c in chunks)

def test_ingest_add_to_chroma():
    docs = ingest.load_pdf_documents()
    chunks = ingest.split_documents(docs)
    count = ingest.add_to_chroma(chunks)
    assert isinstance(count, int)
    assert count >= 0
