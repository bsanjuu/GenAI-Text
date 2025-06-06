import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import Loading from '../common/Loading';

/**
 * StatsDashboard component displays usage statistics and metrics
 */
const StatsDashboard = ({ fetchStats }) => {
  const [stats, setStats] = useState(null);
  const [timeRange, setTimeRange] = useState('week');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadStats = async () => {
      setLoading(true);
      setError('');
      
      try {
        // In a real application, this would pass the timeRange to the API
        const data = await fetchStats(timeRange);
        setStats(data);
      } catch (err) {
        console.error('Error loading stats:', err);
        setError('Failed to load statistics. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    loadStats();
  }, [fetchStats, timeRange]);

  const handleTimeRangeChange = (range) => {
    setTimeRange(range);
  };

  if (loading) {
    return <Loading text="Loading statistics..." size="medium" color="primary" />;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  if (!stats) {
    return <div className="text-gray-500">No statistics available.</div>;
  }

  return (
    <div className="stats-dashboard">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold">Usage Statistics</h2>
        <div className="time-range-selector flex space-x-2">
          <button
            className={`px-3 py-1 text-sm rounded-md ${timeRange === 'day' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'}`}
            onClick={() => handleTimeRangeChange('day')}
          >
            Day
          </button>
          <button
            className={`px-3 py-1 text-sm rounded-md ${timeRange === 'week' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'}`}
            onClick={() => handleTimeRangeChange('week')}
          >
            Week
          </button>
          <button
            className={`px-3 py-1 text-sm rounded-md ${timeRange === 'month' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'}`}
            onClick={() => handleTimeRangeChange('month')}
          >
            Month
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {/* Summary Count Card */}
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="text-sm font-medium text-gray-500">Total Summaries</h3>
          <p className="text-2xl font-bold mt-1">{stats.totalSummaries}</p>
          <div className={`text-sm mt-2 ${stats.summaryChange >= 0 ? 'text-green-500' : 'text-red-500'}`}>
            {stats.summaryChange >= 0 ? '↑' : '↓'} {Math.abs(stats.summaryChange)}% from previous {timeRange}
          </div>
        </div>

        {/* Average Length Card */}
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="text-sm font-medium text-gray-500">Avg. Summary Length</h3>
          <p className="text-2xl font-bold mt-1">{stats.avgLength} chars</p>
          <div className="text-sm mt-2 text-gray-500">
            From {stats.totalDocuments} documents
          </div>
        </div>

        {/* Average Rating Card */}
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="text-sm font-medium text-gray-500">Avg. Rating</h3>
          <p className="text-2xl font-bold mt-1">{stats.avgRating.toFixed(1)}/5</p>
          <div className="text-sm mt-2 text-gray-500">
            Based on {stats.totalRatings} ratings
          </div>
        </div>
      </div>

      {/* Model Usage Section */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <h3 className="text-lg font-medium mb-4">Model Usage</h3>
        <div className="space-y-4">
          {stats.modelUsage.map((model) => (
            <div key={model.id} className="model-usage">
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium">{model.name}</span>
                <span className="text-sm text-gray-500">{model.percentage}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div 
                  className="bg-blue-600 h-2.5 rounded-full" 
                  style={{ width: `${model.percentage}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="text-lg font-medium mb-4">Recent Activity</h3>
        {stats.recentActivity.length === 0 ? (
          <p className="text-gray-500">No recent activity.</p>
        ) : (
          <ul className="space-y-3">
            {stats.recentActivity.map((activity) => (
              <li key={activity.id} className="border-b pb-3 last:border-b-0 last:pb-0">
                <p className="text-sm font-medium">{activity.action}</p>
                <p className="text-xs text-gray-500">{new Date(activity.timestamp).toLocaleString()}</p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

StatsDashboard.propTypes = {
  fetchStats: PropTypes.func.isRequired,
};

// Mock function for demonstration
StatsDashboard.defaultProps = {
  fetchStats: async (timeRange) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    return {
      totalSummaries: 128,
      summaryChange: 12.5,
      avgLength: 320,
      totalDocuments: 87,
      avgRating: 4.2,
      totalRatings: 64,
      modelUsage: [
        { id: 'gpt-3.5-turbo', name: 'GPT-3.5 Turbo', percentage: 45 },
        { id: 'gpt-4', name: 'GPT-4', percentage: 30 },
        { id: 'bart-large-cnn', name: 'BART Large CNN', percentage: 15 },
        { id: 't5-base', name: 'T5 Base', percentage: 10 },
      ],
      recentActivity: [
        { id: '1', action: 'Summarized document "Q3 Financial Report.pdf"', timestamp: new Date().toISOString() },
        { id: '2', action: 'Changed default model to GPT-4', timestamp: new Date(Date.now() - 3600000).toISOString() },
        { id: '3', action: 'Rated summary 5/5 stars', timestamp: new Date(Date.now() - 7200000).toISOString() },
      ],
    };
  },
};

export default StatsDashboard;