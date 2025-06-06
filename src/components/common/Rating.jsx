import React from 'react';
import PropTypes from 'prop-types';

/**
 * Star rating component for collecting user feedback
 */
const Rating = ({
  rating,
  setRating,
  maxRating = 5,
  size = 'medium',
  disabled = false,
  label = 'Rate this summary:',
  required = false,
}) => {
  // Star sizes
  const sizes = {
    small: 'w-4 h-4',
    medium: 'w-6 h-6',
    large: 'w-8 h-8',
  };

  // Text sizes
  const textSizes = {
    small: 'text-sm',
    medium: 'text-base',
    large: 'text-lg',
  };

  // Generate an array of numbers from 1 to maxRating
  const stars = Array.from({ length: maxRating }, (_, i) => i + 1);

  return (
    <div className="flex flex-col">
      {label && (
        <label className={`mb-2 font-medium text-gray-700 ${textSizes[size]}`}>
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}

      <div className="flex space-x-1">
        {stars.map((star) => (
          <button
            key={star}
            type="button"
            onClick={() => !disabled && setRating(star)}
            onMouseEnter={() => !disabled && setRating(star)}
            className={`
              focus:outline-none transition-colors
              ${disabled ? 'cursor-not-allowed' : 'cursor-pointer'}
            `}
            aria-label={`Rate ${star} out of ${maxRating}`}
            disabled={disabled}
          >
            <svg
              className={`
                ${sizes[size]}
                ${star <= rating 
                  ? 'text-yellow-400' 
                  : 'text-gray-300'}
                transition-colors duration-150
                ${!disabled && star > rating ? 'hover:text-yellow-200' : ''}
              `}
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </button>
        ))}

        {rating > 0 && (
          <span className={`ml-2 text-gray-700 ${textSizes[size]}`}>
            {rating}/{maxRating}
          </span>
        )}
      </div>
    </div>
  );
};

Rating.propTypes = {
  rating: PropTypes.number.isRequired,
  setRating: PropTypes.func.isRequired,
  maxRating: PropTypes.number,
  size: PropTypes.oneOf(['small', 'medium', 'large']),
  disabled: PropTypes.bool,
  label: PropTypes.string,
  required: PropTypes.bool,
};

export default Rating;
