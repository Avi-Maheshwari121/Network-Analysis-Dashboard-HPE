// Frontend/src/components/MetricCards.jsx
import React from 'react';
import { ArrowDownCircle, ArrowUpCircle, Activity, Target, ShieldCheck } from 'lucide-react';
// Import our new, correct formatter
import { formatBitrate } from '../utils/formatBitrate';

export default function MetricCards({ metrics }) {

  const Card = ({ title, value, unit, icon: Icon }) => (
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
        <p className="text-xs">&nbsp;</p>
      </div>
    </div>
  );

  // Use the new formatBitrate function.
  // The backend will send raw bps (e.g., 15000000)
  const inboundThrpt = formatBitrate(metrics?.inbound_throughput || 0);
  const outboundThrpt = formatBitrate(metrics?.outbound_throughput || 0);
  const inboundGood = formatBitrate(metrics?.inbound_goodput || 0);
  const outboundGood = formatBitrate(metrics?.outbound_goodput || 0);
  
  const pps = metrics?.packets_per_second ? Math.round(metrics.packets_per_second) : "0";

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6 mb-6">
      <Card title="In Throughput" value={inboundThrpt.value} unit={inboundThrpt.unit} icon={ArrowDownCircle} />
      <Card title="Out Throughput" value={outboundThrpt.value} unit={outboundThrpt.unit} icon={ArrowUpCircle} />
      <Card title="Inbound Goodput" value={inboundGood.value} unit={inboundGood.unit} icon={ArrowDownCircle} />
      <Card title="Outbound Goodput" value={outboundGood.value} unit={outboundGood.unit} icon={ArrowUpCircle} />
      <Card title="Packets/Sec" value={pps} icon={Activity} />
    </div>
  );
}