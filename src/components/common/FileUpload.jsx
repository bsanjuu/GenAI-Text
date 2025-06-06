import React, { useRef, useState } from 'react';
import PropTypes from 'prop-types';
import Button from './Button';

/**
 * File upload component with drag and drop functionality
 */
const FileUpload = ({
  onFileSelect,
  accept = '.txt,.pdf,.docx,.doc',
  maxSize = 10, // in MB
  label = 'Upload Document',
  multiple = false,
  disabled = false,
}) => {
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState('');
  const [selectedFiles, setSelectedFiles] = useState([]);
  const inputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();

    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const validateFiles = (files) => {
    const validFiles = [];
    const invalidFiles = [];

    Array.from(files).forEach(file => {
      // Check file size
      if (file.size > maxSize * 1024 * 1024) {
        invalidFiles.push(`${file.name} (exceeds ${maxSize}MB size limit)`);
        return;
      }

      // Check file type
      const fileExtension = `.${file.name.split('.').pop().toLowerCase()}`;
      const acceptedTypes = accept.split(',');

      if (!acceptedTypes.some(type => {
        // Handle wildcards like application/pdf or .pdf
        if (type.includes('*')) {
          const mimePrefix = type.split('*')[0];
          return file.type.startsWith(mimePrefix);
        }
        return type === fileExtension || type === file.type;
      })) {
        invalidFiles.push(`${file.name} (invalid file type)`);
        return;
      }

      validFiles.push(file);
    });

    if (invalidFiles.length > 0) {
      setError(`Cannot upload: ${invalidFiles.join(', ')}`);
      return false;
    }

    setError('');
    return validFiles;
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const files = multiple ? e.dataTransfer.files : [e.dataTransfer.files[0]];
      const validFiles = validateFiles(files);

      if (validFiles) {
        setSelectedFiles(multiple ? validFiles : [validFiles[0]]);
        onFileSelect(multiple ? validFiles : validFiles[0]);
      }
    }
  };

  const handleChange = (e) => {
    e.preventDefault();

    if (e.target.files && e.target.files.length > 0) {
      const files = multiple ? e.target.files : [e.target.files[0]];
      const validFiles = validateFiles(files);

      if (validFiles) {
        setSelectedFiles(multiple ? validFiles : [validFiles[0]]);
        onFileSelect(multiple ? validFiles : validFiles[0]);
      }
    }
  };

  const handleClick = () => {
    inputRef.current.click();
  };

  const removeFile = (fileToRemove) => {
    const updatedFiles = selectedFiles.filter(file => file !== fileToRemove);
    setSelectedFiles(updatedFiles);
    onFileSelect(multiple ? updatedFiles : updatedFiles[0] || null);
  };

  return (
    <div className="w-full">
      <div
        className={`
          border-2 border-dashed rounded-lg p-4 text-center
          ${dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'} 
          ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:bg-gray-50'}
        `}
        onDragEnter={disabled ? null : handleDrag}
        onDragOver={disabled ? null : handleDrag}
        onDragLeave={disabled ? null : handleDrag}
        onDrop={disabled ? null : handleDrop}
        onClick={disabled ? null : handleClick}
      >
        <input
          ref={inputRef}
          type="file"
          multiple={multiple}
          onChange={handleChange}
          accept={accept}
          className="hidden"
          disabled={disabled}
        />

        <div className="flex flex-col items-center justify-center py-5">
          <svg
            className="w-10 h-10 text-gray-400 mb-3"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>

          <p className="mb-2 text-sm text-gray-500">
            <span className="font-semibold">Click to upload</span> or drag and drop
          </p>
          <p className="text-xs text-gray-500">
            {accept.split(',').join(', ')} (Max: {maxSize}MB)
          </p>
        </div>
      </div>

      {error && (
        <p className="mt-2 text-sm text-red-600">{error}</p>
      )}

      {selectedFiles.length > 0 && (
        <div className="mt-3">
          <p className="text-sm font-medium text-gray-700">Selected Files:</p>
          <ul className="mt-1 space-y-1">
            {selectedFiles.map((file, index) => (
              <li key={index} className="flex items-center justify-between text-sm text-gray-500 p-2 bg-gray-50 rounded">
                <span className="truncate max-w-xs">{file.name}</span>
                <Button
                  variant="danger"
                  size="small"
                  onClick={(e) => {
                    e.stopPropagation();
                    removeFile(file);
                  }}
                  disabled={disabled}
                >
                  Remove
                </Button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

FileUpload.propTypes = {
  onFileSelect: PropTypes.func.isRequired,
  accept: PropTypes.string,
  maxSize: PropTypes.number,
  label: PropTypes.string,
  multiple: PropTypes.bool,
  disabled: PropTypes.bool,
};

export default FileUpload;
