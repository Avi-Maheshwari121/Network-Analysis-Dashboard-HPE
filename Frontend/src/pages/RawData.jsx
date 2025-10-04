import StatusBanner from "../components/StatusBanner";
import PacketTable from "../components/PacketTable";

export default function RawData({ wsConnected, packets, error, metrics }) {
  return (
    <div>
      <StatusBanner connected={wsConnected} error={error} metrics={metrics} />
      <PacketTable packets={packets} />
    </div>
  );
}