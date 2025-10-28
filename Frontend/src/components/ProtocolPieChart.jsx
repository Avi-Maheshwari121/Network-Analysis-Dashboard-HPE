// src/components/ProtocolPieChart.jsx

import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const COLORS = ['#2DD4BF', '#3B82F6', '#F472B6', '#FBBF24', '#8B5CF6', '#d1d5db', '#22C55E'];

export default function ProtocolPieChart({ data }) {
    if (!data || Object.keys(data).length === 0) {
        return (
            <div className="bg-surface-dark p-4 rounded-xl border border-border-dark shadow-md h-72 flex items-center justify-center">
                <p className="text-text-secondary">No protocol data available.</p>
            </div>
        );
    }

  const chartData = Object.entries(data).map(([name, value], index) => ({
    name,
    value,
    fill: COLORS[index % COLORS.length],
  }));

  return (
    <div className="bg-surface-dark p-4 rounded-xl border border-border-dark shadow-md h-72">
      <h3 className="text-md font-semibold text-text-main mb-4">Cumulative Protocol Distribution</h3>
      <ResponsiveContainer width="100%" height="85%">
        <PieChart margin={{ top: 20 }}>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
            nameKey="name"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.fill} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: '#0D1117',
              borderColor: '#30363D',
            }}
            itemStyle={{ color: '#E6EDF3' }}
            labelStyle={{ color: '#8B949E' }}
          />
          <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '20px' }} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}