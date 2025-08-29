import logging
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from retriever import retrieve
from prompts import TIERED_TEMPLATE
from error_parser import parse_error


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the OpenAI Chat model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Prompt template for hint generation
prompt = PromptTemplate.from_template(TIERED_TEMPLATE)

# Output parser
output_parser = StrOutputParser()

# Function to format retrieved chunks into text and citations
def process_retrieved_context(docs):
    logger.info("🔍 Formatting retrieved context...")
    if not docs or not isinstance(docs, list):
        return "", []

    context_str = "\n".join([doc.page_content for doc in docs])
    citations = [
        {"source": doc.metadata.get("source", "unknown"), "anchor": doc.metadata.get("anchor", "N/A")}
        for doc in docs
    ]

    return context_str, citations

# Chain for generating the response
chain = (
    RunnableParallel({
        "error": RunnableLambda(lambda x: parse_error(x["query"])),
        "query": RunnablePassthrough(),
        "context": RunnableLambda(lambda x: process_retrieved_context(retrieve(x["query"]))[0]),
        "citations": RunnableLambda(lambda x: process_retrieved_context(retrieve(x["query"]))[1]),
        "tier": RunnableLambda(lambda x: x["tier"])
    })
    | prompt
    | llm
    | output_parser
)

def answer(query: str, code_snippet: str = None, explicit_request: int = None) -> str:
    """
    Generate a tiered hint response for a given error message and optional code snippet.

    Parameters:
        query (str): The error message or user question.
        code_snippet (str, optional): Additional code context.
        explicit_request (int, optional): Desired help tier (1 to 4).

    Returns:
        str: Tiered hint response from the assistant.
    """
    logger.info(f"🧠 Generating answer for query with tier {explicit_request}")
    try:
        question = query.strip()
        if code_snippet:
            question += f"\n\nCode:\n{code_snippet.strip()}"

        inputs = {
            "query": question,
            "tier": explicit_request
        }

        response = chain.invoke(inputs)
        logger.info("✅ Successfully generated response")
        return response
    except Exception as e:
        logger.error(f"❌ Error generating answer: {e}")
        raise
