import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import HistoryPanel from './HistoryPanel';

describe('HistoryPanel', () => {
  const mockFetchHistory = jest.fn();

  beforeEach(() => {
    mockFetchHistory.mockReset();
  });

  it('renders loading state initially', () => {
    mockFetchHistory.mockReturnValue(new Promise(() => {})); // Simulate loading
    render(<HistoryPanel fetchHistory={mockFetchHistory} />);

    expect(screen.getByText(/loading history.../i)).toBeInTheDocument();
  });

  it('renders error message on fetch failure', async () => {
    mockFetchHistory.mockRejectedValue(new Error('Failed to fetch'));
    render(<HistoryPanel fetchHistory={mockFetchHistory} />);

    await waitFor(() => {
      expect(screen.getByText(/failed to load history/i)).toBeInTheDocument();
    });
  });

  it('renders history items on successful fetch', async () => {
    const mockData = [
      { id: '1', documentId: 'doc123', summary: 'Sample summary', date: new Date().toISOString() },
      { id: '2', documentId: 'doc456', summary: 'Another summary', date: new Date().toISOString() },
    ];
    mockFetchHistory.mockResolvedValue(mockData);

    render(<HistoryPanel fetchHistory={mockFetchHistory} />);

    await waitFor(() => {
      expect(screen.getByText(/doc123/i)).toBeInTheDocument();
      expect(screen.getByText(/sample summary/i)).toBeInTheDocument();
      expect(screen.getByText(/doc456/i)).toBeInTheDocument();
      expect(screen.getByText(/another summary/i)).toBeInTheDocument();
    });
  });

  it('handles view details button click', async () => {
    const mockData = [
      { id: '1', documentId: 'doc123', summary: 'Sample summary', date: new Date().toISOString() },
    ];
    mockFetchHistory.mockResolvedValue(mockData);

    render(<HistoryPanel fetchHistory={mockFetchHistory} />);

    await waitFor(() => {
      expect(screen.getByText(/doc123/i)).toBeInTheDocument();
    });

    const viewDetailsButton = screen.getByRole('button', { name: /view details/i });
    userEvent.click(viewDetailsButton);

    expect(window.alert).toHaveBeenCalledWith('Viewing details for doc123');
  });
});
