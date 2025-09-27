import React from 'react';

// A simple component for the status indicator dot
const StatusDot = ({ colorClass }) => (
  <span className="relative flex h-3 w-3">
    <span className={`animate-ping absolute h-full w-full rounded-full ${colorClass} opacity-75`}></span>
    <span className={`relative inline-flex rounded-full h-3 w-3 ${colorClass}`}></span>
  </span>
);

export default function StatusBanner({ connected, error, metrics }) {
  if (error) {
    return <div className="bg-red-600 text-white px-4 py-2 rounded mb-4">{error}</div>;
  }

  const captureStatus = metrics ? metrics.status : "stopped";
  const isRunning = captureStatus === 'running';

  return (
    <div className="flex items-center justify-between gap-4 font-semibold text-text-secondary mb-6">
      {/* System Connection Status (Left) */}
      <div className="flex items-center gap-2">
        <StatusDot colorClass={connected ? 'bg-green-500' : 'bg-red-500'} />
        <span>System Status: {connected ? "Operational" : "Disconnected"}</span>
      </div>

      {/* Capture Status (Right) */}
      <div className="flex items-center gap-2">
        <span>Capture Status: {captureStatus}</span>
        <StatusDot colorClass={isRunning ? 'bg-green-500' : 'bg-gray-500'} />
      </div>
    </div>
  );
}