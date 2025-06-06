import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './index.css';
import App from './App';
import Layout from './components/Layout';
import HistoryPanel from './components/Dashboard/HistoryPanel';
import StatsDashboard from './components/Dashboard/StatsDashboard';

const fetchHistoryMock = async () => {
  // Mock data for history
  return [
    {
      id: '1',
      documentId: 'doc123',
      summary: 'This is a sample summary.',
      date: new Date().toISOString(),
    },
    {
      id: '2',
      documentId: 'doc456',
      summary: 'Another example summary.',
      date: new Date().toISOString(),
    },
  ];
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<App />} />
          <Route path="/history" element={<HistoryPanel fetchHistory={fetchHistoryMock} />} />
          <Route path="/stats" element={<StatsDashboard />} />
        </Route>
      </Routes>
    </Router>
  </React.StrictMode>
);
