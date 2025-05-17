import requests
import json
from pathlib import Path
import time
from typing import Dict, Any
import sys

class DocumentQATester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1"
        
    def print_response(self, response: requests.Response, title: str = "Response"):
        """Pretty print the API response."""
        print(f"\n{'='*50}")
        print(f"{title}")
        print(f"{'='*50}")
        print(f"Status Code: {response.status_code}")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
        print(f"{'='*50}\n")

    def upload_document(self, file_path: str) -> Dict[str, Any]:
        """Upload a document to the system."""
        print(f"\nUploading document: {file_path}")
        with open(file_path, 'rb') as f:
            files = {'file': (Path(file_path).name, f)}
            response = requests.post(f"{self.api_url}/documents/upload", files=files)
            self.print_response(response, "Upload Response")
            return response.json()

    def ask_question(self, question: str, n_context_docs: int = 3) -> Dict[str, Any]:
        """Ask a question about the documents."""
        print(f"\nAsking question: {question}")
        payload = {
            "question": question,
            "n_context_docs": n_context_docs
        }
        response = requests.post(
            f"{self.api_url}/ask",
            json=payload
        )
        self.print_response(response, "Question Response")
        return response.json()

    def list_documents(self) -> Dict[str, Any]:
        """List all documents in the system."""
        print("\nListing all documents")
        response = requests.get(f"{self.api_url}/documents")
        self.print_response(response, "Documents List")
        return response.json()

    def delete_document(self, document_id: str) -> Dict[str, Any]:
        """Delete a document from the system."""
        print(f"\nDeleting document: {document_id}")
        response = requests.delete(f"{self.api_url}/documents/{document_id}")
        self.print_response(response, "Delete Response")
        return response.json()

def main():
    # Initialize tester
    tester = DocumentQATester()
    
    # Test document path
    test_doc_path = "data/raw/test_document.txt"
    
    try:
        # 1. Upload document
        upload_response = tester.upload_document(test_doc_path)
        document_id = upload_response.get('document_id')
        
        # Wait for processing
        print("Waiting for document processing...")
        time.sleep(2)
        
        # 2. List documents
        tester.list_documents()
        
        # 3. Ask questions
        questions = [
            "What is the difference between AI and ML?",
            "What are the key concepts in AI and ML?",
            "What are some recent developments in AI?",
            "What are the future trends in AI?",
            "How does deep learning work?"
        ]
        
        for question in questions:
            tester.ask_question(question)
            time.sleep(1)  # Small delay between questions
        
        # 4. List documents again
        tester.list_documents()
        
        # 5. Delete document (optional)
        if document_id:
            delete_response = tester.delete_document(document_id)
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server. Make sure it's running at http://localhost:8000")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Test document not found at {test_doc_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 