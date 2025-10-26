import React from 'react';

// A simple component for the status indicator dot
const StatusDot = ({ colorClass }) => (
  <span className="relative flex h-3 w-3">
    <span className={`animate-ping absolute h-full w-full rounded-full ${colorClass} opacity-75`}></span>
    <span className={`relative inline-flex rounded-full h-3 w-3 ${colorClass}`}></span>
  </span>
);

// Formats seconds into a MM:SS string
const formatTime = (seconds) => {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  const paddedMinutes = String(minutes).padStart(2, '0');
  const paddedSeconds = String(remainingSeconds).padStart(2, '0');
  return `${paddedMinutes}:${paddedSeconds}`;
};

export default function StatusBanner({ connected, error, metrics, captureDuration }) {
  if (error) {
    return <div className="bg-red-600 text-white px-4 py-2 rounded mb-4">{error}</div>;
  }

  const captureStatus = metrics ? metrics.status : "stopped";
  const isRunning = captureStatus === 'running';

  return (
    <div className="flex items-start justify-between gap-4 font-semibold text-text-secondary mb-6">
      {/* System Connection Status (Left) */}
      <div className="flex items-center gap-2 pt-1">
        <StatusDot colorClass={connected ? 'bg-green-500' : 'bg-red-500'} />
        <span>System Status: {connected ? "Operational" : "Disconnected"}</span>
      </div>

      {/* Grouped Capture Status & Duration (Right) */}
      <div className="flex flex-col items-end gap-1">
        
        {/* Capture Status (Top) */}
        <div className="flex items-center gap-2">
          <span>Capture Status: {captureStatus}</span>
          <StatusDot colorClass={isRunning ? 'bg-green-500' : 'bg-gray-500'} />
        </div>

        {/* Capture Duration (Bottom) - Only shows when it has a value */}
        {captureDuration > 0 && (
          <div className="font-mono text-lg">
            <span>Duration: </span>
            <span className="font-bold text-primary-accent">{formatTime(captureDuration)}</span>
          </div>
        )}
      </div>
      
    </div>
  );
}