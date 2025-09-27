import StatusBanner from "../components/StatusBanner";
import PacketTable from "../components/PacketTable";

export default function RawData({ wsConnected, packets, error }) {
  return (
    <div>
      <StatusBanner connected={wsConnected} error={error} />
      <PacketTable packets={packets} />
    </div>
  );
}
