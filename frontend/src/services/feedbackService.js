const apiClient = require('./apiClient');

const feedbackService = {
  getAllFeedbacks: async () => {
    try {
      const response = await apiClient.get('/api/feedback');
      return response.data;
    } catch (error) {
      console.error('Get all feedbacks error:', error);
      throw error.response?.data || error;
    }
  },
};

module.exports = feedbackService;

