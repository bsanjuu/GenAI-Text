import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import PropTypes from 'prop-types';

/**
 * Navigation component for the application
 */
const Navigation = ({ title = 'Text Summarization Tool' }) => {
  const location = useLocation();
  
  // Determine which link is active based on current path
  const isActive = (path) => {
    return location.pathname === path ? 'bg-blue-700' : '';
  };
  
  return (
    <nav className="bg-blue-600 text-white p-4">
      <div className="container mx-auto flex flex-col md:flex-row justify-between items-center">
        <div className="text-xl font-bold mb-4 md:mb-0">{title}</div>
        
        <div className="flex space-x-4">
          <Link 
            to="/" 
            className={`px-3 py-2 rounded hover:bg-blue-700 transition-colors ${isActive('/')}`}
          >
            Summarizer
          </Link>
          <Link 
            to="/history" 
            className={`px-3 py-2 rounded hover:bg-blue-700 transition-colors ${isActive('/history')}`}
          >
            History
          </Link>
          <Link 
            to="/stats" 
            className={`px-3 py-2 rounded hover:bg-blue-700 transition-colors ${isActive('/stats')}`}
          >
            Statistics
          </Link>
        </div>
      </div>
    </nav>
  );
};

Navigation.propTypes = {
  title: PropTypes.string,
};

export default Navigation;