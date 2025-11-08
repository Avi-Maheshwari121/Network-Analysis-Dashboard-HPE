// Frontend/src/components/EncryptionCompositionPieChart.jsx
import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const ENCRYPTION_COLORS = {
    Encrypted: '#5e8ccdff', // Blue 
    Unencrypted: '#96d65dff', // Green
};

export default function EncryptionCompositionPieChart({ data }) {
    const encryptedCumulative = data?.encrypted_packets_cumulative || 0;
    const unencryptedCumulative = data?.unencrypted_packets_cumulative || 0;
    const totalCumulative = encryptedCumulative + unencryptedCumulative;

    if (!data || totalCumulative === 0) {
        return (
            <div className="bg-surface-dark p-4 rounded-xl border border-border-dark shadow-md h-full flex items-center justify-center">
                <p className="text-text-secondary">No encryption data available for session.</p>
            </div>
        );
    }

    const chartData = [
        { name: 'Encrypted', value: encryptedCumulative, fill: ENCRYPTION_COLORS.Encrypted },
        { name: 'Unencrypted', value: unencryptedCumulative, fill: ENCRYPTION_COLORS.Unencrypted },
    ].filter(entry => entry.value > 0); 

    if (chartData.length === 0) {
       return (
            <div className="bg-surface-dark p-4 rounded-xl border border-border-dark shadow-md h-full flex items-center justify-center">
                <p className="text-text-secondary">No packets detected yet.</p>
            </div>
        );
    }
    
    // Get percentages for the new stats block
    const encryptedPercent = (data.encrypted_percentage || 0).toFixed(1);
    const unencryptedPercent = (data.unencrypted_percentage || 0).toFixed(1);

    return (
        // *** CHANGED: Removed fixed height, added h-full ***
        <div className="bg-surface-dark p-4 rounded-xl border border-border-dark shadow-md h-full flex flex-col">
          <h3 className="text-md font-semibold text-text-main mb-2">Encryption Distribution</h3>
          
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
                    const percentage = (name === 'Encrypted' ? encryptedPercent : unencryptedPercent);
                    return [`${value.toLocaleString()} packets (${percentage}%)`, name];
                }}
              />
            </PieChart>
          </ResponsiveContainer>

          {/* *** ADDED: New Stats Block (Your Idea) *** */}
          <div className="flex-grow flex justify-around items-center pt-4 border-t border-border-dark">
            <div className="text-center">
              <p className="text-3xl font-bold" style={{ color: ENCRYPTION_COLORS.Encrypted }}>
                {encryptedPercent}%
              </p>
              <p className="text-sm text-text-secondary">Encrypted</p>
            </div>
            <div className="text-center">
              <p className="text-3xl font-bold" style={{ color: ENCRYPTION_COLORS.Unencrypted }}>
                {unencryptedPercent}%
              </p>
              <p className="text-sm text-text-secondary">Unencrypted</p>
            </div>
          </div>

        </div>
      );
}