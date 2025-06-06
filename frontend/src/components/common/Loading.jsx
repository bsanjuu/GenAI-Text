import React from 'react';
import PropTypes from 'prop-types';

/**
 * Loading spinner component with customizable size and color
 */
const Loading = ({
  size = 'medium',
  color = 'primary',
  text = 'Loading...',
  fullScreen = false,
}) => {
  // Size classes for the spinner
  const sizeClasses = {
    small: 'w-4 h-4 border-2',
    medium: 'w-8 h-8 border-3',
    large: 'w-12 h-12 border-4',
  };

  // Color classes for the spinner
  const colorClasses = {
    primary: 'border-blue-500',
    secondary: 'border-gray-500',
    white: 'border-white',
  };

  // Text size classes
  const textSizeClasses = {
    small: 'text-xs',
    medium: 'text-sm',
    large: 'text-base',
  };

  const spinnerClasses = `
    inline-block rounded-full 
    border-t-transparent animate-spin
    ${sizeClasses[size]} 
    ${colorClasses[color]}
  `;

  // For full screen loading overlay
  if (fullScreen) {
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
        <div className="bg-white p-5 rounded-lg flex flex-col items-center shadow-xl">
          <div className={spinnerClasses}></div>
          {text && <p className={`mt-3 font-medium text-gray-700 ${textSizeClasses[size]}`}>{text}</p>}
        </div>
      </div>
    );
  }

  // For inline loading spinner
  return (
    <div className="flex items-center">
      <div className={spinnerClasses}></div>
      {text && <span className={`ml-2 text-gray-700 ${textSizeClasses[size]}`}>{text}</span>}
    </div>
  );
};

Loading.propTypes = {
  size: PropTypes.oneOf(['small', 'medium', 'large']),
  color: PropTypes.oneOf(['primary', 'secondary', 'white']),
  text: PropTypes.string,
  fullScreen: PropTypes.bool,
};

export default Loading;
