import StatusBanner from "../components/StatusBanner";
import MetricCards from "../components/MetricCards";
import ControlPanel from "../components/ControlPanel";
import MetricChart from "../components/MetricChart"; // Import the new chart component

export default function Dashboard({
  wsConnected,
  metrics,
  streamCount,
  commandStatus,
  loading,
  error,
  sendCommand,
  interfaces,
  metricsHistory, // Receive metrics history
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
      
      {/* New section for charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <MetricChart
          title="Throughput"
          unit=" Mbps"
          data={metricsHistory}
          lines={[
            { dataKey: "inbound", name: "Inbound", color: "#2DD4BF" },
            { dataKey: "outbound", name: "Outbound", color: "#3B82F6" }
          ]}
        />
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
  );
}