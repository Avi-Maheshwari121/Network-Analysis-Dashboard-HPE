import React, { useState, useEffect } from 'react';
import { Sparkles, LoaderCircle } from 'lucide-react'; // Import icons

export default function ControlPanel({ sendCommand, loading, commandStatus, interfaces, summaryStatus, onShowSummary }) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedInterface, setSelectedInterface] = useState(null);

  useEffect(() => {
    if (interfaces.length > 0 && !selectedInterface) {
      setSelectedInterface(interfaces[0]);
    }
  }, [interfaces, selectedInterface]);

  const Button = ({ onClick, children, className = '' }) => (
    <button
      className={`bg-primary-accent text-base-dark px-4 py-2 rounded font-bold shadow disabled:opacity-50 ${className}`}
      onClick={onClick}
      disabled={loading && summaryStatus !== 'loading'}
    >
      {children}
    </button>
  );

  // --- RESTORED Wi-Fi CHECK LOGIC ---
  const handleStartCapture = () => {
    if (!selectedInterface) {
      alert("Please select a network interface.");
      return;
    }

    // Frontend check: only allow interfaces with "wi-fi" in the name
    const isWifi = /(wi[-\s]?fi|wireless|wlan|802\.11|airport|en0|en1)/i.test(selectedInterface.name);

    if (isWifi) {
      sendCommand("start_capture", { interface: selectedInterface.id });
      setIsModalOpen(false);
    } else {
      alert("This feature is currently limited to Wi-Fi interfaces to prevent application instability. Please select a Wi-Fi adapter.");
    }
  };
  // --- END OF RESTORED LOGIC ---

  const AISummaryButton = () => {
    if (summaryStatus === 'idle') {
      return null;
    }

    if (summaryStatus === 'loading') {
      return (
        <div className="flex items-center gap-2 ml-4 px-3 py-2 rounded-lg bg-surface-dark text-text-secondary cursor-wait border border-border-dark">
          <LoaderCircle className="animate-spin" size={20} />
          <span>Generating Summary...</span>
        </div>
      );
    }

    if (summaryStatus === 'ready') {
      return (
        <button
          onClick={onShowSummary}
          className="flex items-center gap-2 ml-4 px-3 py-2 rounded-lg bg-primary-accent text-base-dark font-bold hover:opacity-90 transition-opacity"
        >
          <Sparkles size={20} />
          <span>View AI Summary</span>
        </button>
      );
    }
    
    return null;
  };

  return (
    <>
      <div className="flex items-center gap-4 mb-6">
        <Button onClick={() => setIsModalOpen(true)}>Start Capture</Button>
        <Button onClick={() => sendCommand("stop_capture")}>Stop Capture</Button>
        <AISummaryButton />
        <div className="flex-grow" />
        {commandStatus && (
          <div className={`px-4 py-2 rounded text-white ${commandStatus.success ? "bg-green-600" : "bg-red-600"}`}>
            {commandStatus.message}
          </div>
        )}
      </div>

      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
          <div className="bg-surface-dark p-6 rounded-lg shadow-lg w-full max-w-md border border-border-dark">
            <h2 className="text-xl font-bold mb-4">Select Network Interface</h2>
            {/* --- RESTORED NOTE --- */}
            <p className="text-sm text-text-secondary mb-4">
              Note: Live capture is only enabled for Wi-Fi interfaces.
            </p>
            {/* --- END OF RESTORED NOTE --- */}
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