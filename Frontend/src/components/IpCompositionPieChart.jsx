// Frontend/src/components/IpCompositionPieChart.jsx
import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

// Define specific colors for IP versions
const IP_COLORS = {
    IPv4: '#3B82F6', // Blue
    IPv6: '#F472B6', // Pink
};

export default function IpCompositionPieChart({ data }) {
    // Check if cumulative data is present and non-zero
    // Use the cumulative keys from the backend shared_state.py
    const ipv4Cumulative = data?.ipv4_packets_cumulative || 0;
    const ipv6Cumulative = data?.ipv6_packets_cumulative || 0;
    const totalCumulative = ipv4Cumulative + ipv6Cumulative;

    if (!data || totalCumulative === 0) {
        return (
            <div className="bg-surface-dark p-4 rounded-xl border border-border-dark shadow-md h-72 flex items-center justify-center">
                <p className="text-text-secondary">No cumulative IP composition data available.</p>
            </div>
        );
    }

    // Prepare data for the Pie Chart using CUMULATIVE counts
    const chartData = [
        { name: 'IPv4', value: ipv4Cumulative, fill: IP_COLORS.IPv4 },
        { name: 'IPv6', value: ipv6Cumulative, fill: IP_COLORS.IPv6 },
    ].filter(entry => entry.value > 0); // Only include if count > 0

    // Handle case where filtering results in empty data (unlikely now)
    if (chartData.length === 0) {
       return (
            <div className="bg-surface-dark p-4 rounded-xl border border-border-dark shadow-md h-72 flex items-center justify-center">
                <p className="text-text-secondary">No IPv4 or IPv6 packets detected in session.</p>
            </div>
        );
    }

    return (
        <div className="bg-surface-dark p-4 rounded-xl border border-border-dark shadow-md h-72">
          {/* Updated Title */}
          <h3 className="text-md font-semibold text-text-main mb-4">Cumulative IP Version Distribution</h3>
          <ResponsiveContainer width="100%" height="85%">
            <PieChart margin={{ top: 20 }}>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                outerRadius={80}
                fill="#8884d8" // Default fill, overridden by Cell
                dataKey="value"
                nameKey="name"
              >
                {chartData.map((entry) => (
                  <Cell key={`cell-${entry.name}`} fill={entry.fill} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0D1117',
                  borderColor: '#30363D',
                }}
                itemStyle={{ color: '#E6EDF3' }}
                labelStyle={{ color: '#8B949E' }}
                 // Update formatter to use totalCumulative and correct percentage source from ipComposition object
                formatter={(value, name, props) => {
                    const percentage = (name === 'IPv4' ? data.ipv4_percentage : data.ipv6_percentage) || 0;
                    return [`${value} packets (${percentage.toFixed(1)}%)`, name];
                }}
              />
              <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '20px' }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      );
}