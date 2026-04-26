# Smart Loan EMI Advisor

A Streamlit-based application for calculating loan EMIs, providing affordability advice, and answering questions about loan documents using advanced AI.

## Features

- **Loan EMI Calculator**: Calculate monthly payments with affordability analysis
- **Tool-based EMI Calculation**: Use Ollama function calling for accurate EMI math instead of model arithmetic
- **AI Chat Advisor**: Conversational AI for loan-related questions
- **Document Q&A**: Upload PDFs/TXT and ask questions with RAG (Retrieval-Augmented Generation)
- **Structured Data Extraction**: Extract loan details from documents using Pydantic models
- **Affordability Checker**: Personalized advice based on salary and expenses

## Tech Stack

- **Language**: Python 3.14
- **UI**: Streamlit
- **AI**: Ollama with Llama 3.2 (local LLM)
- **Vector Store**: FAISS (in-process)
- **Embeddings**: Sentence-Transformers (all-MiniLM-L6-v2)
- **Structured Output**: Pydantic + LLM JSON mode
- **Dependencies**: Managed via requirements.txt

## Installation

1. Install Python 3.11+
2. Install Ollama: `winget install Ollama.Ollama`
3. Pull model: `ollama pull llama3.2:1b`
4. Clone/download the project
5. Install dependencies: `pip install -r requirements.txt`
6. Run: `streamlit run app.py`

## Usage

1. **Calculate EMI**: Enter loan details and salary/expenses for affordability check
2. **Chat with AI**: Ask general loan questions
3. **Upload Document**: Upload loan agreement PDF/TXT
4. **Ask Questions**: Get AI answers based on document content
5. **Extract Details**: Click "Extract Loan Details" for structured data

## Architecture

- **RAG Pipeline**: Document chunking → embeddings → FAISS indexing → retrieval → LLM generation
- **Error Handling**: Proper exception handling without silent failures
- **Session Management**: Conversation history and document state persistence

## Files

- `app.py`: Main application with RAG and structured output
- `requirements.txt`: Dependencies (Streamlit, Ollama, FAISS, sentence-transformers, Pydantic, PyPDF2)
- `data/loan_knowledge.txt`: Sample knowledge base
- `README.md`: This documentation