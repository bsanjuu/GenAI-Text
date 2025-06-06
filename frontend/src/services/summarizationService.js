import axios from 'axios';

// Get API endpoint from environment variables
const API_URL = process.env.REACT_APP_API_ENDPOINT || 'https://your-api-gateway-url.execute-api.region.amazonaws.com/prod';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Text Summarization API service
 */
const summarizationService = {
  /**
   * Submit text for summarization
   * @param {string} text - The text to summarize
   * @param {object} options - Summarization options
   * @returns {Promise} - Promise containing summarization result
   */
  summarizeText: async (text, options = {}) => {
    try {
      const response = await apiClient.post('/summarize', {
        text,
        max_length: options.maxLength || 150,
        min_length: options.minLength || 40,
      });
      return response.data;
    } catch (error) {
      console.error('Summarization error:', error);
      throw error.response?.data || error;
    }
  },

  /**
   * Upload a document file for summarization
   * @param {File} file - The document file to upload
   * @param {object} options - Summarization options
   * @returns {Promise} - Promise containing document upload result
   */
  uploadDocument: async (file, options = {}) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('max_length', options.maxLength || 150);
      formData.append('min_length', options.minLength || 40);

      const response = await axios.post(`${API_URL}/documents`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      console.error('Document upload error:', error);
      throw error.response?.data || error;
    }
  },

  /**
   * Get a specific document summary
   * @param {string} documentId - Document identifier
   * @returns {Promise} - Promise containing document summary
   */
  getSummary: async (documentId) => {
    try {
      const response = await apiClient.get(`/documents/${documentId}`);
      return response.data;
    } catch (error) {
      console.error('Get summary error:', error);
      throw error.response?.data || error;
    }
  },

  /**
   * Submit user feedback for a summary
   * @param {object} feedback - Feedback data
   * @returns {Promise} - Promise containing feedback submission result
   */
  submitFeedback: async (feedback) => {
    try {
      const response = await apiClient.post('/feedback', feedback);
      return response.data;
    } catch (error) {
      console.error('Feedback submission error:', error);
      throw error.response?.data || error;
    }
  },
};

export default summarizationService;
