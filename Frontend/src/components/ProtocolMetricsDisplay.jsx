// Frontend/src/components/ProtocolMetricsDisplay.jsx
import React from 'react';
import MetricChart from './MetricChart'; 
import { formatBitrate } from '../utils/formatBitrate'; // Use correct 1000-based formatter

// Simple StatCard component for reuse (no change)
const StatCard = ({ title, value, unit = '', subValue = '' }) => (
  <div className="bg-base-dark p-4 rounded-lg border border-border-dark text-center flex flex-col justify-between">
    <div>
      <p className="text-sm font-semibold text-text-secondary uppercase mb-1 whitespace-nowrap">{title}</p>
    </div>
    <div className="my-2">
      <p className="text-2xl font-bold text-text-main">
        {value} {unit && <span className="text-base">{unit}</span>}
      </p>
    </div>
   
  </div>
);

// A sub-component for the clean KPI Bar
const KpiBar = ({ kpis = {}, details = [] }) => {
  // Helper to create a single KPI stat
  const KpiStat = ({ label, value, unit }) => {
    // Don't render if the value from the backend is missing
    if (value === undefined || value === null) return null;
    
    return (
      <div className="text-center sm:text-left">
        <p className="text-xs text-text-secondary uppercase">{label}</p>
        <p className="text-lg font-bold text-text-main">
          {value} <span className="text-base text-text-secondary">{unit}</span>
        </p>
      </div>
    );
  };

  // Format all the values we need from the backend
  // The kpis object is guaranteed to be at least `{}` so this is safe.
  const inPeak = formatBitrate(Number(kpis?.inbound_throughput_peak) || 0);
  const inAvg = formatBitrate(Number(kpis?.inbound_throughput_avg) || 0);
  const outPeak = formatBitrate(Number(kpis?.outbound_throughput_peak) || 0);
  const outAvg = formatBitrate(Number(kpis?.outbound_throughput_avg) || 0);

  return (
    <div className="bg-base-dark p-4 rounded-lg border border-border-dark mt-4">
      {/* *** CHANGED: Removed sm:justify-start to apply justify-around everywhere *** */}
      <div className="flex flex-wrap justify-around gap-x-8 gap-y-4">
        <KpiStat label="Peak Inbound" value={inPeak.value} unit={inPeak.unit} />
        <KpiStat label="Avg Inbound" value={inAvg.value} unit={inAvg.unit} />
        <KpiStat label="Peak Outbound" value={outPeak.value} unit={outPeak.unit} />
        <KpiStat label="Avg Outbound" value={outAvg.value} unit={outAvg.unit} />
        
        {/* Conditional KPIs */}
        {details.includes('latency') && kpis.latency_avg !== undefined && (
          <>
            <KpiStat label="Peak Latency" value={(kpis.latency_peak || 0).toFixed(1)} unit="ms" />
            <KpiStat label="Avg Latency" value={(kpis.latency_avg || 0).toFixed(1)} unit="ms" />
          </>
        )}
        {details.includes('jitter') && kpis.jitter_avg !== undefined && (
          <>
            <KpiStat label="Peak Jitter" value={(kpis.jitter_peak || 0).toFixed(1)} unit="ms" />
            <KpiStat label="Avg Jitter" value={(kpis.jitter_avg || 0).toFixed(1)} unit="ms" />
          </>
        )}
      </div>
    </div>
  );
};


export default function ProtocolMetricsDisplay({
    protocolName,
    metricsData,
    detailsToShow = [],
    throughputHistory = [], 
    latencyHistory = [],    
    jitterHistory = [],     
    kpis, // This prop can be null
    fullMetricsHistory = [], 
}) {
  
  // *** THIS IS THE FIX: Create a "safe" kpiData object ***
  // It's either the kpis prop or an empty object, but never null.
  const kpiData = kpis || {};

  // Loading state (no change)
  if (!metricsData) {
    return (
      <div className="bg-surface-dark p-6 rounded-xl border border-border-dark shadow-md animate-pulse">
        <h3 className="text-xl font-bold text-primary-accent mb-4 h-6 bg-gray-700 rounded w-1/3"></h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
            <div className="h-24 bg-gray-700 rounded"></div>
            <div className="h-24 bg-gray-700 rounded"></div>
            <div className="h-24 bg-gray-700 rounded"></div>
            <div className="h-24 bg-gray-700 rounded"></div>
            <div className="h-24 bg-gray-700 rounded"></div>
        </div>
        <div className="mt-6 h-72 bg-gray-700 rounded"></div>
      </div>
    );
  }

  // --- Dynamically build the list of CORE cards ---
  const coreCards = [];

  // --- Add "Current" Stat Cards ---
  if (detailsToShow.includes('latency') && metricsData.latency !== undefined) {
    coreCards.push(<StatCard key="latency" title="Current Latency" value={(metricsData.latency || 0).toFixed(1)} unit="ms" />);
  }
  if (detailsToShow.includes('jitter') && metricsData.jitter !== undefined) {
      coreCards.push(<StatCard key="jitter" title="Current Jitter" value={(metricsData.jitter || 0).toFixed(1)} unit="ms" />);
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
   
   // --- Add "Current vs. Avg" Throughput Cards ---
   if (detailsToShow.includes('throughput')) {
     const inThrpt = formatBitrate(metricsData.inbound_throughput || 0);
     const outThrpt = formatBitrate(metricsData.outbound_throughput || 0);
     
     // *** CHANGED: Use the safe kpiData object ***
     const avgInFormatted = formatBitrate(Number(kpiData?.inbound_throughput_avg) || 0);
     const avgOutFormatted = formatBitrate(Number(kpiData?.outbound_throughput_avg) || 0);
     
     coreCards.push(
       <StatCard 
         key="inbound-throughput" 
         title="Inbound Throughput" 
         value={inThrpt.value} 
         unit={inThrpt.unit}
         // Use the safe kpiData object here
         subValue={kpis ? `Avg: ${avgInFormatted.value} ${avgInFormatted.unit}` : ''}
       />
     );
     coreCards.push(
       <StatCard 
         key="outbound-throughput" 
         title="Outbound Throughput" 
         value={outThrpt.value} 
         unit={outThrpt.unit}
         // and here
         subValue={kpis ? `Avg: ${avgOutFormatted.value} ${avgOutFormatted.unit}` : ''}
       />
     );
   }

  // --- Determine which graphs to show (no change) ---
  const showThroughputGraph = detailsToShow.includes('throughput') && throughputHistory && throughputHistory.length > 0;
  const showPpsGraph = detailsToShow.includes('packets_per_second') && fullMetricsHistory && fullMetricsHistory.length > 0;
  const showLatencyGraph = (protocolName === 'TCP' || protocolName === 'QUIC') && detailsToShow.includes('latency') && latencyHistory && latencyHistory.length > 0;
  const showJitterGraph = protocolName === 'RTP' && detailsToShow.includes('jitter') && jitterHistory && jitterHistory.length > 0;

  return (
    <div className="bg-surface-dark p-6 rounded-xl border border-border-dark shadow-md">
      {/* --- Row 1: Title --- */}
      <h3 className="text-xl font-bold text-primary-accent mb-4">{protocolName} Metrics</h3>

      {/* --- Row 2: Core Stat Cards --- */}
      {coreCards.length > 0 ? (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
          {coreCards}
        </div>
      ) : (
        <p className="text-text-secondary mb-4">No specific metrics available for {protocolName} in this capture.</p>
      )}

       {/* --- Row 3: Session KPI Bar --- */}
      {/* *** CHANGED: Pass the safe kpiData object, not the null kpis prop *** */}
      <KpiBar kpis={kpiData} details={detailsToShow} />

     

      {/* --- Row 4: Charts Area (Layout is correct now) --- */}
      <div className="mt-6 space-y-6">
        {/* First chart row (always 2 cols) */}
        {(showThroughputGraph || showPpsGraph) && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {showThroughputGraph && (
              <div className="h-72">
                <MetricChart
                  title="Throughput Over Time"
                  unit="bps" 
                  data={throughputHistory}
                  lines={[
                    { dataKey: "inbound_throughput", name: "Inbound", color: "#2DD4BF" },
                    { dataKey: "outbound_throughput", name: "Outbound", color: "#3B82F6" }
                  ]}
                />
              </div>
            )}
            {showPpsGraph && (
              <div className="h-72">
                <MetricChart
                  title="Packets Per Second Over Time"
                  unit="pps"
                  data={fullMetricsHistory.map(entry => ({ 
                    time: entry.time, 
                    packets_per_second: Math.round(entry.packets_per_second || 0) 
                  }))}
                  lines={[
                    { dataKey: "packets_per_second", name: "Packets/sec", color: "#8B5CF6" }
                  ]}
                />
              </div>
            )}
            
          </div>
        )}
       

        {/* Second chart row (for Latency/Jitter) */}
        {(showLatencyGraph || showJitterGraph) && (
          <div className="grid grid-cols-1 gap-6">
            {showLatencyGraph && (
              <div className={`h-72 ${showThroughputGraph && showPpsGraph ? 'md:col-span-2' : ''}`}>
                <MetricChart
                  title={`${protocolName} RTT Latency Over Time`}
                  unit="ms"
                  data={latencyHistory.map(entry => ({ 
                    time: entry.time, 
                    latency: parseFloat(entry.latency?.toFixed(1) || 0) 
                  }))}
                  lines={[
                    { dataKey: "latency", name: "Latency", color: "#F472B6" }
                  ]}
                />
              </div>
            )}
            
            {showJitterGraph && (
              <div className={`h-72 ${showThroughputGraph && showPpsGraph ? 'md:col-span-2' : ''}`}>
                <MetricChart
                  title="RTP Jitter Over Time"
                  unit="ms"
                  data={jitterHistory.map(entry => ({ 
                    time: entry.time, 
                    jitter: parseFloat(entry.jitter?.toFixed(1) || 0) 
                  }))}
                  lines={[
                    { dataKey: "jitter", name: "Jitter", color: "#FBBF24" }
                  ]}
                />
              </div>
            )}
             
          </div>
        )}
      </div>

    </div>
  );
}