from typing import List, Dict, Any
import os
from intelli_docs.core.config import settings
from fastapi import UploadFile
from intelli_docs.services.document_processor import DocumentProcessor
from intelli_docs.services.embedding_service import EmbeddingService

class DocumentService:
    """
    Service for handling document operations
    """
    
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.embedding_service = EmbeddingService()
        self.raw_dir = settings.RAW_DATA_DIR
        self.processed_dir = settings.PROCESSED_DATA_DIR
    
    async def process_document(self, file: UploadFile) -> str:
        """
        Process an uploaded document
        """
        file_path = os.path.join(self.raw_dir, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        documents = await self.document_processor.process_file(file_path)
        
        await self.document_processor.save_processed_document(file_path, documents)
        
        await self.embedding_service.add_documents(documents)
        return file.filename
    
    async def list_documents(self) -> List[Dict[str, Any]]:
        """
        List all processed documents
        """
        return await self.embedding_service.get_all_documents()
    
    async def delete_document(self, document_id: str):
        """
        Delete a document
        """
        await self.embedding_service.delete_document(document_id) 