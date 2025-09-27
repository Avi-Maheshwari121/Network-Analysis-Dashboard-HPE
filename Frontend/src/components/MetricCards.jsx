import React from 'react';
import { ArrowDownCircle, ArrowUpCircle } from 'lucide-react';

export default function MetricCards({ metrics, streamCount }) {
  const Card = ({ title, value, unit, subValue, icon: Icon }) => (
    <div className="bg-surface-dark p-5 rounded-xl border border-border-dark text-center shadow-md">
      <div className="flex items-center justify-center gap-2 mb-2">
        {Icon && <Icon className="text-primary-accent" size={18} />}
        <p className="text-sm font-semibold text-text-secondary uppercase">{title}</p>
      </div>
      <p className="text-3xl font-bold text-text-main">
        {value} {unit && <span className="text-lg">{unit}</span>}
      </p>
      {subValue && <p className="text-xs text-text-secondary mt-1 font-bold">{subValue}</p>}
    </div>
  );

  // Safely access metric values, providing defaults if metrics object is null
  const inboundThroughput = metrics ? (metrics.inbound_throughput || 0).toFixed(2) : "0.00";
  const outboundThroughput = metrics ? (metrics.outbound_throughput || 0).toFixed(2) : "0.00";
  const latency = metrics ? metrics.latency.toFixed(1) : "0.0";
  const jitter = metrics ? (metrics.jitter || 0).toFixed(1) : "0.0";
  const packetLossCount = metrics ? metrics.packet_loss_count : "0";
  const packetLossPercent = metrics ? (metrics.packet_loss_percent || 0).toFixed(2) : "0.00";

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-6">
      <Card title="Inbound" value={inboundThroughput} unit="Mbps" icon={ArrowDownCircle} />
      <Card title="Outbound" value={outboundThroughput} unit="Mbps" icon={ArrowUpCircle} />
      <Card title="Latency" value={latency} unit="ms" />
      <Card title="Jitter" value={jitter} unit="ms" />
      <Card
        title="Packet Loss"
        value={packetLossCount}
        subValue={`(${packetLossPercent}%)`}
      />
    </div>
  );
}