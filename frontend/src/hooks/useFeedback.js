import { useState, useCallback } from 'react';
import feedbackService from './feedbackService';

const useFeedback = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const submitFeedback = useCallback(async (feedback) => {
    setLoading(true);
    setError(null);

    try {
      await feedbackService.submitFeedback(feedback);
    } catch (err) {
      setError(err.message || 'Failed to submit feedback');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const getFeedback = useCallback(async (id) => {
    setLoading(true);
    setError(null);

    try {
      const result = await feedbackService.getFeedback(id);
      return result;
    } catch (err) {
      setError(err.message || 'Failed to fetch feedback');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const getAllFeedbacks = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await feedbackService.getAllFeedbacks();
      return result;
    } catch (err) {
      setError(err.message || 'Failed to fetch all feedbacks');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    loading,
    error,
    submitFeedback,
    getFeedback,
    getAllFeedbacks
  };
};

export default useFeedback;

