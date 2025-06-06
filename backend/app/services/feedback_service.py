import uuid
from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class FeedbackService:
    def __init__(self):
        # In a real implementation, this would use a database
        # For now, we'll use an in-memory dictionary
        self.feedback_store = {}
    
    def submit_feedback(self, summary_id: str, feedback_type: str, comments: str = "") -> Dict[str, Any]:
        """
        Submit feedback for a summary
        
        Args:
            summary_id: ID of the summary being rated
            feedback_type: Type of feedback (positive or negative)
            comments: Optional comments from the user
            
        Returns:
            A dictionary containing the feedback information
        """
        feedback_id = str(uuid.uuid4())
        timestamp = datetime.now()
        
        feedback = {
            "feedback_id": feedback_id,
            "summary_id": summary_id,
            "feedback_type": feedback_type,
            "comments": comments,
            "timestamp": timestamp
        }
        
        # Store the feedback
        self.feedback_store[feedback_id] = feedback
        
        logger.info(f"Feedback submitted: {feedback_id} for summary {summary_id}")
        
        return {
            "feedback_id": feedback_id,
            "summary_id": summary_id,
            "feedback_type": feedback_type,
            "timestamp": timestamp,
            "message": "Thank you for your feedback! This helps improve our AI models."
        }
    
    def get_feedback(self, feedback_id: str) -> Dict[str, Any]:
        """
        Get feedback by ID
        
        Args:
            feedback_id: ID of the feedback to retrieve
            
        Returns:
            The feedback information
        """
        return self.feedback_store.get(feedback_id, {})
    
    def get_feedback_for_summary(self, summary_id: str) -> Dict[str, Any]:
        """
        Get all feedback for a summary
        
        Args:
            summary_id: ID of the summary
            
        Returns:
            Dictionary of feedback for the summary
        """
        return {
            feedback_id: feedback for feedback_id, feedback in self.feedback_store.items()
            if feedback["summary_id"] == summary_id
        }

# Create a singleton instance
feedback_service = FeedbackService()
