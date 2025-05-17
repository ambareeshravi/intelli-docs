# Intelligent Document Q&A System

An advanced Question-Answering system that leverages LLMs through Ollamma, Retrieval Augmented Generation (RAG), and Model Context Protocol (MCP) to provide intelligent responses from multiple document sources.

## Features

- 📚 Multi-source document ingestion (PDF, TXT, DOCX)
- 🔍 Smart document chunking and embedding
- 🤖 Local LLM inference using Ollama
- 🧠 Context-aware question answering
- 📝 Source attribution for answers
- ⚡ FastAPI backend with streaming responses
- 🔄 Model Context Protocol (MCP) for structured reasoning
- 🛠️ LangChain integration for orchestration

## Tech Stack

- Python 3.9+
- FastAPI
- LangChain
- Ollama
- ChromaDB (Vector Store)
- PyPDF2 (PDF Processing)
- python-docx (DOCX Processing)
- Sentence Transformers (Embeddings)

## Setup

1. Clone the repositor and cd into the directory
```bash
git clone https://github.com/ambareeshravi/intelli-docs.git
cd intelli-docs
```

2. Run the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

3. Start the FastAPI server:
```bash
uvicorn intelli_docs.main:app --reload
```

4. Access the API documentation at `http://localhost:8000/docs`


## Usage

1. Upload documents through the API endpoint
2. Wait for document processing and embedding
3. Ask questions through the QA endpoint
4. Receive responses with source attributions

## API Endpoints

- `POST /api/v1/documents/upload` - Upload new documents
- `POST /api/v1/qa/ask` - Ask questions about the documents
- `GET /api/v1/documents/list` - List all processed documents
- `DELETE /api/v1/documents/{doc_id}` - Remove a document

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 