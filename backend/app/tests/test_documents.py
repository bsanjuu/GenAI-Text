import pytest
from app.services.document_service import document_service

class TestDocumentService:
    """
    Test cases for the document service
    """

    def setup_method(self):
        """Setup for each test method"""
        # Clear document store before each test
        document_service.document_store.clear()
        document_service.summaries_by_document.clear()

    def test_upload_document(self):
        """Test document upload"""
        file_content = b"This is a test document content."
        filename = "test_document.txt"
        content_type = "text/plain"

        result = document_service.upload_document(file_content, filename, content_type)

        assert result is not None
        assert "document_id" in result
        assert result["filename"] == filename
        assert result["content_type"] == content_type
        assert result["size"] == len(file_content)
        assert result["text_content"] == file_content.decode('utf-8')
        assert "upload_timestamp" in result

    def test_upload_binary_document(self):
        """Test upload of binary document"""
        file_content = b"\x89PNG\r\n\x1a\n"  # PNG file header
        filename = "test_image.png"
        content_type = "image/png"

        result = document_service.upload_document(file_content, filename, content_type)

        assert result is not None
        assert result["filename"] == filename
        assert result["content_type"] == content_type
        # Binary content should be handled gracefully
        assert result["text_content"] == f"[Binary content from {filename}]"

    def test_get_document(self):
        """Test getting a document by ID"""
        file_content = b"Test content for retrieval."
        filename = "retrieve_test.txt"

        # Upload document first
        upload_result = document_service.upload_document(file_content, filename)
        document_id = upload_result["document_id"]

        # Retrieve document
        retrieved_doc = document_service.get_document(document_id)

        assert retrieved_doc is not None
        assert retrieved_doc["document_id"] == document_id
        assert retrieved_doc["filename"] == filename
        assert retrieved_doc["text_content"] == file_content.decode('utf-8')

    def test_get_nonexistent_document(self):
        """Test getting a document that doesn't exist"""
        result = document_service.get_document("nonexistent_id")
        assert result == {}

    def test_list_documents_empty(self):
        """Test listing documents when none exist"""
        result = document_service.list_documents()

        assert result["documents"] == []
        assert result["total_count"] == 0

    def test_list_documents_with_content(self):
        """Test listing documents with content"""
        # Upload multiple documents
        docs = []
        for i in range(3):
            file_content = f"Test document {i} content.".encode('utf-8')
            filename = f"test_doc_{i}.txt"
            result = document_service.upload_document(file_content, filename)
            docs.append(result)

        # List documents
        result = document_service.list_documents()

        assert len(result["documents"]) == 3
        assert result["total_count"] == 3

        # Check sorting (newest first)
        doc_list = result["documents"]
        assert all("document_id" in doc for doc in doc_list)
        assert all("filename" in doc for doc in doc_list)
        assert all("summary_count" in doc for doc in doc_list)

    def test_list_documents_pagination(self):
        """Test document listing with pagination"""
        # Upload 5 documents
        for i in range(5):
            file_content = f"Test document {i} content.".encode('utf-8')
            filename = f"test_doc_{i}.txt"
            document_service.upload_document(file_content, filename)

        # Test pagination
        result = document_service.list_documents(skip=2, limit=2)

        assert len(result["documents"]) == 2
        assert result["total_count"] == 5

    def test_delete_document(self):
        """Test document deletion"""
        file_content = b"Document to be deleted."
        filename = "delete_test.txt"

        # Upload document
        upload_result = document_service.upload_document(file_content, filename)
        document_id = upload_result["document_id"]

        # Verify document exists
        assert document_service.get_document(document_id) != {}

        # Delete document
        success = document_service.delete_document(document_id)
        assert success is True

        # Verify document is deleted
        assert document_service.get_document(document_id) == {}

    def test_delete_nonexistent_document(self):
        """Test deleting a document that doesn't exist"""
        success = document_service.delete_document("nonexistent_id")
        assert success is False

    def test_add_summary_to_document(self):
        """Test adding summary to document"""
        file_content = b"Document with summary."
        filename = "summary_test.txt"

        # Upload document
        upload_result = document_service.upload_document(file_content, filename)
        document_id = upload_result["document_id"]

        # Add summary
        summary_id = "test_summary_123"
        success = document_service.add_summary_to_document(document_id, summary_id)
        assert success is True

        # Check if summary was added
        assert document_id in document_service.summaries_by_document
        assert summary_id in document_service.summaries_by_document[document_id]

        # List documents should show summary count
        result = document_service.list_documents()
        doc = next(d for d in result["documents"] if d["document_id"] == document_id)
        assert doc["summary_count"] == 1

    def test_add_summary_to_nonexistent_document(self):
        """Test adding summary to non-existent document"""
        success = document_service.add_summary_to_document("nonexistent_id", "summary_id")
        assert success is False

    def test_content_type_detection(self):
        """Test content type detection when not provided"""
        file_content = b"Test content without explicit type."
        filename = "test.txt"

        result = document_service.upload_document(file_content, filename, None)

        assert result["content_type"] == "text/plain"

    def test_unknown_file_extension(self):
        """Test handling of unknown file extension"""
        file_content = b"Unknown file type content."
        filename = "test.unknown"

        result = document_service.upload_document(file_content, filename, None)

        assert result["content_type"] == "application/octet-stream"