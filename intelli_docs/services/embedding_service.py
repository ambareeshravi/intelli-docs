import chromadb
import os
import json

from typing import List, Dict, Any
from chromadb.config import Settings
from langchain.schema import Document as LangchainDocument
from langchain.embeddings import HuggingFaceEmbeddings
from intelli_docs.core.config import settings

class EmbeddingService:
    """
    Handles document embeddings and vector storage
    """
    
    def __init__(self):
        # Initialize the embedding model
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )
        
        # Initialize ChromaDB client
        self.client = chromadb.Client(
            Settings(
                persist_directory=str(settings.VECTOR_STORE_PATH)
            )
        )
        
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"} # use cosine similarity metric
        )
    
    def add_documents(self, documents: List[LangchainDocument]):
        """
        Add documents to the vector store
        """
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        ids = [f"doc_{idx}" for idx in range(len(documents))]
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
    
    def search_similar(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar documents to the query
        """
        query_embedding = self.embeddings.embed_query(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results # returns the top `n` results
        )

        # only use the top result
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else None
            })
        return formatted_results
    
    def process_document(self, file_path: str):
        """
        Process a document and add its chunks to the vector store
        """
        from .document_processor import DocumentProcessor
        processor = DocumentProcessor()

        # use concurrency for efficient exectution
        import asyncio
        # process file and save chunks
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        documents = loop.run_until_complete(processor.process_file(file_path))
        loop.run_until_complete(processor.save_processed_document(file_path, documents))
        # add to the vector store
        self.add_documents(documents)
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """
        List all documents in the vector store
        """
        results = self.collection.get()
        formatted_results = []
        for i in range(len(results['documents'])):
            formatted_results.append({
                'content': results['documents'][i],
                'metadata': results['metadatas'][i],
                'id': results['ids'][i]
            })
        return formatted_results
    
    def delete_document(self, document_id: str):
        """
        Delete a document from the vector store
        """
        self.collection.delete(ids=[document_id]) 