import { FILE_TYPES } from './constants';

export const validateFile = (file) => {
    const errors = [];

    if (!file) {
        errors.push('No file selected');
        return { isValid: false, errors };
    }

    // Check file size
    if (file.size > FILE_TYPES.MAX_SIZE) {
        errors.push(`File size exceeds ${FILE_TYPES.MAX_SIZE / (1024 * 1024)}MB limit`);
    }

    // Check file extension
    const extension = '.' + file.name.split('.').pop().toLowerCase();
    if (!FILE_TYPES.ALLOWED_EXTENSIONS.includes(extension)) {
        errors.push(`File type not allowed. Allowed types: ${FILE_TYPES.ALLOWED_EXTENSIONS.join(', ')}`);
    }

    return {
        isValid: errors.length === 0,
        errors
    };
};

export const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};