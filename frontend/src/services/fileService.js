const apiClient = require('./apiClient');

const fileService = {
  uploadFile: async (file, options = {}) => {
    try {
      const MAX_FILE_SIZE_MB = 10;
      const fileSizeMB = file.size / (1024 * 1024);
      if (fileSizeMB > MAX_FILE_SIZE_MB) {
        throw new Error(`File size exceeds ${MAX_FILE_SIZE_MB} MB limit.`);
      }

      const formData = new FormData();
      formData.append('file', file);
      Object.keys(options).forEach(key => {
        formData.append(key, options[key]);
      });

      const response = await apiClient.post('/api/documents', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return response.data;
    } catch (error) {
      console.error('File upload error:', error);
      throw error.response?.data || error;
    }
  },
};

module.exports = fileService;

