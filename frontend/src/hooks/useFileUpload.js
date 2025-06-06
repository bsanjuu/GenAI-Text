import { useState, useCallback } from 'react';
import fileService from './fileService';

const useFileUpload = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);

  const uploadFile = useCallback(async (file, options = {}) => {
    setLoading(true);
    setError(null);
    setUploadProgress(0);

    const MAX_FILE_SIZE_MB = 10;
    const fileSizeMB = file.size / (1024 * 1024);
    if (fileSizeMB > MAX_FILE_SIZE_MB) {
      const errorMessage = `File size exceeds ${MAX_FILE_SIZE_MB} MB limit.`;
      setError(errorMessage);
      setLoading(false);
      throw new Error(errorMessage);
    }

    try {
      const result = await fileService.uploadFile(file, options);
      setUploadProgress(100);
      return result;
    } catch (err) {
      setError(err.message || 'Failed to upload file');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { uploadFile, loading, error, uploadProgress };
};

export default useFileUpload;

