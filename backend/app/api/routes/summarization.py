from fastapi import APIRouter, HTTPException, Depends
from app.models.summarization_models import SummarizationRequest, SummarizationResponse
from app.services.summarization_service import summarization_service
import uuid
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=SummarizationResponse)
async def summarize_text(request: SummarizationRequest):
    """
    Generate a summary of the provided text
    """
    try:
        # Generate summary using the summarization service
        summary_result = summarization_service.generate_summary(
            text=request.text,
            summary_type=request.summary_type,
            summary_length=request.summary_length
        )
        
        return SummarizationResponse(
            summary=summary_result["summary"],
            original_length=summary_result["original_length"],
            summary_length=summary_result["summary_length"],
            compression_ratio=summary_result["compression_ratio"],
            summary_type=summary_result["summary_type"]
        )
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")

@router.get("/models")
async def get_available_models():
    """
    Get a list of available summarization models
    """
    from app.services.model_service import model_service
    
    try:
        models = model_service.get_available_models()
        return {"models": models}
    except Exception as e:
        logger.error(f"Error retrieving models: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving models: {str(e)}")

@router.get("/models/{model_type}/info")
async def get_model_info(model_type: str):
    """
    Get information about a specific summarization model
    """
    from app.services.model_service import model_service
    
    try:
        model_info = model_service.get_model_info(model_type)
        if not model_info:
            raise HTTPException(status_code=404, detail=f"Model type '{model_type}' not found")
        
        return model_info
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving model info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving model info: {str(e)}")
