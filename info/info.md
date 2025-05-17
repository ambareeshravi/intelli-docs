# Key components and interactions

1. Client Layer
API Client: External applications or users making requests to the system

2. API Layer
FastAPI Server: Main application server
API Routes: Endpoints for document management and QA
Request/Response Models: Data validation and serialization

3. Core Services
QAService: Orchestrates the question-answering process
EmbeddingService: Manages document embeddings and vector storage
DocumentProcessor: Handles document processing and chunking
MCP Pipeline: Implements the Model Context Protocol for structured reasoning

4. External Services
Ollama LLM: Local language model for text generation
ChromaDB: Vector database for similarity search
HuggingFace Embeddings: Embedding model for text vectorization

5. Data Storage
Raw Documents: Original uploaded files
Processed Chunks: Text chunks after processing
Vector Store: Stored document embeddings

# Key Data Flows:

### Document Processing Flow:
Raw Document → DocumentProcessor → Chunks → EmbeddingService → Vector Store

### Question Answering Flow:
Question → QAService → EmbeddingService → Similar Documents → MCP Pipeline → Answer

### Document Management Flow:
Upload → DocumentProcessor → EmbeddingService → Vector Store

# Component Responsibilities:

### QAService:
- Manages the question-answering process
- Coordinates between embedding search and answer generation
- Handles error cases and response formatting

### EmbeddingService:
- Manages document embeddings
- Handles vector storage operations
- Performs similarity searches

### DocumentProcessor:
- Processes different document types (PDF, DOCX, TXT)
- Splits documents into chunks
- Manages document metadata

### MCP Pipeline:
- Implements structured reasoning
- Manages context and answer generation
- Handles step-by-step processing

This architecture follows a clean, modular design with clear separation of concerns and well-defined interfaces between components. The system is scalable and can be extended with additional features or modified components as needed.