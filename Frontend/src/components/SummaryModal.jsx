import React from 'react';

// A simple loading indicator
const LoadingSpinner = () => (
  <div className="text-center p-8">
    <p className="text-primary-accent text-lg">Generating AI Analysis, please wait...</p>
  </div>
);

export default function SummaryModal({ isOpen, isLoading, summaryData, onClose }) {
  // Don't render anything if the modal is closed
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 animate-fade-in">
      <div className="bg-surface-dark p-6 rounded-lg shadow-lg w-full max-w-3xl border border-border-dark flex flex-col max-h-[80vh]">
        <div className="flex-shrink-0">
          <h2 className="text-xl font-bold mb-4 text-primary-accent">Capture Session Analysis</h2>
        </div>

        <div className="flex-grow overflow-y-auto pr-2">
          {/* Conditional Rendering Logic */}
          {isLoading ? (
            <LoadingSpinner />
          ) : summaryData ? (
            <>
              {/* Part 1: The Summary Paragraph */}
              <h3 className="font-semibold text-lg mb-2 text-text-primary">Overall Summary</h3>
              <p className="text-text-secondary whitespace-pre-wrap leading-relaxed mb-6">
                {summaryData.summary}
              </p>

              {/* Part 2: The Breakdown Table */}
              <h3 className="font-semibold text-lg mb-3 text-text-primary">Protocol Breakdown</h3>
              <table className="w-full text-left table-auto">
                <thead className="bg-base-dark">
                  <tr>
                    <th className="p-2 w-1/6">Protocol</th>
                    <th className="p-2 w-2/6">Key Metrics</th>
                    <th className="p-2 w-3/6">Observations</th>
                  </tr>
                </thead>
                <tbody>
                  {summaryData.breakdown.map((item, index) => (
                    <tr key={index} className="border-t border-border-dark align-top">
                      <td className="p-2 font-bold text-primary-accent">{item.protocol}</td>
                      <td className="p-2 text-text-secondary">{item.keyMetrics}</td>
                      <td className="p-2 text-text-secondary">{item.observations}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          ) : (
             <p className="text-text-secondary">No summary data available or an error occurred.</p>
          )}
        </div>

        <div className="flex justify-end mt-6 flex-shrink-0">
          <button
            onClick={onClose}
            className="bg-primary-accent text-base-dark px-4 py-2 rounded font-bold hover:opacity-90 transition-opacity"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
