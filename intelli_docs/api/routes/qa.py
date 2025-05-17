from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from intelli_docs.services.qa_service import QAService
from intelli_docs.services.embedding_service import EmbeddingService
from intelli_docs.api.models.models import QuestionRequest, DocumentResponse, AnswerResponse
import os
from intelli_docs.core.config import settings

router = APIRouter()
qa_service = QAService()
embedding_service = EmbeddingService()

@router.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    """
    Ask a question about the uploaded documents
    """
    try:
        response = qa_service.answer_question(
            question=request.question,
            n_context_docs=request.n_context_docs
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/upload")
def upload_document(file: UploadFile = File(...)):
    """
    Upload a document for question answering
    """
    try:
        # Save the file
        file_path = os.path.join(settings.DATA_DIR, "raw", file.filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        
        # Process the document
        embedding_service.process_document(file_path)
        
        return {
            "message": "Document uploaded and processed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents", response_model=List[DocumentResponse])
def list_documents():
    """
    List all processed documents
    """
    try:
        documents = embedding_service.list_documents()
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/documents/{document_id}")
def delete_document(document_id: str):
    """
    Delete an existing document
    """
    try:
        embedding_service.delete_document(document_id)
        return {
            "message": "Document deleted successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 