// Frontend/src/pages/TrafficCompositionPage.jsx
import React from 'react';
import StatusBanner from '../components/StatusBanner';
import ProtocolMetricsDisplay from '../components/ProtocolMetricsDisplay'; // Reusable component for IPv4/IPv6 display
import IpCompositionPieChart from '../components/IpCompositionPieChart'; // Use the cumulative pie chart
import EncryptionCompositionPieChart from '../components/EncryptionCompositionPieChart'; // New Encryption Pie Chart Component

// Simple StatCard component for reuse within this page only
const StatCard = ({ title, value, unit = '', subValue = '' }) => (
    <div className="bg-base-dark p-4 rounded-lg border border-border-dark flex flex-col justify-between text-center h-full">
        <div><p className="text-sm font-semibold text-text-secondary uppercase mb-1">{title}</p></div>
        <div className="my-2"><p className="text-2xl font-bold text-text-main">{value} {unit && <span className="text-base">{unit}</span>}</p></div>
        <div className="h-4">{subValue ? <p className="text-xs text-text-secondary mt-1">{subValue}</p> : <p className="text-xs text-text-secondary mt-1">&nbsp;</p>}</div>
    </div>
);

// Define the component function
function TrafficCompositionPage({
  wsConnected,
  error,
  metrics, // For status banner
  ipv4Metrics,
  ipv6Metrics,
  ipComposition,
  ipv4History,
  ipv6History,
  ipv4KPIs,
  ipv6KPIs,
  encryptionComposition,
}) {

  // Configuration for IP versions display
  const ipVersions = [
    { name: 'IPv4', data: ipv4Metrics, throughputHistory: ipv4History, kpis: ipv4KPIs, details: ['packets_per_second', 'throughput'] },
    { name: 'IPv6', data: ipv6Metrics, throughputHistory: ipv6History, kpis: ipv6KPIs, details: ['packets_per_second', 'throughput'] },
  ];

  return (
    <div>
      <StatusBanner connected={wsConnected} error={error} metrics={metrics} />

      {/* Display IPv4 and IPv6 Metrics */}
      <div className="space-y-6 mb-6"> {/* Add margin below IP version details */}
        {ipVersions.map((ipVer) => (
          <ProtocolMetricsDisplay
            key={ipVer.name}
            protocolName={ipVer.name} // Display as "IPv4 Metrics", "IPv6 Metrics"
            metricsData={ipVer.data}
            detailsToShow={ipVer.details}
            throughputHistory={ipVer.throughputHistory}
            throughputKPIs={ipVer.kpis}
            // No latency/jitter history needed here
          />
        ))}
      </div>

      {/* Display IP Composition Section (using cumulative data) */}
      {ipComposition && (
        <div className="bg-surface-dark p-6 rounded-xl border border-border-dark shadow-md mb-6">
          <h3 className="text-xl font-bold text-primary-accent mb-4">Cumulative IP Composition</h3>
          {/* Grid for Cards and Pie Chart */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
            {/* Column 1 & 2: Stat Cards using cumulative data */}
            <div className="md:col-span-2 grid grid-cols-1 sm:grid-cols-3 gap-4">
               {/* Use cumulative counts from ipComposition */}
              <StatCard title="Total IP Packets (Session)" value={ipComposition.ipv4_packets_cumulative + ipComposition.ipv6_packets_cumulative || 0} />
              <StatCard title="IPv4 Packets (Session)" value={`${ipComposition.ipv4_packets_cumulative || 0}`} subValue={`(${(ipComposition.ipv4_percentage || 0).toFixed(1)}%)`} />
              <StatCard title="IPv6 Packets (Session)" value={`${ipComposition.ipv6_packets_cumulative || 0}`} subValue={`(${(ipComposition.ipv6_percentage || 0).toFixed(1)}%)`} />
            </div>
            {/* Column 3: Pie Chart (uses cumulative data via prop) */}
            <div className="md:col-span-1">
              {/* Pass the updated ipComposition object */}
              <IpCompositionPieChart data={ipComposition} />
            </div>
          </div>
        </div>
      )}

      {/*Encryption Composition Section */}
      {encryptionComposition && (
        <div className="bg-surface-dark p-6 rounded-xl border border-border-dark shadow-md">
          <h3 className="text-xl font-bold text-primary-accent mb-4">Cumulative Encryption Composition</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
            {/* Column 1 & 2: Stat Cards using cumulative encryption data */}
            <div className="md:col-span-2 grid grid-cols-1 sm:grid-cols-3 gap-4">
               <StatCard
                 title="Total Packets (Session)"
                 value={encryptionComposition.encrypted_packets_cumulative + encryptionComposition.unencrypted_packets_cumulative || 0}
               />
               <StatCard
                 title="Encrypted Packets (Session)"
                 value={`${encryptionComposition.encrypted_packets_cumulative || 0}`}
                 subValue={`(${(encryptionComposition.encrypted_percentage || 0).toFixed(1)}%)`} // Use overall percentage if available, otherwise calc
               />
               <StatCard
                 title="Unencrypted Packets (Session)"
                 value={`${encryptionComposition.unencrypted_packets_cumulative || 0}`}
                 subValue={`(${(encryptionComposition.unencrypted_percentage || 0).toFixed(1)}%)`} // Use overall percentage if available, otherwise calc
               />
            </div>
            {/* Column 3: Pie Chart */}
            <div className="md:col-span-1">
              <EncryptionCompositionPieChart data={encryptionComposition} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// Add the missing export default statement
export default TrafficCompositionPage; // <-- THIS LINE WAS MISSING