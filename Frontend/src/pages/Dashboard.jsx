// avi-maheshwari121/network-analysis-dashboard-hpe/Network-Analysis-Dashboard-HPE-d12cfd16410c6685dd2d171d8840126ca82c0967/Frontend/src/pages/Dashboard.jsx

import StatusBanner from "../components/StatusBanner";
import MetricCards from "../components/MetricCards";
import ControlPanel from "../components/ControlPanel";
import MetricChart from "../components/MetricChart";
import ProtocolPieChart from "../components/ProtocolPieChart";

export default function Dashboard({
  wsConnected,
  metrics,
  streamCount,
  commandStatus,
  loading,
  error,
  sendCommand,
  interfaces,
  metricsHistory,
  protocolDistribution,
}) {
  return (
    <div>
      <StatusBanner connected={wsConnected} error={error} metrics={metrics} />
      <ControlPanel
        sendCommand={sendCommand}
        loading={loading}
        commandStatus={commandStatus}
        interfaces={interfaces}
      />
      <MetricCards metrics={metrics} streamCount={streamCount} />
      
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
    </div>
  );
}