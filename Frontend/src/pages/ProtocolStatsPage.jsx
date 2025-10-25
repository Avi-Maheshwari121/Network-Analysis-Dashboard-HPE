// Frontend/src/pages/ProtocolStatsPage.jsx
import { useState } from 'react';
import StatusBanner from '../components/StatusBanner';
import ProtocolMetricsDisplay from '../components/ProtocolMetricsDisplay';
import IpCompositionPieChart from '../components/IpCompositionPieChart'; // Import the IP chart

// Simple StatCard component for reuse within this page only
const StatCard = ({ title, value, unit = '', subValue = '' }) => (
    // Style remains the same as the last correct version for uniform height
    <div className="bg-base-dark p-4 rounded-lg border border-border-dark flex flex-col justify-between text-center">
        <div><p className="text-sm font-semibold text-text-secondary uppercase mb-1">{title}</p></div>
        <div className="my-2"><p className="text-2xl font-bold text-text-main">{value} {unit && <span className="text-base">{unit}</span>}</p></div>
        <div className="h-4">{subValue ? <p className="text-xs text-text-secondary mt-1">{subValue}</p> : <p className="text-xs text-text-secondary mt-1">&nbsp;</p>}</div>
    </div>
);

export default function ProtocolStatsPage({
  wsConnected,
  error,
  metrics, // General metrics for status banner
  // Protocol Metrics Data (No IP)
  tcpMetrics,
  rtpMetrics,
  udpMetrics,
  quicMetrics,
  dnsMetrics,  // <-- Added
  igmpMetrics, // <-- Added
  // Protocol History & KPIs (No IP)
  tcpHistory,
  rtpHistory,
  udpHistory,
  quicHistory,
  dnsHistory,  // <-- Added
  igmpHistory, // <-- Added
  tcpKPIs,
  rtpKPIs,
  udpKPIs,
  quicKPIs,
  dnsKPIs,   // <-- Added
  igmpKPIs,  // <-- Added
  // Full Metrics History
  tcpFullMetricsHistory,
  rtpFullMetricsHistory,
}) {
  // Update initial visible state
  const [visibleProtocols, setVisibleProtocols] = useState({
    TCP: true,
    UDP: true,
    RTP: true,
    QUIC: false,
    DNS: true,   // <-- Added DNS
    IGMP: false, // <-- Added IGMP (default off)
  });

  // Handler remains the same
  const handleCheckboxChange = (event) => {
    const { name, checked } = event.target;
    setVisibleProtocols((prev) => ({ ...prev, [name]: checked }));
  };

  // Update configuration to include DNS/IGMP, remove IPv4/IPv6
  const protocols = [
    { name: 'TCP', data: tcpMetrics, throughputHistory: tcpHistory, latencyHistory: tcpFullMetricsHistory, kpis: tcpKPIs, details: ['latency', 'packet_loss', 'packets_per_second', 'throughput'] },
    { name: 'UDP', data: udpMetrics, throughputHistory: udpHistory, kpis: udpKPIs, details: ['packets_per_second', 'throughput'] },
    { name: 'RTP', data: rtpMetrics, throughputHistory: rtpHistory, jitterHistory: rtpFullMetricsHistory, kpis: rtpKPIs, details: ['jitter', 'packet_loss_percentage', 'packets_per_second', 'throughput'] },
    { name: 'QUIC', data: quicMetrics, throughputHistory: quicHistory, kpis: quicKPIs, details: ['packets_per_second', 'throughput'] },
    { name: 'DNS', data: dnsMetrics, throughputHistory: dnsHistory, kpis: dnsKPIs, details: ['packets_per_second', 'throughput'] },     // <-- Add DNS Config
    { name: 'IGMP', data: igmpMetrics, throughputHistory: igmpHistory, kpis: igmpKPIs, details: ['packets_per_second', 'throughput'] },   // <-- Add IGMP Config
  ];


  return (
    <div>
      <StatusBanner connected={wsConnected} error={error} metrics={metrics} />

      {/* --- Protocol Selection Checkboxes (Updated) --- */}
      <div className="bg-surface-dark p-4 rounded-lg border border-border-dark mb-6">
        <h2 className="text-lg font-semibold text-primary-accent mb-3">Protocols to Monitor:</h2>
        <div className="flex flex-wrap gap-x-6 gap-y-2">
          {/* This part correctly maps over the updated 'protocols' array */}
          {protocols.map((p) => (
            <label key={p.name} className="flex items-center gap-2 cursor-pointer text-text-main">
              <input
                type="checkbox"
                name={p.name}
                checked={!!visibleProtocols[p.name]} // Use !! for robustness
                onChange={handleCheckboxChange}
                className="form-checkbox h-4 w-4 text-primary-accent bg-surface-dark border-border-dark rounded focus:ring-primary-accent"
              />
              {p.name}
            </label>
          ))}
        </div>
      </div>
      {/* --- End Checkbox Section --- */}


      {/* --- Display Metrics and Graph Sections for Visible Protocols --- */}
      <div className="space-y-6">
        {protocols.map((p) =>
          visibleProtocols[p.name] && (
            <ProtocolMetricsDisplay
              key={p.name}
              protocolName={p.name}
              metricsData={p.data}
              detailsToShow={p.details}
              throughputHistory={p.throughputHistory}
              latencyHistory={p.latencyHistory} // Will be undefined for non-TCP
              jitterHistory={p.jitterHistory}   // Will be undefined for non-RTP
              throughputKPIs={p.kpis}
            />
          )
        )}
      {/* --- End Protocol Display Loop --- */}

        {/* --- REMOVED IP Composition Section --- */}

      </div>
    </div>
  );
}