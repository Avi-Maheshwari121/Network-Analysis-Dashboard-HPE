// Frontend/src/pages/SummaryHistoryPage.jsx
import React from 'react';
import { Clock } from 'lucide-react';

// A sub-component for a single summary card
const SummaryCard = ({ summary }) => {
  if (!summary) return null;

  const formattedTimestamp = new Date(summary.timestamp).toLocaleString();

  return (
    <div className="bg-surface-dark border border-border-dark rounded-lg shadow-md p-4 animate-fadeIn">
      <div className="flex justify-between items-center mb-2 pb-2 border-b border-border-dark">
        <h3 className="text-lg font-semibold text-primary-accent">AI Analysis</h3>
        <div className="flex items-center gap-2 text-sm text-text-secondary">
          <Clock size={16} />
          <span>{formattedTimestamp}</span>
        </div>
      </div>
      <p className="text-sm text-text-main whitespace-pre-wrap leading-relaxed">
        {summary.summary}
      </p>
    </div>
  );
};

// The main page component
export default function SummaryHistoryPage({ periodicSummaryHistory = [] }) {
  const hasHistory = periodicSummaryHistory.length > 0;

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-primary-accent mb-4">
        AI Summary History
      </h1>
      <p className="text-text-secondary mb-6">
        All periodic insights generated during the current capture session are logged here, with the newest appearing first.
      </p>

      {hasHistory ? (
        <div className="space-y-4">
          {/* Show newest first by reversing the array */}
          {[...periodicSummaryHistory].reverse().map((summary, index) => (
            <SummaryCard key={index} summary={summary} />
          ))}
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center h-64 bg-surface-dark border border-border-dark rounded-lg">
          <p className="text-lg text-text-secondary">No summaries have been generated yet.</p>
          <p className="text-sm text-text-secondary">Start a capture and wait for 60 seconds for insights to appear.</p>
        </div>
      )}
    </div>
  );
}