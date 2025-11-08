// Frontend/src/components/MetricChart.jsx
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Label } from 'recharts';

/**
 * Helper function to determine the best unit for bitrate (bits per second)
 * and return the appropriate scale. This is for scaling the entire Y-axis.
 */
function getOptimalBitrateScale(data, lines) {
  let maxValue = 0;

  // Find the maximum value across all data points and lines
  data.forEach(point => {
    lines.forEach(line => {
      const value = point[line.dataKey];
      if (value && value > maxValue) {
        maxValue = value;
      }
    });
  });

  // Determine the appropriate unit based on max value (using 1000 for bits)
  const units = [
    { threshold: 1_000_000_000, divisor: 1_000_000_000, label: 'Gbps' }, // Giga-bits
    { threshold: 1_000_000,     divisor: 1_000_000,     label: 'Mbps' }, // Mega-bits
    { threshold: 1_000,         divisor: 1_000,         label: 'Kbps' }, // Kilo-bits
    { threshold: 0,             divisor: 1,             label: 'bps' }   // bits
  ];

  for (const unit of units) {
    if (maxValue >= unit.threshold) {
      return unit;
    }
  }

  return units[units.length - 1]; // Default to 'bps'
}

/**
 * A generic chart component that can be reused for different metrics.
 * If the 'unit' prop is set to "bps", it will dynamically scale the
 * Y-axis and legend to bps, Kbps, Mbps, or Gbps.
 */
export default function MetricChart({ data, lines, unit, title }) {
  // Check if this is a bitrate chart that needs dynamic scaling
  const isBitrateChart = unit === 'bps';

  // Get optimal scale only if it's a bitrate chart
  const scale = isBitrateChart ? getOptimalBitrateScale(data, lines) : null;

  // Scale the data if a scale has been determined
  const displayData = scale ? data.map(point => {
    const scaledPoint = { ...point };
    lines.forEach(line => {
      if (point[line.dataKey] !== undefined && point[line.dataKey] !== null) {
        // Scale the value
        scaledPoint[line.dataKey] = parseFloat((point[line.dataKey] / scale.divisor).toFixed(2));
      }
    });
    return scaledPoint;
  }) : data;
  
  const displayUnit = scale ? ` ${scale.label}` : (unit ? ` ${unit}` : '');

  // *** ADDED: Robust tick formatter to prevent float errors ***
  const yAxisTickFormatter = (tick) => {
    if (Math.abs(tick) < 0.01) return '0'; // Catches 0 and tiny floats
    if (tick < 1) return tick.toFixed(2); // e.g., 0.09
    if (tick < 10) return tick.toFixed(1); // e.g., 2.1
    return Math.round(tick); // e.g., 12
  };

  // Custom formatter for the tooltip
  const tooltipFormatter = (value, name, props) => {
    const formattedValue = value.toFixed(2);
    const unitLabel = scale ? scale.label : unit;
    return [`${formattedValue} ${unitLabel.trim()}`, name];
  };

  return (
    <div className="bg-surface-dark p-4 rounded-xl border border-border-dark shadow-md h-72 flex flex-col">
      <h3 className="text-md font-semibold text-text-main mb-4">{title}</h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={displayData} margin={{ top: 5, right: 20, left: 10, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#30363D" />
          <XAxis dataKey="time" stroke="#8B949E" fontSize={12} tick={{ fill: '#8B949E' }} />
          <YAxis
            stroke="#8B949E"
            fontSize={12}
            tick={{ fill: '#8B949E' }}
            // *** THIS IS THE FIX ***
            domain={[0, 'auto']} // Force bottom to 0, let Recharts pick a nice top
            tickFormatter={yAxisTickFormatter} // Add formatter back
          >
            <Label value={displayUnit.trim()} angle={-90} position="insideLeft" style={{ textAnchor: 'middle', fill: '#8B949E' }} />
          </YAxis>
          <Tooltip
            contentStyle={{
              backgroundColor: '#0D1117',
              borderColor: '#30363D',
              color: '#E6EDF3'
            }}
            labelStyle={{ color: '#8B949E' }}
            itemStyle={{ fontWeight: 'bold' }}
            formatter={tooltipFormatter} 
            labelFormatter={(label) => `Time: ${label}`} 
            itemSorter={(item) => -item.value} 
          />
          <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '20px' }} />
          {lines.map(line => (
            <Line
              key={line.dataKey}
              type="monotone"
              dataKey={line.dataKey}
              name={line.name}
              stroke={line.color}
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 6 }}
              isAnimationActive={false}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}