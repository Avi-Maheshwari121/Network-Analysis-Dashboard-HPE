import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Label } from 'recharts';

// A generic chart component that can be reused for different metrics
export default function MetricChart({ data, lines, unit, title }) {
  return (
    <div className="bg-surface-dark p-4 rounded-xl border border-border-dark shadow-md h-72 flex flex-col">
      <h3 className="text-md font-semibold text-text-main mb-4">{title}</h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 5, right: 20, left: 10, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#30363D" />
          <XAxis dataKey="time" stroke="#8B949E" fontSize={12} tick={{ fill: '#8B949E' }} />
          <YAxis stroke="#8B949E" fontSize={12} tick={{ fill: '#8B949E' }} domain={['dataMin', 'dataMax + 2']}>
            <Label value={unit} angle={-90} position="insideLeft" style={{ textAnchor: 'middle', fill: '#8B949E' }} />
          </YAxis>
          <Tooltip
            contentStyle={{
              backgroundColor: '#0D1117',
              borderColor: '#30363D',
              color: '#E6EDF3'
            }}
            labelStyle={{ color: '#8B949E' }}
            itemStyle={{ fontWeight: 'bold' }}
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