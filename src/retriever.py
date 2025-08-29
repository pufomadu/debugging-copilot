import os
import logging
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CHROMA_DIR = "./chroma_db"

def get_embeddings():
    """Get OpenAI embeddings using ada model (no access issues)."""
    return OpenAIEmbeddings(model="text-embedding-ada-002")

def _db():
    """Initialize Chroma vector database with persisted directory."""
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=get_embeddings()
    )

def retrieve(query: str, k: int = 6):
    """
    Retrieve relevant documents based on similarity search.
    
    Returns a list of LangChain Documents with `.page_content` and `.metadata`
    """
    logger.info(f"🔍 Running vector search for query: {query}")
    results = _db().similarity_search_with_score(query, k=k)

    if not results:
        logger.warning("⚠️ No documents found for query.")
        return []

    docs = []
    for doc, score in results:
        logger.info(f"📄 Found: {doc.metadata.get('source')} - score: {score}")
        docs.append(doc)  # `doc` is a LangChain Document with page_content + metadata

    return docs
