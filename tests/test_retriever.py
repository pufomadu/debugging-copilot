from src.retriever import retrieve

def test_retrieve_returns_list():
    results = retrieve("What is SQL?", k=2)
    assert isinstance(results, list)

def test_retrieve_contains_documents():
    results = retrieve("What is SQL?", k=1)
    assert hasattr(results[0], "page_content")

def test_retrieve_empty_query():
    results = retrieve("", k=2)
    assert isinstance(results, list)  # Should fail gracefully
