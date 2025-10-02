// avi-maheshwari121/network-analysis-dashboard-hpe/Network-Analysis-Dashboard-HPE-d12cfd16410c6685dd2d171d8840126ca82c0967/Frontend/src/hooks/useWebsocket.js

import { useState, useRef, useEffect } from "react";

const MAX_PACKETS_TO_STORE = 10000;
const MAX_HISTORY_LENGTH = 30; // Number of data points for the charts

export default function useWebSocket(url) {
  const [wsConnected, setWsConnected] = useState(false);
  const [metrics, setMetrics] = useState(null);
  const [packets, setPackets] = useState([]);
  const [streamCount, setStreamCount] = useState(0);
  const [commandStatus, setCommandStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [interfaces, setInterfaces] = useState([]);
  const [metricsHistory, setMetricsHistory] = useState([]);
  const [protocolDistribution, setProtocolDistribution] = useState({});
  const ws = useRef(null);
  const isStopping = useRef(false);

  useEffect(() => {
    ws.current = new WebSocket(url);
    ws.current.onopen = () => setWsConnected(true);
    ws.current.onclose = () => setWsConnected(false);
    ws.current.onerror = () => setError("WebSocket connection error.");

    ws.current.onmessage = ({ data }) => {
      try {
        const msg = JSON.parse(data);
        setError(null);

        if (isStopping.current && msg.metrics?.status === "running") return;
        if (msg.metrics?.status === "stopped") isStopping.current = false;

        switch (msg.type) {
          case "initial_state":
            setMetrics(msg.metrics);
            setPackets(msg.packets || []);
            setInterfaces(msg.interfaces || []);
            setMetricsHistory([]);
            setProtocolDistribution(msg.metrics.protocol_distribution || {});
            break;
          case "interfaces_response":
            setInterfaces(msg.interfaces || []);
            break;
          case "update":
          case "metrics_update":
            setMetrics(msg.metrics);
            setStreamCount(msg.stream_count || 0);
            setProtocolDistribution(msg.metrics.protocol_distribution || {});

            setMetricsHistory(prevHistory => {
              const newEntry = {
                time: new Date().toLocaleTimeString(),
                inbound: parseFloat((msg.metrics.inbound_throughput || 0).toFixed(2)),
                outbound: parseFloat((msg.metrics.outbound_throughput || 0).toFixed(2)),
                latency: parseFloat(msg.metrics.latency.toFixed(1)),
                jitter: parseFloat((msg.metrics.jitter || 0).toFixed(1)),
              };
              const updatedHistory = [...prevHistory, newEntry];
              return updatedHistory.slice(-MAX_HISTORY_LENGTH);
            });

            if (msg.new_packets?.length > 0) {
              setPackets(prev => [...prev, ...msg.new_packets].slice(-MAX_PACKETS_TO_STORE));
            }
            break;
          case "command_response":
            setCommandStatus(msg);
            setLoading(false);
            if (msg.command === "start_capture" && msg.success) {
              isStopping.current = false;
              setMetrics(null);
              setPackets([]);
              setStreamCount(0);
              setMetricsHistory([]);
              setProtocolDistribution({});
            }
            break;
          default:
            break;
        }
      } catch (e) {
        setError("Invalid data received from backend.");
      }
    };

    return () => ws.current?.close();
  }, [url]);

  const sendCommand = (command, payload = {}) => {
    setLoading(true);
    if (command === "stop_capture") {
      isStopping.current = true;
      setMetrics(prev => ({ ...prev, status: "stopped" }));
      setLoading(false);
    }
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify({ command, ...payload }));
    } else {
      setError("Cannot send command: WebSocket is not connected.");
      setLoading(false);
    }
  };

  return {
    wsConnected, metrics, packets, streamCount, commandStatus, loading, error, sendCommand, interfaces, metricsHistory, protocolDistribution,
  };
}