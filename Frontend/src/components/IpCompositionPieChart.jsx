// Frontend/src/components/IpCompositionPieChart.jsx
import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const IP_COLORS = {
    IPv4: '#3B82F6', // Blue
    IPv6: '#F472B6', // Pink
};

export default function IpCompositionPieChart({ data }) {
    const ipv4Cumulative = data?.ipv4_packets_cumulative || 0;
    const ipv6Cumulative = data?.ipv6_packets_cumulative || 0;
    const totalCumulative = ipv4Cumulative + ipv6Cumulative;

    if (!data || totalCumulative === 0) {
        return (
            <div className="bg-surface-dark p-4 rounded-xl border border-border-dark shadow-md h-full flex items-center justify-center">
                <p className="text-text-secondary">No cumulative IP composition data available.</p>
            </div>
        );
    }

    const chartData = [
        { name: 'IPv4', value: ipv4Cumulative, fill: IP_COLORS.IPv4 },
        { name: 'IPv6', value: ipv6Cumulative, fill: IP_COLORS.IPv6 },
    ].filter(entry => entry.value > 0);

    if (chartData.length === 0) {
       return (
            <div className="bg-surface-dark p-4 rounded-xl border border-border-dark shadow-md h-full flex items-center justify-center">
                <p className="text-text-secondary">No IPv4 or IPv6 packets detected in session.</p>
            </div>
        );
    }

    // Get percentages for the new stats block
    const ipv4Percent = (data.ipv4_percentage || 0).toFixed(1);
    const ipv6Percent = (data.ipv6_percentage || 0).toFixed(1);

    return (
        // *** CHANGED: Removed fixed height, added h-full ***
        <div className="bg-surface-dark p-4 rounded-xl border border-border-dark shadow-md h-full flex flex-col">
          <h3 className="text-md font-semibold text-text-main mb-2">IP Version Distribution</h3>
          
          {/* *** ADDED: Moved Legend to the top to prevent clipping *** */}
          <div className="flex justify-center w-full mb-2">
            <Legend
              payload={chartData.map(entry => ({
                value: entry.name,
                type: 'square',
                color: entry.fill
              }))}
              wrapperStyle={{ fontSize: '14px' }}
            />
          </div>

          {/* Chart Container */}
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                outerRadius={90} // Slightly smaller radius to fit
                fill="#8884d8"
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
                formatter={(value, name) => {
                    const percentage = (name === 'IPv4' ? ipv4Percent : ipv6Percent);
                    return [`${value.toLocaleString()} packets (${percentage}%)`, name];
                }}
              />
            </PieChart>
          </ResponsiveContainer>
          
          {/* *** ADDED: New Stats Block (Your Idea) *** */}
          <div className="flex-grow flex justify-around items-center pt-4 border-t border-border-dark">
            <div className="text-center">
              <p className="text-3xl font-bold" style={{ color: IP_COLORS.IPv4 }}>
                {ipv4Percent}%
              </p>
              <p className="text-sm text-text-secondary">IPv4</p>
            </div>
            <div className="text-center">
              <p className="text-3xl font-bold" style={{ color: IP_COLORS.IPv6 }}>
                {ipv6Percent}%
              </p>
              <p className="text-sm text-text-secondary">IPv6</p>
            </div>
          </div>

        </div>
      );
}