from fastapi import APIRouter, HTTPException, Depends
from app.models.feedback_models import FeedbackRequest, FeedbackResponse
from app.services.feedback_service import feedback_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    """
    Submit feedback for a summary
    """
    try:
        feedback_result = feedback_service.submit_feedback(
            summary_id=request.summary_id,
            feedback_type=request.feedback_type,
            comments=request.comments
        )

        return FeedbackResponse(**feedback_result)

    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error submitting feedback: {str(e)}")

@router.get("/{feedback_id}")
async def get_feedback(feedback_id: str):
    """
    Get feedback by ID
    """
    try:
        feedback = feedback_service.get_feedback(feedback_id)
        if not feedback:
            raise HTTPException(status_code=404, detail=f"Feedback with ID '{feedback_id}' not found")

        return feedback

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving feedback: {str(e)}")

@router.get("/summary/{summary_id}")
async def get_feedback_for_summary(summary_id: str):
    """
    Get all feedback for a specific summary
    """
    try:
        feedback = feedback_service.get_feedback_for_summary(summary_id)
        return {"summary_id": summary_id, "feedback": feedback}

    except Exception as e:
        logger.error(f"Error retrieving feedback for summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving feedback for summary: {str(e)}")