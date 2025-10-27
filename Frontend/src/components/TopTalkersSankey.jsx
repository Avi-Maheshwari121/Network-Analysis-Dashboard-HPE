// Frontend/src/components/TopTalkersSankey.jsx
import React from 'react';
import { Chart } from 'react-google-charts';

// Helper to format bytes (remains the same)
const formatBytes = (bytes) => {
  // ... (keep existing implementation)
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = bytes > 0 ? Math.floor(Math.log(bytes) / Math.log(k)) : 0;
  const formattedValue = parseFloat((bytes / Math.pow(k, Math.max(0, i))).toFixed(1));
  return formattedValue + ' ' + sizes[Math.max(0, i)];
};

export default function TopTalkersSankey({ topTalkers }) {

  // Process data for Google Charts Sankey: [['From', 'To', 'Bytes'], ...]
  const processGoogleSankeyData = (data) => {
    if (!data || data.length === 0) {
      return null;
    }

    // *** CHANGED: Use 'Bytes' instead of 'Weight' in the header ***
    const chartData = [['From', 'To', 'Bytes']]; // Header row

    data.forEach(([srcIp, dstIp, packets, bytesStr]) => {
      const bytes = parseInt(bytesStr, 10);
      if (bytes > 0) {
        chartData.push([srcIp, dstIp, bytes]);
      }
    });

    return chartData.length > 1 ? chartData : null;
  };

  const googleSankeyData = processGoogleSankeyData(topTalkers);

  // --- Configuration Options for Google Charts Sankey ---
  const options = {
    tooltip: {
      isHtml: true, // Enable HTML for potential future customization
      // *** CHANGED: Set tooltip text style to black ***
      textStyle: {
          color: '#000000', // Black text color for tooltip content
          fontName: 'Arial',
          fontSize: 12,
      },
      // Note: Styling the default "From -> To: Value" labels *within* the tooltip
      // to black isn't directly possible via standard options.
      // If this is critical, a fully custom HTML tooltip would be needed.
    },
    sankey: {
      node: {
        label: {
          fontName: 'Arial',
          fontSize: 12,
          color: '#E6EDF3', // Node label color (kept light for dark background)
          bold: false,
          italic: false,
        },
        labelPadding: 10,
        nodePadding: 30,
        width: 10,
        colors: ['#2DD4BF', '#3B82F6', '#F472B6', '#FBBF24', '#8B5CF6', '#22C55E', '#d1d5db']
      },
      link: {
        colorMode: 'gradient',
        colors: ['#2DD4BF', '#3B82F6', '#F472B6', '#FBBF24', '#8B5CF6', '#22C55E', '#d1d5db']
      }
    },
    backgroundColor: 'transparent',
    chartArea: {
        left: 20,
        top: 20,
        width: '95%',
        height: '85%'
    }
  };

  return (
    <div className="bg-surface-dark p-4 rounded-xl border border-border-dark shadow-md h-96 flex flex-col mt-6">
      <h3 className="text-md font-semibold text-text-main mb-2">Top 7 Outbound Conversations (by Volume)</h3>
      {googleSankeyData ? (
        <Chart
          chartType="Sankey"
          width="100%"
          height="100%"
          data={googleSankeyData}
          options={options}
          loader={<div className="text-text-secondary">Loading Chart...</div>}
        />
      ) : (
        <div className="flex items-center justify-center h-full">
          <p className="text-text-secondary">No top talker data available for the current session.</p>
        </div>
      )}
    </div>
  );
}