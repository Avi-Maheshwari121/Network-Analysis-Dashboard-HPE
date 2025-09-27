import React, { useState, useEffect } from 'react';

export default function ControlPanel({ sendCommand, loading, commandStatus, interfaces }) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedInterface, setSelectedInterface] = useState(null);

  useEffect(() => {
    // Set a default selection when interfaces become available
    if (interfaces.length > 0 && !selectedInterface) {
      setSelectedInterface(interfaces[0]);
    }
  }, [interfaces, selectedInterface]);

  const Button = ({ onClick, children, className = '' }) => (
    <button
      className={`bg-primary-accent text-base-dark px-4 py-2 rounded font-bold shadow disabled:opacity-50 ${className}`}
      onClick={onClick}
      disabled={loading}
    >
      {children}
    </button>
  );

  const handleStartCapture = () => {
    if (!selectedInterface) {
      alert("Please select a network interface.");
      return;
    }

    // Frontend check: only allow interfaces with "wi-fi" in the name
    const isWifi = /wi-fi/i.test(selectedInterface.name);

    if (isWifi) {
      sendCommand("start_capture", { interface: selectedInterface.id });
      setIsModalOpen(false);
    } else {
      alert("This feature is currently limited to Wi-Fi interfaces to prevent application instability. Please select a Wi-Fi adapter.");
    }
  };

  return (
    <>
      <div className="flex items-center gap-4 mb-6">
        <Button onClick={() => setIsModalOpen(true)}>Start Capture</Button>
        <Button onClick={() => sendCommand("stop_capture")}>Stop Capture</Button>
        {commandStatus && (
          <div className={`ml-auto px-4 py-2 rounded text-white ${commandStatus.success ? "bg-green-600" : "bg-red-600"}`}>
            {commandStatus.message || `Status: ${commandStatus.metrics.status}`}
          </div>
        )}
      </div>

      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-surface-dark p-6 rounded-lg shadow-lg w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Select Network Interface</h2>
            <p className="text-sm text-text-secondary mb-4">
              Note: Live capture is only enabled for Wi-Fi interfaces.
            </p>
            <select
              value={selectedInterface?.id || ''}
              onChange={(e) => {
                const iface = interfaces.find(i => i.id === e.target.value);
                setSelectedInterface(iface);
              }}
              className="w-full bg-base-dark border border-border-dark rounded px-3 py-2 text-text-main mb-4"
            >
              {interfaces.map((iface) => (
                <option key={iface.id} value={iface.id}>
                  {iface.name}
                </option>
              ))}
            </select>
            <div className="flex justify-end gap-4">
              <button onClick={() => setIsModalOpen(false)} className="bg-gray-700 text-white px-4 py-2 rounded font-bold">
                Cancel
              </button>
              <Button onClick={handleStartCapture}>
                Start
              </Button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}