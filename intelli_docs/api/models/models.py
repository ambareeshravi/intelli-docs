from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class QuestionRequest(BaseModel):
    """
    Request model for asking questions
    """
    question: str
    n_context_docs: Optional[int] = 3

class DocumentResponse(BaseModel):
    id: str
    content: str
    metadata: dict

class DocumentMetadata(BaseModel):
    """
    Model for document metadata
    """
    source: str
    chunk_index: int
    additional_info: Optional[Dict[str, Any]] = None

class SourceDocument(BaseModel):
    """
    Model for source document information
    """
    content: str
    metadata: DocumentMetadata
    relevance_score: float

class AnswerResponse(BaseModel):
    """
    Response model for question answers
    """
    answer: str
    sources: List[Dict[str, Any]]
    analysis: Dict[str, Any]

class DocumentUploadResponse(BaseModel):
    """
    Response model for document upload
    """
    document_id: str
    status: str
    message: str
    chunks_processed: int

class DocumentListResponse(BaseModel):
    """
    Response model for listing documents
    """
    documents: List[Dict[str, Any]]
    total_documents: int

class ErrorResponse(BaseModel):
    """
    Error response model
    """
    error: str
    detail: Optional[str] = None 