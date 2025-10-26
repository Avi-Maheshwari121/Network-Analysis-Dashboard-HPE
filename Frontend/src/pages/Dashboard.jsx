// Frontend/src/pages/Dashboard.jsx
import { useState, useEffect, useRef } from 'react';
import StatusBanner from "../components/StatusBanner";
import MetricCards from "../components/MetricCards";
import ControlPanel from "../components/ControlPanel";
import MetricChart from "../components/MetricChart";
import ProtocolPieChart from "../components/ProtocolPieChart";
import ProtocolBarChart from '../components/ProtocolBarChart';
import SummaryModal from '../components/SummaryModal';

export default function Dashboard({
  wsConnected,
  metrics, // This object now contains packets_per_second
  commandStatus,
  loading,
  error,
  sendCommand,
  interfaces,
  metricsHistory, // Global throughput history
  protocolDistribution,
  // Removed ipv4Metrics, ipv6Metrics as they are not needed here anymore
  // AI Summary props
  captureSummary,
  summaryStatus,
}) {
  const [isSummaryModalOpen, setIsSummaryModalOpen] = useState(false);

  const isUiLocked = loading && summaryStatus !== 'done';

// --- ADD THIS NEW, CORRECTED LOGIC ---

  const [captureDuration, setCaptureDuration] = useState(0);
  // useRef to store the exact start time, unaffected by re-renders.
  const startTimeRef = useRef(null);


  useEffect(() => {
    let intervalId = null;

    if (metrics?.status === 'running') {
      // Look for a start time in the browser's session storage.
      let startTime = sessionStorage.getItem('captureStartTime');

      // If one doesn't exist, this is a new capture. Create it.
      if (!startTime) {
        startTime = Date.now();
        sessionStorage.setItem('captureStartTime', startTime);
      }

      // Update the timer every second based on the stored start time.
      intervalId = setInterval(() => {
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        setCaptureDuration(elapsed >= 0 ? elapsed : 0);
      }, 1000);

    } else {
      // When capture stops, clear the start time from storage.
      sessionStorage.removeItem('captureStartTime');
    }

    // Stop the timer when the component updates or unmounts.
    return () => {
      clearInterval(intervalId);
    };
  }, [metrics]);
// ---------------------------------------------
  // totalPacketsPerSecond calculation removed

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

      {/* Row 1: Simplified Metric Cards - Pass the whole metrics object */}
      <MetricCards metrics={metrics} />

      {/* Row 2: Full Width Throughput Chart */}
      <div className="mt-6 h-72">
         <MetricChart
            title="Overall Throughput"
            unit=" Mbps"
            data={metricsHistory}
            lines={[
              { dataKey: "inbound", name: "Inbound", color: "#2DD4BF" },
              { dataKey: "outbound", name: "Outbound", color: "#3B82F6" }
            ]}
          />
      </div>

      {/* Row 3: Protocol Distribution Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
        <div className="lg:col-span-1">
            <ProtocolPieChart data={protocolDistribution} />
        </div>
        <div className="lg:col-span-2">
             <ProtocolBarChart data={protocolDistribution} />
        </div>
      </div>

      {/* AI Summary Modal */}
      <SummaryModal
        summaryData={captureSummary}
        isLoading={summaryStatus === 'loading'}
        isOpen={isSummaryModalOpen}
        onClose={() => setIsSummaryModalOpen(false)}
      />
    </div>
  );
}