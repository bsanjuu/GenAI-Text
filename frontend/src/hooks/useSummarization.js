import { useState, useCallback } from 'react';
import summarizationService from '../services/summarizationService';

export const useSummarization = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [summary, setSummary] = useState(null);

    const summarizeText = useCallback(async (text, options = {}) => {
        setLoading(true);
        setError(null);

        try {
            const result = await summarizationService.summarizeText(text, options);
            setSummary(result);
            return result;
        } catch (err) {
            setError(err.message || 'Failed to generate summary');
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    const summarizeFile = useCallback(async (file, options = {}) => {
        setLoading(true);
        setError(null);

        try {
            const result = await summarizationService.uploadDocument(file, options);
            setSummary(result);
            return result;
        } catch (err) {
            setError(err.message || 'Failed to process document');
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    const reset = useCallback(() => {
        setSummary(null);
        setError(null);
        setLoading(false);
    }, []);

    return {
        loading,
        error,
        summary,
        summarizeText,
        summarizeFile,
        reset
    };
};