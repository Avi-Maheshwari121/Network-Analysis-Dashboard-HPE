// Frontend/src/pages/TrafficCompositionPage.jsx
import React from 'react';
import StatusBanner from '../components/StatusBanner';
import ProtocolMetricsDisplay from '../components/ProtocolMetricsDisplay'; 
import IpCompositionPieChart from '../components/IpCompositionPieChart'; 
import EncryptionCompositionPieChart from '../components/EncryptionCompositionPieChart'; 

// Simple StatCard component for reuse (no change)
const StatCard = ({ title, value, unit = '', subValue = '' }) => (
    <div className="bg-base-dark p-4 rounded-lg border border-border-dark flex flex-col justify-between text-center h-full">
        <div><p className="text-sm font-semibold text-text-secondary uppercase mb-1">{title}</p></div>
        <div className="my-2"><p className="text-2xl font-bold text-text-main">{value} {unit && <span className="text-base">{unit}</span>}</p></div>
        <div className="h-4">{subValue ? <p className="text-xs text-text-secondary mt-1">{subValue}</p> : <p className="text-xs text-text-secondary mt-1">&nbsp;</p>}</div>
    </div>
);

function TrafficCompositionPage({
  wsConnected,
  error,
  metrics, // For status banner
  ipv4Metrics,
  ipv6Metrics,
  ipComposition,
  ipv4History,
  ipv6History,
  // *** Receive the KPI props from App.jsx ***
  ipv4KPIs,
  ipv6KPIs, 
  ipv4FullMetricsHistory, 
  ipv6FullMetricsHistory,
  encryptionComposition,
}) {

  // *** Assign the KPI props to the config object ***
  const ipVersions = [
    { name: 'IPv4', data: ipv4Metrics, throughputHistory: ipv4History, kpis: ipv4KPIs, details: ['packets_per_second', 'throughput'], fullHistory: ipv4FullMetricsHistory },
    { name: 'IPv6', data: ipv6Metrics, throughputHistory: ipv6History, kpis: ipv6KPIs, details: ['packets_per_second', 'throughput'], fullHistory: ipv6FullMetricsHistory },
  ];

  // Calculate totals
  const totalIpPackets = (ipComposition?.ipv4_packets_cumulative || 0) + (ipComposition?.ipv6_packets_cumulative || 0);
  const totalEncryptionPackets = (encryptionComposition?.encrypted_packets_cumulative || 0) + (encryptionComposition?.unencrypted_packets_cumulative || 0);

  return (
    <div>
      <StatusBanner connected={wsConnected} error={error} metrics={metrics} />

      {/* Display IPv4 and IPv6 Metrics */}
      <div className="space-y-6 mb-6"> 
        {ipVersions.map((ipVer) => (
          <ProtocolMetricsDisplay
            key={ipVer.name}
            protocolName={ipVer.name} 
            metricsData={ipVer.data}
            detailsToShow={ipVer.details}
            throughputHistory={ipVer.throughputHistory}
            // *** THE FIX: Pass prop as `kpis`, not `throughputKPIs` ***
            kpis={ipVer.kpis} 
            fullMetricsHistory={ipVer.fullHistory}
          />
        ))}
      </div>

      {/* --- RE-DESIGNED IP Composition Section --- */}
      {ipComposition && (
        <div className="bg-surface-dark p-6 rounded-xl border border-border-dark shadow-md mb-6">
          <h3 className="text-xl font-bold text-primary-accent mb-4">Cumulative IP Composition</h3>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <div className="lg:col-span-2">
              <IpCompositionPieChart data={ipComposition} />
            </div>
            
            <div className="lg:col-span-1 flex flex-col gap-4 justify-center h-full">
              <StatCard title="Total IP Packets (Session)" value={totalIpPackets.toLocaleString()} />
              <StatCard title="IPv4 Packets (Session)" value={`${(ipComposition.ipv4_packets_cumulative || 0).toLocaleString()}`} />
              <StatCard title="IPv6 Packets (Session)" value={`${(ipComposition.ipv6_packets_cumulative || 0).toLocaleString()}`} />
            </div>
          
          </div>
        </div>
      )}

      {/* --- RE-DESIGNED Encryption Composition Section --- */}
      {encryptionComposition && (
        <div className="bg-surface-dark p-6 rounded-xl border border-border-dark shadow-md">
          <h3 className="text-xl font-bold text-primary-accent mb-4">Cumulative Encryption Composition</h3>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <div className="lg:col-span-2">
              <EncryptionCompositionPieChart data={encryptionComposition} />
            </div>

            <div className="lg:col-span-1 flex flex-col gap-4 justify-center h-full">
              <StatCard
                title="Total Packets (Session)"
                value={totalEncryptionPackets.toLocaleString()}
              />
              <StatCard
                title="Encrypted Packets (Session)"
                value={`${(encryptionComposition.encrypted_packets_cumulative || 0).toLocaleString()}`}
              />
              <StatCard
                title="Unencrypted Packets (Session)"
                value={`${(encryptionComposition.unencrypted_packets_cumulative || 0).toLocaleString()}`}
              />
            </div>

          </div>
        </div>
      )}
    </div>
  );
}

export default TrafficCompositionPage;