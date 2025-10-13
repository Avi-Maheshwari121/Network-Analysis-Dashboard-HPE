// avi-maheshwari121/network-analysis-dashboard-hpe/Network-Analysis-Dashboard-HPE-d12cfd16410c6685dd2d171d8840126ca82c0967/Frontend/src/hooks/useWebsocket.js

import { useState, useRef, useEffect } from "react";

const MAX_PACKETS_TO_STORE = 10000;
const MAX_HISTORY_LENGTH = 30;

export default function useWebSocket(url) {
  const [wsConnected, setWsConnected] = useState(false);
  const [metrics, setMetrics] = useState(null);
  const [packets, setPackets] = useState([]);
  const [commandStatus, setCommandStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [interfaces, setInterfaces] = useState([]);
  const [metricsHistory, setMetricsHistory] = useState([]);
  const [protocolDistribution, setProtocolDistribution] = useState({});
  const ws = useRef(null);
  const isStopping = useRef(false);

  // --- NEW: States for AI Summary ---
  const [captureSummary, setCaptureSummary] = useState(null);
  const [summaryStatus, setSummaryStatus] = useState('idle'); // 'idle', 'loading', 'ready'
  // --- End of NEW section ---

  useEffect(() => {
    let isInitialized = false;  
    
    ws.current = new WebSocket(url);
    
    ws.current.onopen = () => {
      console.log('WebSocket CONNECTED - Waiting for initial_state');
      setWsConnected(true);
      setError(null);
    };
    
    ws.current.onclose = () => {
      console.log('WebSocket DISCONNECTED');
      setWsConnected(false);
    };
    
    ws.current.onerror = () => setError("WebSocket connection error.");

    ws.current.onmessage = ({ data }) => {
      try {
        const msg = JSON.parse(data);
        setError(null);

        // IGNORE messages until initialized 
        if (!isInitialized && msg.type !== 'initial_state') {
          console.warn(`IGNORING ${msg.type} - waiting for initial_state`);
          return;
        }

        if (isStopping.current && msg.metrics?.status === "running") return;
        if (msg.metrics?.status === "stopped") isStopping.current = false;

        switch (msg.type) {
          case "initial_state":
            console.log('=== Received initial_state - RESETTING ===');
            isInitialized = true;  // MARK AS INITIALIZED 
            
            setMetrics(msg.metrics || null);
            setPackets(msg.packets || []);
            setInterfaces(msg.interfaces || []);
            setMetricsHistory([]);
            setProtocolDistribution(msg.metrics?.protocol_distribution || {});
            setCommandStatus(null);
            setCaptureSummary(null);
            setSummaryStatus('idle');
            isStopping.current = false;
            break;
          case "interfaces_response":
            setInterfaces(msg.interfaces || []);
            break;
          case "update":
            setMetrics(msg.metrics);
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
              setMetricsHistory([]);
              setProtocolDistribution({});
              // --- NEW: Reset summary on new capture ---
              setCaptureSummary(null);
              setSummaryStatus('idle');
              // --- End of NEW section ---
            }
            // --- NEW: Handle summary from stop_capture response ---
            if (msg.command === "stop_capture" && msg.summary) {
              setCaptureSummary(msg.summary);
              setSummaryStatus('ready');
            } else if (msg.command === "stop_capture") {
              // If stop command is received without a summary, ensure we are not in loading state
              setSummaryStatus('idle');
            }
            // --- End of NEW section ---
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
    // <-- START: UPDATED LOGIC
    if (command === "stop_capture") {
      // Only show the "Generating Summary..." status if a capture is actually running.
      if (metrics?.status === 'running') {
        isStopping.current = true;
        // Optimistically update UI status to "stopped"
        setMetrics(prev => ({ ...prev, status: "stopped" }));
        setSummaryStatus('loading');
      }
      // If not running, still send the command to get the "tshark not running" message
      // from the backend, but DO NOT set summary status to 'loading'.
    } else {
      setLoading(true);
    }
    // <-- END: UPDATED LOGIC

    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify({ command, ...payload }));
    } else {
      setError("Cannot send command: WebSocket is not connected.");
      setLoading(false);
      if (command === "stop_capture") setSummaryStatus('idle'); // Reset if WS not connected
    }
  };

  return {
    wsConnected, metrics, packets, commandStatus, loading, error, sendCommand, interfaces, metricsHistory, protocolDistribution,
    // --- NEW: Export new states ---
    captureSummary, summaryStatus,
    // --- End of NEW section ---
  };
}