# 🔧 Debugging Copilot — Tiered Python Help Assistant

Debugging Copilot is a Streamlit-powered study assistant that helps students unblock coding problems **and** answer conceptual questions.  
It uses **retrieval-augmented generation (RAG)** over course slides and labs to provide **tiered help**:
1. Nudge
2. Guided steps
3. Near solution
4. Full solution

## 🚀 Features

- Ingests PDF slide decks and notebooks into a **Chroma vector database**
- Splits large documents into **text chunks** for efficient retrieval
- Embeds chunks using **OpenAI embeddings**
- Retrieves relevant context when a student asks a question or pastes an error
- Provides tiered hints, from gentle nudges to full solutions
- Cites **exact slides or notebook cells** for trustworthy answers
- Runs as a **Streamlit app** with a simple UI
- Built with: LangChain, ChromaDB, OpenAI, PyPDF

### Tiered Responses:

-  Tier 1 – Nudge: Gentle conceptual guidance and where to look.
-  Tier 2 – Guided Steps: Step-by-step breakdowns and references.
-  Tier 3 – Near Solution: Skeleton code or patch hints with citation.
-  Tier 4 – Full Fix: Concise fix with citations (only if explicitly asked).

🧾 Citations: Every answer cites slides or notebook cells to avoid hallucination.


## 📂 Project Structure
        debugging-copilot/
                ├── src/
                        ├── ingest.py # Ingests PDFs into Chroma
                        ├── retriever.py # Retrieves relevant chunks
                        ├── prompts.py # Prompt template for tiered hints
                        ├── error_parser.py # Basic error pattern matching
                        ├── tiered_helper.py # Core logic: builds the chain
                        └── streamlitapp.py # Streamlit UI
                ├── tests/ # Pytest-based unit tests
                ├── data/ # Place your PDFs here
                ├── chroma_db/ # Persistent vector database
                ├── .env # Store your OpenAI key here
                ├── requirements.txt
                └── README.md

## 🔑 Environment Setup

### Setup Instructions
- Clone the repo
- git clone https://github.com/pufomadu/debugging-copilot.git
- cd debugging-copilot

### Install dependencies
- Create a virtual environment (optional), then:
- pip install -r requirements.txt

### Add your PDFs
- Place course materials (slide decks, labs, etc.) into the /data folder.

### Set up API key
- Create a .env file:
- OPENAI_API_KEY=your-key-here

### Ingest documents into vector DB
- Put your slides (PDFs) in the ./data folder, then run:
- python src/ingest.py

### Expected Output
- 📄 Loading PDFs from ./data folder...
- ✂️ Splitting documents into smaller chunks...
- 🧠 Saving chunks to Chroma vector DB...
- 🎉 Finished indexing 2000+ chunks into ./chroma_db


### Run the Streamlit App
- Start the app: 
- streamlit run src/streamlitapp.py

## 🤖 How It Works

- User input: Paste your error and select a help tier.
- Error parsing: The assistant extracts key error labels (e.g. KeyError, IndexError) using regex.
- Context retrieval: Relevant pages are pulled from your course PDFs using Chroma vector search.
- LLM reasoning: The assistant constructs a tiered response using GPT-4o (or fallback).
- Response: You get structured help, step-by-step fixes, or citations with page numbers.
  

## 📌 Example Tiers
 - User: "What is SQL?"

| Tier | Output | 
|:-------- |:--------:|
| 1     | “Check the slide titled 'SQL Review' on page 10 of the ‘Advanced SQL I.pdf’. What patterns do you notice?”   | 
| 2     | “Start by defining SQL. Then identify how it's used for data queries. Slides on page 10-12 of ‘SQL Review.pdf’ walk through this.”   | 
| 3     | “Here’s a short example of SQL: SELECT name FROM users WHERE age > 21; Refer to ‘SQL Review II.pdf’, page 7.”   | 
| 4     | “SQL (Structured Query Language) is used to manage data in relational databases. It includes commands like SELECT, INSERT, UPDATE, DELETE... [more with examples and citations]”  | 



## 🧠 Educational Use Case
This project was built for students at The Knowledge House to help them:

- Debug with less frustration
- Learn how to search contextually
- Rely on course material, not just hallucinated answers


## 🐛 Troubleshooting || ⚠️ Known Risks
- 403 Errors → Check if your OpenAI API key has access to the correct model (gpt-4o-mini).
- No PDFs found → Make sure your files are in /data and re-run ingest.py.
        If ./data is empty, ingestion will do nothing
- Answers depend on context — if slides are missing, tiers may default to nudges



## 📌 Future Improvements
- Add mock retrieval tests for offline CI
- Expand error parser for richer Python diagnostics
- Support additional file formats (notebooks, CSVs)

