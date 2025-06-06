import React, { useState } from 'react';
import './TextSummarizationTool.css';

// Import custom components
import Button from './components/common/Button';
import TextArea from './components/common/TextArea';
import FileUpload from './components/common/FileUpload';
import Rating from './components/common/Rating';
import Loading from './components/common/Loading';
import ModelSelector from './components/Settings/ModelSelector';
import AdvancedOptions from './components/Settings/AdvancedOptions';

// Import service
import summarizationService from './services/summarizationService';

// This is the main component for text summarization functionality
const TextSummarizationTool = () => {
  // State management
  const [text, setText] = useState('');
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);
  const [feedback, setFeedback] = useState('');
  const [rating, setRating] = useState(0);
  const [documentId, setDocumentId] = useState('');
  const [error, setError] = useState('');
  const [selectedModel, setSelectedModel] = useState('gpt-3.5-turbo');
  const [summaryOptions, setSummaryOptions] = useState({
    maxLength: 150,
    minLength: 40,
  });
  const [advancedOptions, setAdvancedOptions] = useState({
    temperature: 0.7,
    format: 'paragraph',
    includeKeywords: false,
    language: 'auto',
  });
  const [processingStatus, setProcessingStatus] = useState('');

  // Handle text input change
  const handleTextChange = (e) => {
    setText(e.target.value);
  };

  // Handle file upload
  const handleFileUpload = (selectedFile) => {
    setFile(selectedFile);
    // Reset any previous document ID when a new file is selected
    if (documentId) {
      setDocumentId('');
      setSummary('');
    }
  };

  // Handle options change
  const handleOptionsChange = (e) => {
    const { name, value } = e.target;
    setSummaryOptions({
      ...summaryOptions,
      [name]: parseInt(value),
    });
  };

  // Handle model selection
  const handleModelSelect = (modelId) => {
    setSelectedModel(modelId);
  };

  // Handle advanced options change
  const handleAdvancedOptionsChange = (newOptions) => {
    setAdvancedOptions(newOptions);
  };

  // Reset advanced options to defaults
  const resetAdvancedOptions = () => {
    setAdvancedOptions({
      temperature: 0.7,
      format: 'paragraph',
      includeKeywords: false,
      language: 'auto',
    });
  };

  // Handle direct text summarization
  const summarizeText = async () => {
    if (!text.trim()) {
      setError('Please enter some text to summarize');
      return;
    }

    setLoading(true);
    setError('');
    setProcessingStatus('Generating summary...');

    try {
      const result = await summarizationService.summarizeText(text, {
        ...summaryOptions,
        model: selectedModel,
        ...advancedOptions,
      });

      setSummary(result.summary);
      setDocumentId(result.document_id);
      setLoading(false);
    } catch (error) {
      console.error('Error summarizing text:', error);
      setError('An error occurred during summarization. Please try again.');
      setLoading(false);
    }
  };

  // Handle file summarization
  const summarizeFile = async () => {
    if (!file) {
      setError('Please select a file to upload');
      return;
    }

    setLoading(true);
    setError('');
    setProcessingStatus('Uploading document...');

    try {
      // First upload the document
      const uploadResult = await summarizationService.uploadDocument(file, {
        ...summaryOptions,
        model: selectedModel,
        ...advancedOptions,
      });
      const docId = uploadResult.document_id;
      setDocumentId(docId);

      // Poll for summary completion
      setProcessingStatus('Processing document...');
      let summaryReady = false;
      let attempts = 0;
      const maxAttempts = 30; // 30 * 2 seconds = 60 seconds max wait time

      while (!summaryReady && attempts < maxAttempts) {
        await new Promise(resolve => setTimeout(resolve, 2000)); // Wait 2 seconds

        try {
          const summaryResponse = await summarizationService.getSummary(docId);
          if (summaryResponse.status === 'completed') {
            setSummary(summaryResponse.summary);
            summaryReady = true;
          } else {
            setProcessingStatus(`Processing document... (${attempts + 1}/${maxAttempts})`);
          }
        } catch (err) {
          console.log('Summary not ready yet, retrying...');
        }

        attempts++;
      }

      if (!summaryReady) {
        setError('Summary generation is taking longer than expected. Please check back later.');
      }

      setLoading(false);
    } catch (error) {
      console.error('Error processing document:', error);
      setError('Error uploading or processing document. Please try again.');
      setLoading(false);
    }
  };

  // Submit feedback on the summary
  const submitFeedback = async () => {
    if (rating === 0) {
      setError('Please provide a rating before submitting feedback');
      return;
    }

    setLoading(true);
    setError('');
    setProcessingStatus('Submitting feedback...');

    try {
      await summarizationService.submitFeedback({
        document_id: documentId,
        summary_id: documentId, // Using same ID for simplicity
        rating: rating,
        feedback_text: feedback,
        original_summary: summary,
      });

      // Show success message
      setProcessingStatus('Feedback submitted successfully!');
      setTimeout(() => setProcessingStatus(''), 3000);

      // Reset feedback form
      setFeedback('');
      setRating(0);
      setLoading(false);
    } catch (error) {
      console.error('Error submitting feedback:', error);
      setError('Error submitting feedback. Please try again.');
      setLoading(false);
    }
  };

  return (
    <div className="summarization-tool">
      <h1>Text Summarization Tool</h1>
      <p className="tool-description">
        This tool uses AI to generate concise summaries of your text or documents.
      </p>

      {/* Error display */}
      {error && <div className="error-message">{error}</div>}

      {/* Loading state */}
      {loading && <div className="text-center my-4">
        <Loading text={processingStatus} size="medium" color="primary" />
      </div>}

      <div className="input-section">
        <h2>Input</h2>

        {/* Text input option */}
        <div className="text-input">
          <h3>Enter text to summarize</h3>
          <TextArea
            rows={10}
            value={text}
            onChange={handleTextChange}
            placeholder="Paste your text here..."
            disabled={loading}
          />
          <Button
            onClick={summarizeText}
            disabled={loading}
            variant="primary"
            size="medium"
            fullWidth
          >
            Summarize Text
          </Button>
        </div>

        <div className="section-divider">OR</div>

        {/* File upload option */}
        <div className="file-upload">
          <h3>Upload a document</h3>
          <FileUpload
            onFileSelect={handleFileUpload}
            accept=".txt,.pdf,.docx,.doc"
            maxSize={10}
            disabled={loading}
          />
          <div className="mt-4">
            <Button
              onClick={summarizeFile}
              disabled={loading || !file}
              variant="primary"
              size="medium"
              fullWidth
            >
              Upload & Summarize
            </Button>
          </div>
        </div>

        {/* Summarization options */}
        <div className="summary-options">
          <h3>Summarization Options</h3>
          <div className="option">
            <label>Max Length (characters): </label>
            <input 
              type="range" 
              name="maxLength" 
              min="50" 
              max="500" 
              value={summaryOptions.maxLength} 
              onChange={handleOptionsChange} 
              disabled={loading}
            />
            <span>{summaryOptions.maxLength}</span>
          </div>
          <div className="option">
            <label>Min Length (characters): </label>
            <input 
              type="range" 
              name="minLength" 
              min="20" 
              max="200" 
              value={summaryOptions.minLength} 
              onChange={handleOptionsChange} 
              disabled={loading}
            />
            <span>{summaryOptions.minLength}</span>
          </div>
        </div>

        {/* Model Selector */}
        <div className="model-selection mt-6">
          <ModelSelector
            selectedModel={selectedModel}
            onModelSelect={handleModelSelect}
            disabled={loading}
          />
        </div>

        {/* Advanced Options */}
        <AdvancedOptions
          options={advancedOptions}
          onChange={handleAdvancedOptionsChange}
          onReset={resetAdvancedOptions}
          disabled={loading}
        />
      </div>

      {/* Summary output */}
      {summary && (
        <div className="output-section">
          <h2>Summary</h2>
          <div className="summary-box">
            {summary}
          </div>

          {/* Feedback section */}
          <div className="feedback-section">
            <h3>How would you rate this summary?</h3>
            <div className="mb-4">
              <Rating
                rating={rating}
                setRating={setRating}
                disabled={loading}
                size="large"
              />
            </div>

            <TextArea
              placeholder="Additional feedback (optional)"
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
              rows={4}
              disabled={loading}
            />

            <Button
              onClick={submitFeedback}
              disabled={loading || rating === 0}
              variant="success"
              size="medium"
              className="mt-2"
            >
              Submit Feedback
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

export default TextSummarizationTool;
