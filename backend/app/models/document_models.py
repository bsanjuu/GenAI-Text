from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class DocumentUploadResponse(BaseModel):
    """
    Response model for document upload
    """
    document_id: str = Field(..., description="ID of the uploaded document")
    filename: str = Field(..., description="Original filename of the document")
    content_type: str = Field(..., description="Content type of the document")
    size: int = Field(..., description="Size of the document in bytes")
    upload_timestamp: datetime = Field(..., description="Timestamp of the upload")
    text_content: str = Field(..., description="Extracted text content from the document")

class DocumentListItem(BaseModel):
    """
    Model for document list item
    """
    document_id: str = Field(..., description="ID of the document")
    filename: str = Field(..., description="Original filename of the document")
    content_type: str = Field(..., description="Content type of the document")
    size: int = Field(..., description="Size of the document in bytes")
    upload_timestamp: datetime = Field(..., description="Timestamp of the upload")
    summary_count: int = Field(0, description="Number of summaries generated for this document")

class DocumentListResponse(BaseModel):
    """
    Response model for document list
    """
    documents: List[DocumentListItem] = Field(..., description="List of documents")
    total_count: int = Field(..., description="Total number of documents")
