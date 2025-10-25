// Frontend/src/components/ProtocolBarChart.jsx
import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

// Use the same colors as the Pie Chart for consistency
const COLORS = ['#2DD4BF', '#3B82F6', '#F472B6', '#FBBF24', '#8B5CF6', '#d1d5db', '#22C55E'];

export default function ProtocolBarChart({ data }) {
    if (!data || Object.keys(data).length === 0) {
        return (
            <div className="bg-surface-dark p-4 rounded-xl border border-border-dark shadow-md h-72 flex items-center justify-center">
                <p className="text-text-secondary">No protocol data available.</p>
            </div>
        );
    }

    // Convert data for BarChart format and assign colors
    const chartData = Object.entries(data)
        .map(([name, value], index) => ({
            name,
            value,
            fill: COLORS[index % COLORS.length],
        }))
        // Optional: Sort bars by value descending
        .sort((a, b) => b.value - a.value);

    return (
        <div className="bg-surface-dark p-4 rounded-xl border border-border-dark shadow-md h-72">
          <h3 className="text-md font-semibold text-text-main mb-4">Protocol Distribution (Count)</h3>
          <ResponsiveContainer width="100%" height="85%">
            <BarChart
              data={chartData}
              layout="vertical" // Makes it a horizontal bar chart, often better for category labels
              margin={{
                top: 5,
                right: 30,
                left: 20, // Increased left margin for labels
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#30363D" horizontal={false} />
              {/* Category Axis (Protocols) */}
              <YAxis
                  dataKey="name"
                  type="category"
                  stroke="#8B949E"
                  fontSize={12}
                  tick={{ fill: '#8B949E' }}
                  width={60} // Adjust width as needed for labels
              />
              {/* Value Axis (Packet Count) */}
              <XAxis
                  type="number"
                  stroke="#8B949E"
                  fontSize={12}
                  tick={{ fill: '#8B949E' }}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0D1117',
                  borderColor: '#30363D',
                }}
                itemStyle={{ color: '#E6EDF3' }}
                labelStyle={{ color: '#8B949E' }}
                cursor={{fill: '#161B22'}} // Darker background on hover
              />
              <Bar dataKey="value" name="Packet Count" barSize={20}>
                  {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      );
}