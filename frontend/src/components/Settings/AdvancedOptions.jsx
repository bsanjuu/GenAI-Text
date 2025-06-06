import React, { useState } from 'react';
import PropTypes from 'prop-types';
import Button from '../common/Button';

/**
 * AdvancedOptions component provides additional configuration options for text summarization
 */
const AdvancedOptions = ({
  options,
  onChange,
  disabled = false,
  onReset,
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    // Handle different input types
    const newValue = type === 'checkbox' ? checked : 
                    type === 'number' ? Number(value) : 
                    value;
    
    onChange({
      ...options,
      [name]: newValue,
    });
  };

  return (
    <div className="advanced-options border rounded-lg p-4 mt-4">
      <div 
        className="flex justify-between items-center cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <h3 className="text-lg font-medium">Advanced Options</h3>
        <button 
          className="text-gray-500 focus:outline-none"
          aria-label={isExpanded ? "Collapse advanced options" : "Expand advanced options"}
        >
          <svg 
            className={`w-5 h-5 transform transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24" 
            xmlns="http://www.w3.org/2000/svg"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      </div>
      
      {isExpanded && (
        <div className="mt-4 space-y-4">
          {/* Temperature setting */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Temperature: {options.temperature.toFixed(1)}
            </label>
            <input
              type="range"
              name="temperature"
              min="0"
              max="1"
              step="0.1"
              value={options.temperature}
              onChange={handleChange}
              disabled={disabled}
              className="w-full"
            />
            <p className="text-xs text-gray-500 mt-1">
              Lower values produce more focused summaries, higher values produce more creative ones.
            </p>
          </div>
          
          {/* Format selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Output Format
            </label>
            <select
              name="format"
              value={options.format}
              onChange={handleChange}
              disabled={disabled}
              className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="paragraph">Paragraph</option>
              <option value="bullets">Bullet Points</option>
              <option value="numbered">Numbered List</option>
            </select>
          </div>
          
          {/* Include keywords option */}
          <div className="flex items-center">
            <input
              type="checkbox"
              id="includeKeywords"
              name="includeKeywords"
              checked={options.includeKeywords}
              onChange={handleChange}
              disabled={disabled}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="includeKeywords" className="ml-2 block text-sm text-gray-700">
              Include key phrases in summary
            </label>
          </div>
          
          {/* Language selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Output Language
            </label>
            <select
              name="language"
              value={options.language}
              onChange={handleChange}
              disabled={disabled}
              className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="auto">Auto-detect</option>
              <option value="en">English</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
              <option value="de">German</option>
              <option value="zh">Chinese</option>
            </select>
          </div>
          
          <div className="flex justify-end">
            <Button
              variant="outline"
              size="small"
              onClick={onReset}
              disabled={disabled}
            >
              Reset to Defaults
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

AdvancedOptions.propTypes = {
  options: PropTypes.shape({
    temperature: PropTypes.number.isRequired,
    format: PropTypes.string.isRequired,
    includeKeywords: PropTypes.bool.isRequired,
    language: PropTypes.string.isRequired,
  }).isRequired,
  onChange: PropTypes.func.isRequired,
  disabled: PropTypes.bool,
  onReset: PropTypes.func.isRequired,
};

export default AdvancedOptions;