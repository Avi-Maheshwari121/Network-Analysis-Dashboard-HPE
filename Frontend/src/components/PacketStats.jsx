export default function PacketStats({ total_packets, stream_count, protocol_distribution }) {
  if (!protocol_distribution) return null;
  return (
    <div className="bg-surface-dark border border-border-dark rounded-lg p-4 my-4 flex flex-col">
      <h3 className="text-lg font-semibold text-primary-accent mb-2">Packet Stats</h3>
      <div className="flex justify-between w-full mb-2">
        <div>Total Packets: <span className="font-bold">{total_packets}</span></div>
        <div>Streams: <span className="font-bold">{stream_count}</span></div>
      </div>
      <div>
        <h4 className="text-sm text-text-secondary mb-1">Protocol Distribution:</h4>
        <ul>
          {Object.entries(protocol_distribution).map(([proto, count], idx) => (
            <li key={idx}>{proto}: <span className="font-bold">{count}</span></li>
          ))}
        </ul>
      </div>
    </div>
  );
}
