import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

// Define specific colors
const ENCRYPTION_COLORS = {
    Encrypted: '#5e8ccdff', // Blue 
    Unencrypted: '#96d65dff', // Green
};

export default function EncryptionCompositionPieChart({ data }) {
    // Use cumulative counts from the backend
    const encryptedCumulative = data?.encrypted_packets_cumulative || 0;
    const unencryptedCumulative = data?.unencrypted_packets_cumulative || 0;
    const totalCumulative = encryptedCumulative + unencryptedCumulative;

    if (!data || totalCumulative === 0) {
        return (
            <div className="bg-surface-dark p-4 rounded-xl border border-border-dark shadow-md h-72 flex items-center justify-center">
                <p className="text-text-secondary">No encryption data available for session.</p>
            </div>
        );
    }

    // Prepare data for the Pie Chart using CUMULATIVE counts
    const chartData = [
        { name: 'Encrypted', value: encryptedCumulative, fill: ENCRYPTION_COLORS.Encrypted },
        { name: 'Unencrypted', value: unencryptedCumulative, fill: ENCRYPTION_COLORS.Unencrypted },
    ].filter(entry => entry.value > 0); // Only include if count > 0

    if (chartData.length === 0) {
       return (
            <div className="bg-surface-dark p-4 rounded-xl border border-border-dark shadow-md h-72 flex items-center justify-center">
                <p className="text-text-secondary">No packets detected yet.</p>
            </div>
        );
    }

    return (
        <div className="bg-surface-dark p-4 rounded-xl border border-border-dark shadow-md h-72">
          <h3 className="text-md font-semibold text-text-main mb-4">Cumulative Encryption Distribution</h3>
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
                  backgroundColor: '#0D1117', // Dark background
                  borderColor: '#30363D',    // Dark border
                }}
                itemStyle={{ color: '#E6EDF3' }} // Light text
                labelStyle={{ color: '#8B949E' }} // Secondary text color
                formatter={(value, name) => {
                    // Calculate percentage based on cumulative total
                    const percentage = totalCumulative > 0 ? (value / totalCumulative) * 100 : 0;
                    return [`${value} packets (${percentage.toFixed(1)}%)`, name];
                }}
              />
              <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '20px' }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      );
}