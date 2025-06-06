import pytest
from datetime import datetime
from app.services.feedback_service import feedback_service

class TestFeedbackService:
    """
    Test cases for the feedback service
    """

    def setup_method(self):
        """Setup for each test method"""
        # Clear feedback store before each test
        feedback_service.feedback_store.clear()

    def test_submit_positive_feedback(self):
        """Test submitting positive feedback"""
        summary_id = "test_summary_123"
        feedback_type = "positive"
        comments = "This summary was very helpful and accurate."

        result = feedback_service.submit_feedback(summary_id, feedback_type, comments)

        assert result is not None
        assert "feedback_id" in result
        assert result["summary_id"] == summary_id
        assert result["feedback_type"] == feedback_type
        assert "timestamp" in result
        assert "message" in result
        assert "Thank you" in result["message"]

    def test_submit_negative_feedback(self):
        """Test submitting negative feedback"""
        summary_id = "test_summary_456"
        feedback_type = "negative"
        comments = "The summary missed important points."

        result = feedback_service.submit_feedback(summary_id, feedback_type, comments)

        assert result is not None
        assert result["feedback_type"] == feedback_type
        assert result["summary_id"] == summary_id

    def test_submit_feedback_without_comments(self):
        """Test submitting feedback without comments"""
        summary_id = "test_summary_789"
        feedback_type = "positive"

        result = feedback_service.submit_feedback(summary_id, feedback_type)

        assert result is not None
        assert result["summary_id"] == summary_id
        assert result["feedback_type"] == feedback_type

    def test_get_feedback_by_id(self):
        """Test retrieving feedback by ID"""
        summary_id = "test_summary_get"
        feedback_type = "positive"
        comments = "Great summary!"

        # Submit feedback first
        submit_result = feedback_service.submit_feedback(summary_id, feedback_type, comments)
        feedback_id = submit_result["feedback_id"]

        # Retrieve feedback
        retrieved_feedback = feedback_service.get_feedback(feedback_id)

        assert retrieved_feedback is not None
        assert retrieved_feedback["feedback_id"] == feedback_id
        assert retrieved_feedback["summary_id"] == summary_id
        assert retrieved_feedback["feedback_type"] == feedback_type
        assert retrieved_feedback["comments"] == comments
        assert "timestamp" in retrieved_feedback

    def test_get_nonexistent_feedback(self):
        """Test retrieving feedback that doesn't exist"""
        result = feedback_service.get_feedback("nonexistent_feedback_id")
        assert result == {}

    def test_get_feedback_for_summary(self):
        """Test retrieving all feedback for a specific summary"""
        summary_id = "test_summary_multiple"

        # Submit multiple feedback entries for the same summary
        feedback1 = feedback_service.submit_feedback(summary_id, "positive", "Good summary")
        feedback2 = feedback_service.submit_feedback(summary_id, "negative", "Could be better")

        # Retrieve all feedback for the summary
        result = feedback_service.get_feedback_for_summary(summary_id)

        assert len(result) == 2

        feedback_ids = list(result.keys())
        assert feedback1["feedback_id"] in feedback_ids
        assert feedback2["feedback_id"] in feedback_ids

        # Check that all feedback entries are for the correct summary
        for feedback in result.values():
            assert feedback["summary_id"] == summary_id

    def test_get_feedback_for_summary_no_feedback(self):
        """Test retrieving feedback for summary with no feedback"""
        result = feedback_service.get_feedback_for_summary("summary_with_no_feedback")
        assert result == {}

    def test_feedback_timestamp(self):
        """Test that feedback includes proper timestamp"""
        before_submit = datetime.now()

        result = feedback_service.submit_feedback("test_summary", "positive", "Test")
        feedback_id = result["feedback_id"]

        after_submit = datetime.now()

        # Get the stored feedback
        stored_feedback = feedback_service.get_feedback(feedback_id)
        timestamp = stored_feedback["timestamp"]

        # Timestamp should be between before and after submission
        assert before_submit <= timestamp <= after_submit

    def test_multiple_feedback_for_different_summaries(self):
        """Test multiple feedback entries for different summaries"""
        summary1 = "summary_1"
        summary2 = "summary_2"

        # Submit feedback for different summaries
        feedback1 = feedback_service.submit_feedback(summary1, "positive", "Good")
        feedback2 = feedback_service.submit_feedback(summary2, "negative", "Bad")
        feedback3 = feedback_service.submit_feedback(summary1, "positive", "Also good")

        # Check feedback for summary1
        result1 = feedback_service.get_feedback_for_summary(summary1)
        assert len(result1) == 2

        # Check feedback for summary2
        result2 = feedback_service.get_feedback_for_summary(summary2)
        assert len(result2) == 1

        # Verify feedback IDs are unique
        all_feedback_ids = list(result1.keys()) + list(result2.keys())
        assert len(all_feedback_ids) == len(set(all_feedback_ids))  # All unique

    def test_feedback_storage_persistence(self):
        """Test that feedback is properly stored and persists"""
        summary_id = "persistent_test"
        feedback_type = "positive"
        comments = "Persistent feedback test"

        # Submit feedback
        result = feedback_service.submit_feedback(summary_id, feedback_type, comments)
        feedback_id = result["feedback_id"]

        # Verify it's in the store
        assert feedback_id in feedback_service.feedback_store

        stored_feedback = feedback_service.feedback_store[feedback_id]
        assert stored_feedback["summary_id"] == summary_id
        assert stored_feedback["feedback_type"] == feedback_type
        assert stored_feedback["comments"] == comments

    def test_feedback_id_uniqueness(self):
        """Test that feedback IDs are unique"""
        feedback_ids = set()

        # Submit multiple feedback entries
        for i in range(10):
            result = feedback_service.submit_feedback(f"summary_{i}", "positive", f"Test {i}")
            feedback_id = result["feedback_id"]

            # Ensure ID is unique
            assert feedback_id not in feedback_ids
            feedback_ids.add(feedback_id)