from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

class FeedbackRequest(BaseModel):
    """
    Request model for feedback submission
    """
    summary_id: str = Field(..., description="ID of the summary being rated")
    feedback_type: Literal["positive", "negative"] = Field(..., description="Type of feedback")
    comments: str = Field("", description="Optional comments from the user")

class FeedbackResponse(BaseModel):
    """
    Response model for feedback submission
    """
    feedback_id: str = Field(..., description="ID of the submitted feedback")
    summary_id: str = Field(..., description="ID of the summary being rated")
    feedback_type: str = Field(..., description="Type of feedback")
    timestamp: datetime = Field(..., description="Timestamp of the feedback submission")
    message: str = Field(..., description="Confirmation message")
