// Frontend/src/components/ProtocolMetricsDisplay.jsx
import React from 'react';
import MetricChart from './MetricChart'; // Import the chart component

// Simple StatCard component for reuse - Updated for uniform height
const StatCard = ({ title, value, unit = '', subValue = '' }) => (
  // Use flex column layout to control vertical alignment and height
  <div className="bg-base-dark p-4 rounded-lg border border-border-dark text-center flex flex-col justify-between">
    {/* Top Part: Title */}
    <div>
      <p className="text-sm font-semibold text-text-secondary uppercase mb-1 whitespace-nowrap">{title}</p>
    </div>

    {/* Middle Part: Main Value */}
    <div className="my-2">
      <p className="text-2xl font-bold text-text-main">
        {value} {unit && <span className="text-base">{unit}</span>}
      </p>
    </div>

    {/* Bottom Part: SubValue (Ensure this part always takes up space) */}
    <div className="h-4"> {/* Reserve space for subValue */}
      {subValue ? (
        <p className="text-xs text-text-secondary mt-1">{subValue}</p>
      ) : (
        // Render a non-breaking space if no subValue to maintain height
        <p className="text-xs text-text-secondary mt-1">&nbsp;</p>
      )}
    </div>
  </div>
);


export default function ProtocolMetricsDisplay({
    protocolName,
    metricsData,
    detailsToShow = [],
    throughputHistory = [], // Accept throughput history prop
    latencyHistory = [],    // Accept latency history prop
    jitterHistory = [],     // Accept jitter history prop
    throughputKPIs = {}     // Accept KPIs prop
}) {
  // Show loading state if data hasn't arrived yet
  if (!metricsData) {
    return (
      <div className="bg-surface-dark p-6 rounded-xl border border-border-dark shadow-md animate-pulse">
        <h3 className="text-xl font-bold text-primary-accent mb-4 h-6 bg-gray-700 rounded w-1/3"></h3>
        {/* Simplified loading placeholder for cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="h-24 bg-gray-700 rounded"></div>
            <div className="h-24 bg-gray-700 rounded"></div>
            <div className="h-24 bg-gray-700 rounded"></div>
            <div className="h-24 bg-gray-700 rounded"></div>
        </div>
         {/* Placeholder for graph area */}
        <div className="mt-6 h-72 bg-gray-700 rounded"></div>
      </div>
    );
  }

  // --- Helper to format throughput KPIs as simple text ---
  const formatKpiText = (label, inValue, outValue, unit) => (
      <span>
          <span className="font-semibold text-text-secondary">{label}: </span>
          <span className="font-bold text-text-main">{Number(inValue || 0).toFixed(2)} / {Number(outValue || 0).toFixed(2)}</span>
          <span className="text-sm text-text-secondary"> {unit}</span>
      </span>
  );

  // --- Dynamically build the list of CORE cards ---
  const coreCards = [];

  if (detailsToShow.includes('latency') && metricsData.latency !== undefined) {
    coreCards.push(<StatCard key="latency" title="Avg RTT Latency" value={(metricsData.latency || 0).toFixed(1)} unit="ms" />);
  }
  if (detailsToShow.includes('jitter') && metricsData.jitter !== undefined) {
      coreCards.push(<StatCard key="jitter" title="RTP Jitter" value={(metricsData.jitter || 0).toFixed(1)} unit="ms" />);
  }
  if (detailsToShow.includes('packet_loss_percentage') && metricsData.packet_loss_percentage !== undefined) {
      const lossCount = metricsData.packet_loss || 0;
      coreCards.push(<StatCard key="loss-percent" title="Packet Loss" value={`${(metricsData.packet_loss_percentage || 0).toFixed(2)} %`} subValue={`(${lossCount} pkts)`} />);
  } else if (detailsToShow.includes('packet_loss') && metricsData.packet_loss !== undefined) {
      coreCards.push(<StatCard key="loss-count" title="Retransmissions" value={metricsData.packet_loss || 0} />);
  }
   if (detailsToShow.includes('packets_per_second') && metricsData.packets_per_second !== undefined) {
       coreCards.push(<StatCard key="pps" title="Packets/sec" value={(metricsData.packets_per_second || 0).toFixed(0)} />);
   }
   // Add the instantaneous throughput as a card
   if (detailsToShow.includes('throughput')) {
     const currentIn = (metricsData.inbound_throughput || 0).toFixed(2);
     const currentOut = (metricsData.outbound_throughput || 0).toFixed(2);
     coreCards.push(<StatCard key="current-throughput" title="Current Thrpt (In/Out)" value={`${currentIn} / ${currentOut}`} unit="Mbps" />);
   }

  // --- Determine which graphs to show ---
  const showThroughputGraph = detailsToShow.includes('throughput') && throughputHistory && throughputHistory.length > 0;
  const showLatencyGraph = protocolName === 'TCP' && detailsToShow.includes('latency') && latencyHistory && latencyHistory.length > 0;
  const showJitterGraph = protocolName === 'RTP' && detailsToShow.includes('jitter') && jitterHistory && jitterHistory.length > 0;

  // Calculate grid columns needed for charts (1 or 2)
  const chartCols = [showThroughputGraph, showLatencyGraph, showJitterGraph].filter(Boolean).length > 1 ? 2 : 1;

  return (
    <div className="bg-surface-dark p-6 rounded-xl border border-border-dark shadow-md">
      <h3 className="text-xl font-bold text-primary-accent mb-4">{protocolName} Metrics</h3>

      {/* --- Row 1: Core Stat Cards --- */}
      {coreCards.length > 0 ? (
         <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {coreCards}
        </div>
      ) : (
        <p className="text-text-secondary mb-4">No specific metrics available for {protocolName} in this capture.</p>
      )}

      {/* --- Row 2: Charts Area --- */}
      {(showThroughputGraph || showLatencyGraph || showJitterGraph) && (
          <div className={`mt-6 grid grid-cols-1 ${chartCols === 2 ? 'lg:grid-cols-2' : ''} gap-6`}>
              {/* Throughput Chart (Always show if applicable) */}
              {showThroughputGraph && (
                  <div className="h-72">
                      <MetricChart
                          title={`${protocolName} Throughput`}
                          unit=" Mbps"
                          data={throughputHistory}
                          lines={[
                              { dataKey: "inbound_throughput", name: "Inbound", color: "#2DD4BF" },
                              { dataKey: "outbound_throughput", name: "Outbound", color: "#3B82F6" }
                          ]}
                      />
                  </div>
              )}

              {/* Latency Chart (TCP Only) */}
              {showLatencyGraph && (
                   <div className="h-72">
                       <MetricChart
                           title="TCP RTT Latency"
                           unit=" ms"
                           // Extract latency from the full history object
                           data={latencyHistory.map(entry => ({ time: entry.time, latency: parseFloat(entry.latency?.toFixed(1) || 0) }))}
                           lines={[
                               { dataKey: "latency", name: "Latency", color: "#F472B6" }
                           ]}
                       />
                   </div>
              )}

              {/* Jitter Chart (RTP Only) */}
              {showJitterGraph && (
                  <div className="h-72">
                      <MetricChart
                          title="RTP Jitter"
                          unit=" ms"
                          // Extract jitter from the full history object
                          data={jitterHistory.map(entry => ({ time: entry.time, jitter: parseFloat(entry.jitter?.toFixed(1) || 0) }))}
                          lines={[
                              { dataKey: "jitter", name: "Jitter", color: "#FBBF24" }
                          ]}
                      />
                  </div>
              )}
          </div>
      )}

      {/* --- Row 3: KPIs Below Charts --- */}
      {showThroughputGraph && ( // Only show throughput KPIs if the graph is shown
           <div className="mt-4 flex flex-col sm:flex-row justify-center sm:justify-start gap-x-6 gap-y-1 text-sm">
                 {formatKpiText("Peak Throughput (In/Out)", throughputKPIs?.peakIn, throughputKPIs?.peakOut, "Mbps")}
                 {formatKpiText("Average Throughput (In/Out)", throughputKPIs?.avgIn, throughputKPIs?.avgOut, "Mbps")}
          </div>
      )}
    </div>
  );
}