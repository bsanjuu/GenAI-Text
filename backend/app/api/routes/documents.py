from fastapi import APIRouter, HTTPException, File, UploadFile, Depends, Query
from app.models.document_models import DocumentUploadResponse, DocumentListResponse
from app.services.document_service import document_service
from app.services.summarization_service import summarization_service
import logging
from typing import Optional

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document for text extraction and summarization
    """
    try:
        # Check file size (10MB limit)
        if file.size and file.size > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")

        # Read file content
        file_content = await file.read()

        # Upload document using the service
        document = document_service.upload_document(
            file_content=file_content,
            filename=file.filename,
            content_type=file.content_type
        )

        return DocumentUploadResponse(**document)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")

@router.get("/", response_model=DocumentListResponse)
async def list_documents(
        skip: int = Query(0, ge=0, description="Number of documents to skip"),
        limit: int = Query(100, ge=1, le=1000, description="Maximum number of documents to return")
):
    """
    Get a list of uploaded documents
    """
    try:
        result = document_service.list_documents(skip=skip, limit=limit)
        return DocumentListResponse(**result)
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")

@router.get("/{document_id}")
async def get_document(document_id: str):
    """
    Get a specific document by ID
    """
    try:
        document = document_service.get_document(document_id)
        if not document:
            raise HTTPException(status_code=404, detail=f"Document with ID '{document_id}' not found")

        return document
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving document: {str(e)}")

@router.post("/{document_id}/summarize")
async def summarize_document(
        document_id: str,
        summary_type: str = Query("extractive", description="Type of summarization"),
        summary_length: str = Query("medium", description="Length of summary")
):
    """
    Generate a summary for a specific document
    """
    try:
        # Get the document
        document = document_service.get_document(document_id)
        if not document:
            raise HTTPException(status_code=404, detail=f"Document with ID '{document_id}' not found")

        # Generate summary
        summary_result = summarization_service.generate_summary(
            text=document["text_content"],
            summary_type=summary_type,
            summary_length=summary_length
        )

        # Add document ID to response
        summary_result["document_id"] = document_id

        return summary_result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error summarizing document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error summarizing document: {str(e)}")

@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """
    Delete a document by ID
    """
    try:
        success = document_service.delete_document(document_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Document with ID '{document_id}' not found")

        return {"message": f"Document '{document_id}' deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")