from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class QuestionRequest(BaseModel):
    """
    Request model for asking questions
    """
    question: str
    n_context_docs: int = 3

class Source(BaseModel):
    """
    Model for document source information
    """
    content: str
    metadata: Dict[str, Any]
    relevance_score: float

class QuestionResponse(BaseModel):
    """
    Response model for question answers
    """
    answer: str
    sources: List[Source]
    analysis: Dict[str, Any]

class DocumentUploadResponse(BaseModel):
    """
    Response model for document upload
    """
    document_id: str
    message: str

class DocumentListResponse(BaseModel):
    """
    Response model for listing documents
    """
    documents: List[Dict[str, Any]] 