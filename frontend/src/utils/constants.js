export const SUMMARY_TYPES = {
    EXTRACTIVE: 'extractive',
    ABSTRACTIVE: 'abstractive',
    BULLET: 'bullet'
};

export const SUMMARY_LENGTHS = {
    SHORT: 'short',
    MEDIUM: 'medium',
    LONG: 'long'
};

export const FILE_TYPES = {
    ALLOWED_EXTENSIONS: ['.txt', '.pdf', '.docx', '.doc'],
    MAX_SIZE: 10 * 1024 * 1024, // 10MB
    MIME_TYPES: {
        'text/plain': '.txt',
        'application/pdf': '.pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
        'application/msword': '.doc'
    }
};

export const API_ENDPOINTS = {
    SUMMARIZE: '/api/summarization',
    DOCUMENTS: '/api/documents',
    FEEDBACK: '/api/feedback'
};