import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import Loading from '../common/Loading';
import Button from '../common/Button';

/**
 * HistoryPanel component displays a list of past summarization tasks.
 */
const HistoryPanel = ({ fetchHistory }) => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const data = await fetchHistory();
        setHistory(data);
      } catch (err) {
        setError('Failed to load history. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    loadHistory();
  }, [fetchHistory]);

  if (loading) {
    return <Loading text="Loading history..." size="medium" color="primary" />;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="history-panel">
      <h2 className="text-lg font-semibold mb-4">Summarization History</h2>
      {history.length === 0 ? (
        <p className="text-gray-500">No history available.</p>
      ) : (
        <ul className="space-y-4">
          {history.map((item) => (
            <li key={item.id} className="p-4 bg-white shadow rounded-lg">
              <p className="text-sm text-gray-700 mb-2">
                <strong>Document ID:</strong> {item.documentId}
              </p>
              <p className="text-sm text-gray-700 mb-2">
                <strong>Summary:</strong> {item.summary}
              </p>
              <p className="text-sm text-gray-500">
                <strong>Date:</strong> {new Date(item.date).toLocaleString()}
              </p>
              <Button
                variant="outline"
                size="small"
                onClick={() => alert(`Viewing details for ${item.documentId}`)}
              >
                View Details
              </Button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

HistoryPanel.propTypes = {
  fetchHistory: PropTypes.func.isRequired,
};

export default HistoryPanel;

