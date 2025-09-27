import React from 'react';
import { useVirtualizer } from '@tanstack/react-virtual';

export default function PacketTable({ packets }) {
  const parentRef = React.useRef(null);

  const rowVirtualizer = useVirtualizer({
    count: packets.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 36, // Row height in pixels
    overscan: 15,
  });

  // 1. Increased width of the first column from 60px to 80px
  const gridTemplate = '80px 120px 140px 140px 80px 70px 1fr';
  // 2. Define a minimum width for the table to enable horizontal scrolling
  const tableMinWidth = '1000px';

  return (
    <div className="bg-surface-dark border border-border-dark rounded-lg p-6 mt-6 flex flex-col">
      <h2 className="text-lg font-bold mb-4 text-primary-accent text-center">
        Raw Data of Captured Packets ({packets.length} stored)
      </h2>
      
      {/* Container with fixed height and scroll (now handles vertical and horizontal) */}
      <div 
        ref={parentRef} 
        className="overflow-auto border border-gray-600"
        style={{ height: '70vh' }}
      >
        {/* Wrapper to enforce minimum width for the table content */}
        <div style={{ minWidth: tableMinWidth }}>
          {/* Sticky Header */}
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

          {/* Virtualized Content Container */}
          <div
            style={{
              height: `${rowVirtualizer.getTotalSize()}px`,
              width: '100%',
              position: 'relative',
            }}
          >
            {/* Virtual Rows */}
            {rowVirtualizer.getVirtualItems().map((virtualRow) => {
              const packet = packets[virtualRow.index];
              if (!packet) return null;

              return (
                <div
                  key={virtualRow.key}
                  className="absolute left-0 w-full text-sm text-gray-200 hover:bg-gray-700 border-b border-gray-700"
                  style={{
                    height: `${virtualRow.size}px`,
                    transform: `translateY(${virtualRow.start}px)`,
                    display: 'grid',
                    gridTemplateColumns: gridTemplate, // Same grid as header
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