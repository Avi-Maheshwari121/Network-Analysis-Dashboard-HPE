// Frontend/src/pages/Dashboard.jsx
import { useState } from 'react'; // Removed useMemo
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

  // totalPacketsPerSecond calculation removed

  return (
    <div>
      <StatusBanner connected={wsConnected} error={error} metrics={metrics} />
      <ControlPanel
        sendCommand={sendCommand}
        loading={loading}
        commandStatus={commandStatus}
        interfaces={interfaces}
        summaryStatus={summaryStatus}
        onShowSummary={() => setIsSummaryModalOpen(true)}
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
        summary={captureSummary}
        isOpen={isSummaryModalOpen}
        onClose={() => setIsSummaryModalOpen(false)}
      />
    </div>
  );
}