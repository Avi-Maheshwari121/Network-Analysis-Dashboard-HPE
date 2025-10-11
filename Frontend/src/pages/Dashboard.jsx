// Dashboard.jsx

import { useState } from 'react';
import StatusBanner from "../components/StatusBanner";
import MetricCards from "../components/MetricCards";
import ControlPanel from "../components/ControlPanel";
import MetricChart from "../components/MetricChart";
import ProtocolPieChart from "../components/ProtocolPieChart";
import SummaryModal from '../components/SummaryModal'; // Import the new modal

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
  // --- NEW: Receive summary props ---
  captureSummary,
  summaryStatus,
  // --- End of NEW section ---
}) {
  // --- NEW: State to control modal visibility ---
  const [isSummaryModalOpen, setIsSummaryModalOpen] = useState(false);
  // --- End of NEW section ---

  return (
    <div>
      <StatusBanner connected={wsConnected} error={error} metrics={metrics} />
      <ControlPanel
        sendCommand={sendCommand}
        loading={loading}
        commandStatus={commandStatus}
        interfaces={interfaces}
        // --- NEW: Pass summary props and handler to ControlPanel ---
        summaryStatus={summaryStatus}
        onShowSummary={() => setIsSummaryModalOpen(true)}
        // --- End of NEW section ---
      />
      <MetricCards metrics={metrics} />
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
        <div className="lg:col-span-2">
            <MetricChart
              title="Throughput"
              unit=" Mbps"
              data={metricsHistory}
              lines={[
                { dataKey: "inbound", name: "Inbound", color: "#2DD4BF" },
                { dataKey: "outbound", name: "Outbound", color: "#3B82F6" }
              ]}
            />
        </div>
        <ProtocolPieChart data={protocolDistribution} />
        <div className="lg:col-span-3">
            <MetricChart
              title="Latency & Jitter"
              unit=" ms"
              data={metricsHistory}
              lines={[
                { dataKey: "latency", name: "Latency", color: "#F472B6" },
                { dataKey: "jitter", name: "Jitter", color: "#FBBF24" }
              ]}
            />
        </div>
      </div>
      
      {/* --- NEW: Render the modal and control it with state --- */}
      <SummaryModal 
        summary={captureSummary} 
        isOpen={isSummaryModalOpen}
        onClose={() => setIsSummaryModalOpen(false)} 
      />
      {/* --- End of NEW section --- */}
    </div>
  );
}