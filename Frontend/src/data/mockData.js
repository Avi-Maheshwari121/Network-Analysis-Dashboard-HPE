export const mockMetrics = {
  throughput_bps: 128000000,
  latency_ms_avg: 32.1,
  packet_loss_percent: 0.07,
  jitter_ms: 2.1,
};

export const mockPackets = Array.from({ length: 50 }, (_, i) => ({
  id: 3031 + i,
  time: `4.559803${i.toString().padStart(2, '0')}`,
  source: i % 2 === 0 ? '74.125.159.76' : '192.168.0.114',
  destination: i % 2 === 0 ? '192.168.0.114' : '74.125.159.76',
  protocol: i % 3 === 0 ? 'TCP' : 'UDP',
  length: 1392,
  info: `Len=${1350 + i}`,
}));
