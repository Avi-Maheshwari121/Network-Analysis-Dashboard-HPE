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
  //Get topTalkers from props (passed down from App.jsx via useWebSocket)
  topTalkers,
}) {
  const [isSummaryModalOpen, setIsSummaryModalOpen] = useState(false);
  const [captureDuration, setCaptureDuration] = useState(0);
  const startTimeRef = useRef(null);

  useEffect(() => {
     let intervalId = null;

    if (metrics?.status === 'running') {
      sessionStorage.removeItem('finalCaptureDuration');
      let startTime = sessionStorage.getItem('captureStartTime');
      if (!startTime) {
        startTime = Date.now();
        sessionStorage.setItem('captureStartTime', startTime);
      }

      intervalId = setInterval(() => {
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        setCaptureDuration(elapsed >= 0 ? elapsed : 0);
      }, 1000);

    } else {
      const finalDuration = sessionStorage.getItem('finalCaptureDuration');
      if (finalDuration) {
        setCaptureDuration(parseInt(finalDuration, 10));
      } else {
         if (captureDuration > 0) { // Only save if there was a duration tracked
             sessionStorage.setItem('finalCaptureDuration', captureDuration);
         }
      }
      sessionStorage.removeItem('captureStartTime');
    }

    return () => {
      clearInterval(intervalId);
    };
  }, [metrics?.status]); // Depend only on status change

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

      {/* Row 1: Simplified Metric Cards */}
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

      {/* *** NEW: Row 4: Top Talkers Sankey Diagram *** */}
      <TopTalkersSankey topTalkers={topTalkers} />

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