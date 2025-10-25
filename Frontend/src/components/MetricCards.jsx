// Frontend/src/components/MetricCards.jsx
import React from 'react';
import { ArrowDownCircle, ArrowUpCircle, Activity } from 'lucide-react';

// Use metrics object directly
export default function MetricCards({ metrics }) {

  const Card = ({ title, value, unit, subValue, icon: Icon }) => (
    <div className="bg-surface-dark p-5 rounded-xl border border-border-dark text-center shadow-md flex flex-col justify-between h-full">
      <div>
        <div className="flex items-center justify-center gap-2 mb-2">
          {Icon && <Icon className="text-primary-accent" size={18} />}
          <p className="text-sm font-semibold text-text-secondary uppercase">{title}</p>
        </div>
        <p className="text-3xl font-bold text-text-main">
          {value} {unit && <span className="text-lg">{unit}</span>}
        </p>
      </div>
       <div className="h-4 mt-1">
          {subValue ? <p className="text-xs text-text-secondary font-bold">{subValue}</p> : <p className="text-xs">&nbsp;</p>}
       </div>
    </div>
  );

  // Safely access metric values
  const inboundThroughput = metrics ? (metrics.inbound_throughput || 0).toFixed(2) : "0.00";
  const outboundThroughput = metrics ? (metrics.outbound_throughput || 0).toFixed(2) : "0.00";
  // Get PPS directly from metrics object, round it
  const pps = metrics?.packets_per_second ? Math.round(metrics.packets_per_second) : "0";

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <Card title="Inbound" value={inboundThroughput} unit="Mbps" icon={ArrowDownCircle} />
      <Card title="Outbound" value={outboundThroughput} unit="Mbps" icon={ArrowUpCircle} />
      <Card title="Packets/Sec" value={pps} icon={Activity} /> {/* Display calculated value */}
    </div>
  );
}