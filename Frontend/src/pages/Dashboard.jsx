// Frontend/src/pages/Dashboard.jsx
import { useState, useEffect, useRef } from 'react';
import StatusBanner from "../components/StatusBanner";
import MetricCards from "../components/MetricCards";
import ControlPanel from "../components/ControlPanel";
import MetricChart from "../components/MetricChart";
import ProtocolPieChart from "../components/ProtocolPieChart";
import ProtocolBarChart from '../components/ProtocolBarChart';
import SummaryModal from '../components/SummaryModal';
import TopTalkersSankey from '../components/TopTalkersSankey';

export default function Dashboard({
  wsConnected,
  metrics,
  commandStatus,
  loading,
  error,
  sendCommand,
  interfaces,
  metricsHistory,
  protocolDistribution,
  captureSummary,
  summaryStatus,
  topTalkers,
}) {
  const [isSummaryModalOpen, setIsSummaryModalOpen] = useState(false);
  const [captureDuration, setCaptureDuration] = useState(0);
  const intervalRef = useRef(null);

  // ... (useEffect and helper functions for timer remain identical) ...
  // Check sessionStorage only on initial mount to handle refresh persistence
  useEffect(() => {
    const storedStartTime = sessionStorage.getItem('captureStartTime');
    const backendStatus = metrics?.status; // Get status directly from props on mount

    if (backendStatus === 'running' && storedStartTime) {
      // If backend is running AND we have a stored start time (persisted refresh)
      const elapsedOnLoad = Math.floor((Date.now() - parseInt(storedStartTime, 10)) / 1000);
      setCaptureDuration(elapsedOnLoad >= 0 ? elapsedOnLoad : 0);
      console.log("Detected running status and start time on mount. Resuming timer.");
      startInterval(parseInt(storedStartTime, 10));
    } else {
      // If not running or no stored time, ensure timer is 0
      setCaptureDuration(0);
      sessionStorage.removeItem('captureStartTime'); // Clean up just in case
      console.log("No running status or start time on mount. Setting timer to 0.");
    }

    return () => {
      stopInterval();
      console.log("Dashboard component unmounted, interval cleared.");
    };
  }, []); // Run only once on initial mount/refresh

  // Helper function to start the interval
  const startInterval = (startTime) => {
    stopInterval(); // Clear existing interval first
    intervalRef.current = setInterval(() => {
      const elapsed = Math.floor((Date.now() - startTime) / 1000);
      setCaptureDuration(elapsed >= 0 ? elapsed : 0);
    }, 1000);
    console.log("Timer interval started.");
  };

  // Helper function to stop the interval
  const stopInterval = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
      console.log("Timer interval stopped.");
    }
  };

  // Effect to manage the timer based on backend status changes
  useEffect(() => {
    if (metrics?.status === 'running') {
      let startTime = sessionStorage.getItem('captureStartTime');
      if (!startTime) {
        // "Start Capture" was just clicked
        startTime = Date.now();
        sessionStorage.setItem('captureStartTime', startTime);
        setCaptureDuration(0); // Start from 0 when clicking Start
        console.log("Starting capture. Set start time:", startTime);
        startInterval(startTime);
      } else {
        // Resuming view while already running
        if (!intervalRef.current) {
             console.log("Status running, start time exists, ensuring interval is running.");
             startInterval(parseInt(startTime, 10));
        }
      }
    } else { // Status is 'stopped'
      stopInterval();
      // <<< REMOVED: setCaptureDuration(0); >>>  // Don't reset duration on stop
      sessionStorage.removeItem('captureStartTime'); // Clean up start time
      console.log("Capture stopped. Interval stopped, start time removed.");
      // The captureDuration state retains its last value
    }

    return () => {
      // Stop interval on cleanup (e.g., status change away from running)
      stopInterval();
    };
  }, [metrics?.status]); // Re-run when backend status changes


  return (
    <div>
      <StatusBanner connected={wsConnected} error={error} metrics={metrics} captureDuration={captureDuration} />
      <ControlPanel
        sendCommand={sendCommand}
        loading={loading}
        commandStatus={commandStatus}
        interfaces={interfaces}
        summaryStatus={summaryStatus}
        onShowSummary={() => setIsSummaryModalOpen(true)}
        captureDuration={captureDuration}
      />


      <MetricCards metrics={metrics} />
      
      {/* Overall Throughput and Packets Per Second - Side by Side */}
      <div className="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="h-72">
          <MetricChart
            title="Overall Throughput"
            // *** CHANGED: Pass "bps" to trigger dynamic scaling ***
            unit="bps"
            data={metricsHistory}
            lines={[
              { dataKey: "inbound", name: "Inbound", color: "#2DD4BF" },
              { dataKey: "outbound", name: "Outbound", color: "#3B82F6" }
            ]}
          />
        </div>
        <div className="h-72">
          <MetricChart
            title="Packets Per Second"
            // *** CHANGED: Pass "pps" (no space) ***
            unit="pps"
            data={metricsHistory}
            lines={[
              // This dataKey MUST be added to useWebsocket.js
              { dataKey: "packets_per_sec", name: "Packets/sec", color: "#8B5CF6" }
            ]}
          />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
        <div className="lg:col-span-1">
            <ProtocolPieChart data={protocolDistribution} />
        </div>
        <div className="lg:col-span-2">
             <ProtocolBarChart data={protocolDistribution} />
        </div>
      </div>
      <TopTalkersSankey topTalkers={topTalkers} />
      <SummaryModal
        summaryData={captureSummary}
        isLoading={summaryStatus === 'loading'}
        isOpen={isSummaryModalOpen}
        onClose={() => setIsSummaryModalOpen(false)}
      />
    </div>
  );
}