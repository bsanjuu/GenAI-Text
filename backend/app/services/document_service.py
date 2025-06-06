import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
import os
import mimetypes

logger = logging.getLogger(__name__)

class DocumentService:
    def __init__(self):
        # In a real implementation, this would use a database and file storage
        # For now, we'll use an in-memory dictionary
        self.document_store = {}
        self.summaries_by_document = {}
    
    def upload_document(self, file_content: bytes, filename: str, content_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a document and extract its text content
        
        Args:
            file_content: The content of the file
            filename: The name of the file
            content_type: The content type of the file
            
        Returns:
            A dictionary containing the document information
        """
        document_id = str(uuid.uuid4())
        upload_timestamp = datetime.now()
        
        # Determine content type if not provided
        if not content_type:
            content_type, _ = mimetypes.guess_type(filename)
            if not content_type:
                content_type = "application/octet-stream"
        
        # Extract text content (in a real implementation, this would use OCR or other text extraction methods)
        try:
            text_content = file_content.decode('utf-8')
        except UnicodeDecodeError:
            # If we can't decode as UTF-8, just use a placeholder
            text_content = f"[Binary content from {filename}]"
        
        document = {
            "document_id": document_id,
            "filename": filename,
            "content_type": content_type,
            "size": len(file_content),
            "upload_timestamp": upload_timestamp,
            "text_content": text_content
        }
        
        # Store the document
        self.document_store[document_id] = document
        self.summaries_by_document[document_id] = []
        
        logger.info(f"Document uploaded: {document_id} - {filename}")
        
        return document
    
    def get_document(self, document_id: str) -> Dict[str, Any]:
        """
        Get a document by ID
        
        Args:
            document_id: ID of the document to retrieve
            
        Returns:
            The document information
        """
        return self.document_store.get(document_id, {})
    
    def list_documents(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """
        List all documents
        
        Args:
            skip: Number of documents to skip
            limit: Maximum number of documents to return
            
        Returns:
            A dictionary containing the list of documents and total count
        """
        documents = list(self.document_store.values())
        
        # Sort by upload timestamp (newest first)
        documents.sort(key=lambda x: x.get("upload_timestamp", datetime.min), reverse=True)
        
        # Apply pagination
        paginated_documents = documents[skip:skip + limit]
        
        # Convert to list items with summary count
        document_list_items = []
        for doc in paginated_documents:
            doc_id = doc["document_id"]
            summary_count = len(self.summaries_by_document.get(doc_id, []))
            
            document_list_items.append({
                "document_id": doc["document_id"],
                "filename": doc["filename"],
                "content_type": doc["content_type"],
                "size": doc["size"],
                "upload_timestamp": doc["upload_timestamp"],
                "summary_count": summary_count
            })
        
        return {
            "documents": document_list_items,
            "total_count": len(documents)
        }
    
    def delete_document(self, document_id: str) -> bool:
        """
        Delete a document by ID
        
        Args:
            document_id: ID of the document to delete
            
        Returns:
            True if the document was deleted, False otherwise
        """
        if document_id in self.document_store:
            del self.document_store[document_id]
            if document_id in self.summaries_by_document:
                del self.summaries_by_document[document_id]
            logger.info(f"Document deleted: {document_id}")
            return True
        return False
    
    def add_summary_to_document(self, document_id: str, summary_id: str) -> bool:
        """
        Add a summary ID to a document's list of summaries
        
        Args:
            document_id: ID of the document
            summary_id: ID of the summary
            
        Returns:
            True if the summary was added, False otherwise
        """
        if document_id in self.document_store:
            if document_id not in self.summaries_by_document:
                self.summaries_by_document[document_id] = []
            
            self.summaries_by_document[document_id].append(summary_id)
            return True
        return False

# Create a singleton instance
document_service = DocumentService()
