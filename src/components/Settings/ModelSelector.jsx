import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import Button from '../common/Button';
import Loading from '../common/Loading';

/**
 * ModelSelector component allows users to select different AI models for text summarization
 */
const ModelSelector = ({ 
  selectedModel, 
  onModelSelect, 
  disabled = false 
}) => {
  const [models, setModels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Fetch available models on component mount
  useEffect(() => {
    const fetchModels = async () => {
      try {
        // In a real application, this would be an API call
        // For now, we'll use mock data
        const mockModels = [
          { id: 'gpt-3.5-turbo', name: 'GPT-3.5 Turbo', description: 'Fast and efficient summarization' },
          { id: 'gpt-4', name: 'GPT-4', description: 'Most accurate summarization' },
          { id: 'bart-large-cnn', name: 'BART Large CNN', description: 'Optimized for news articles' },
          { id: 't5-base', name: 'T5 Base', description: 'Balanced performance and speed' },
        ];
        
        // Simulate API delay
        setTimeout(() => {
          setModels(mockModels);
          setLoading(false);
        }, 500);
      } catch (err) {
        console.error('Error fetching models:', err);
        setError('Failed to load available models. Please try again later.');
        setLoading(false);
      }
    };

    fetchModels();
  }, []);

  if (loading) {
    return <Loading text="Loading models..." size="small" color="primary" />;
  }

  if (error) {
    return <div className="text-red-500 text-sm">{error}</div>;
  }

  return (
    <div className="model-selector">
      <h3 className="text-lg font-medium mb-3">Select AI Model</h3>
      <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
        {models.map((model) => (
          <div 
            key={model.id}
            className={`
              border rounded-lg p-4 cursor-pointer transition-all
              ${selectedModel === model.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'}
              ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
            `}
            onClick={() => !disabled && onModelSelect(model.id)}
          >
            <h4 className="font-medium text-gray-800">{model.name}</h4>
            <p className="text-sm text-gray-600 mt-1">{model.description}</p>
          </div>
        ))}
      </div>
      
      {selectedModel && (
        <div className="mt-4 flex justify-end">
          <Button 
            variant="outline" 
            size="small"
            onClick={() => !disabled && onModelSelect(null)}
            disabled={disabled}
          >
            Reset Selection
          </Button>
        </div>
      )}
    </div>
  );
};

ModelSelector.propTypes = {
  selectedModel: PropTypes.string,
  onModelSelect: PropTypes.func.isRequired,
  disabled: PropTypes.bool,
};

export default ModelSelector;