import React from 'react';
import { useVirtualizer } from '@tanstack/react-virtual';

export default function PacketTable({ packets }) {
  const parentRef = React.useRef(null);

  const [filterType, setFilterType] = React.useState('all');
  const [filterValue, setFilterValue] = React.useState('');
  const [filteredPackets, setFilteredPackets] = React.useState(packets);

  // Automatically apply filtering whenever inputs change
  React.useEffect(() => {
    applyFilterLogic();
  }, [packets, filterType, filterValue]);

  const applyFilterLogic = () => {
    const value = filterValue.trim().toLowerCase();

    if (!value) {
      setFilteredPackets(packets);
      return;
    }

    const filtered = packets.filter((packet) => {
      const src = packet?.source?.toLowerCase() || '';
      const dst = packet?.destination?.toLowerCase() || '';
      const proto = packet?.protocol?.toLowerCase() || '';
      const info = packet?.info?.toLowerCase() || '';

      switch (filterType) {
        case 'src':
          return src.includes(value);
        case 'dst':
          return dst.includes(value);
        case 'protocol':
          return proto.startsWith(value);
        case 'info':
          return info.includes(value);
        case 'all':
        default:
          // For “All Fields” — still partial matches for most, exact for protocol
          return (
            src.includes(value) ||
            dst.includes(value) ||
            proto.startsWith(value) ||
            info.includes(value)
          );
      }
    });

    setFilteredPackets(filtered);
  };

  const rowVirtualizer = useVirtualizer({
    count: filteredPackets.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 36,
    overscan: 15,
  });

  const gridTemplate = '80px 120px 140px 140px 80px 70px 1fr';
  const tableMinWidth = '1000px';

  return (
    <div className="bg-surface-dark border border-border-dark rounded-lg p-6 mt-6 flex flex-col">
      <h2 className="text-lg font-bold mb-4 text-primary-accent text-center">
        Raw Data of Captured Packets ({filteredPackets.length} shown of {packets.length})
      </h2>

      {/* Filter UI */}
      <div className="flex flex-wrap gap-2 mb-4 items-center">
        <label className="text-sm text-primary-accent font-bold">Filter by :</label>
        <select
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
          className="p-2 rounded bg-gray-800 text-primary-accent font-bold shadow disabled:opacity-50 hover:text-white transition-colors duration-200 outline-none border border-border-dark"
        >
          <option value="all">All Fields</option>
          <option value="src">Source IP</option>
          <option value="dst">Destination IP</option>
          <option value="protocol">Protocol</option>
          <option value="info">Info</option>
        </select>

        <input
          type="text"
          value={filterValue}
          onChange={(e) => setFilterValue(e.target.value)}
          placeholder="Enter value..."
          className="flex-1 min-w-[200px] p-2 rounded bg-gray-800 text-white outline-none border border-border-dark"
        />
      </div>

      {/* Table */}
      <div
        ref={parentRef}
        className="overflow-auto border border-gray-600"
        style={{ height: '70vh' }}
      >
        <div style={{ minWidth: tableMinWidth }}>
          {/* Table Header */}
          <div
            className="sticky top-0 bg-gray-800 text-gray-300 font-semibold text-sm border-b border-gray-600 z-10"
            style={{
              display: 'grid',
              gridTemplateColumns: gridTemplate,
              padding: '8px 0',
            }}
          >
            <div className="px-3 text-right">No.</div>
            <div className="px-3 text-center">Time</div>
            <div className="px-3 text-center">Source</div>
            <div className="px-3 text-center">Destination</div>
            <div className="px-3 text-left">Protocol</div>
            <div className="px-3 text-right">Length</div>
            <div className="px-3 text-left">Info</div>
          </div>

          {/* Virtualized Rows */}
          <div
            style={{
              height: `${rowVirtualizer.getTotalSize()}px`,
              width: '100%',
              position: 'relative',
            }}
          >
            {rowVirtualizer.getVirtualItems().map((virtualRow) => {
              const packet = filteredPackets[virtualRow.index];
              if (!packet) return null;

              return (
                <div
                  key={virtualRow.key}
                  className="absolute left-0 w-full text-sm text-gray-200 hover:bg-gray-700 border-b border-gray-700"
                  style={{
                    height: `${virtualRow.size}px`,
                    transform: `translateY(${virtualRow.start}px)`,
                    display: 'grid',
                    gridTemplateColumns: gridTemplate,
                    alignItems: 'center',
                    padding: '8px 0',
                  }}
                >
                  <div className="px-3 text-right truncate">{packet.no}</div>
                  <div className="px-3 text-center truncate text-gray-400">{packet.time}</div>
                  <div className="px-3 text-center truncate text-green-400">{packet.source}</div>
                  <div className="px-3 text-center truncate text-blue-400">{packet.destination}</div>
                  <div className="px-3 text-left truncate">{packet.protocol}</div>
                  <div className="px-3 text-right truncate text-gray-400">{packet.length}</div>
                  <div className="px-3 text-left truncate text-gray-400">{packet.info}</div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
