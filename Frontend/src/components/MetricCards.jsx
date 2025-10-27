// Frontend/src/components/MetricCards.jsx
import React from 'react';
import { ArrowDownCircle, ArrowUpCircle, Activity, Target, ShieldCheck } from 'lucide-react'; // Added Target and ShieldCheck icons

// Use metrics object directly
export default function MetricCards({ metrics }) {

  const Card = ({ title, value, unit, icon: Icon }) => (
    // Adjusted card style for better consistency if needed, but keeping original for now
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
       {/* Keep the spacer div for consistent height */}
       <div className="h-4 mt-1">
          <p className="text-xs">&nbsp;</p>
       </div>
    </div>
  );

  // Safely access metric values
  const inboundThroughput = metrics ? (metrics.inbound_throughput || 0).toFixed(2) : "0.00";
  const outboundThroughput = metrics ? (metrics.outbound_throughput || 0).toFixed(2) : "0.00";
  // *** NEW: Safely access goodput values ***
  const inboundGoodput = metrics ? (metrics.inbound_goodput || 0).toFixed(2) : "0.00";
  const outboundGoodput = metrics ? (metrics.outbound_goodput || 0).toFixed(2) : "0.00";
  // Get PPS directly from metrics object, round it
  const pps = metrics?.packets_per_second ? Math.round(metrics.packets_per_second) : "0";

  return (
    // *** UPDATED: Changed grid columns for 5 items. Adjust breakpoints as needed. ***
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6 mb-6">
      <Card title="Inbound Thrpt" value={inboundThroughput} unit="Mbps" icon={ArrowDownCircle} />
      <Card title="Outbound Thrpt" value={outboundThroughput} unit="Mbps" icon={ArrowUpCircle} />
      {/* *** NEW: Added Goodput Cards *** */}
      <Card title="Inbound Goodput" value={inboundGoodput} unit="Mbps" icon={Target} />
      <Card title="Outbound Goodput" value={outboundGoodput} unit="Mbps" icon={ShieldCheck} />
      <Card title="Packets/Sec" value={pps} icon={Activity} />
    </div>
  );
}