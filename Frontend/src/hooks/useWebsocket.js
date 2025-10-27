// Frontend/src/hooks/useWebsocket.js
import { useState, useRef, useEffect, useMemo } from "react";

const MAX_PACKETS_TO_STORE = 10000;
const MAX_HISTORY_LENGTH = 30; // History length for charts

// Helper function to calculate KPIs from history (remains the same)
const calculateThroughputKPIs = (history) => {
  // ... (keep existing implementation)
  if (!history || history.length === 0) {
    return { peakIn: 0, peakOut: 0, avgIn: 0, avgOut: 0 };
  }
  let peakIn = 0;
  let peakOut = 0;
  let sumIn = 0;
  let sumOut = 0;
  history.forEach(entry => {
    const inVal = Number(entry.inbound_throughput || 0);
    const outVal = Number(entry.outbound_throughput || 0);
    peakIn = Math.max(peakIn, inVal);
    peakOut = Math.max(peakOut, outVal);
    sumIn += inVal;
    sumOut += outVal;
  });
  const count = history.length;
  return {
    peakIn: peakIn.toFixed(2),
    peakOut: peakOut.toFixed(2),
    avgIn: (sumIn / count).toFixed(2),
    avgOut: (sumOut / count).toFixed(2),
  };
};


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

  // Protocol Specific Metrics
  const [tcpMetrics, setTcpMetrics] = useState(null);
  const [rtpMetrics, setRtpMetrics] = useState(null);
  const [udpMetrics, setUdpMetrics] = useState(null);
  const [quicMetrics, setQuicMetrics] = useState(null);
  const [ipv4Metrics, setIpv4Metrics] = useState(null);
  const [ipv6Metrics, setIpv6Metrics] = useState(null);
  const [dnsMetrics, setDnsMetrics] = useState(null);
  const [igmpMetrics, setIgmpMetrics] = useState(null);
  const [ipComposition, setIpComposition] = useState(null);
  const [encryptionComposition, setEncryptionComposition] = useState(null);

  // Protocol Specific History
  const [tcpHistory, setTcpHistory] = useState([]);
  const [rtpHistory, setRtpHistory] = useState([]);
  const [udpHistory, setUdpHistory] = useState([]);
  const [quicHistory, setQuicHistory] = useState([]);
  const [ipv4History, setIpv4History] = useState([]);
  const [ipv6History, setIpv6History] = useState([]);
  const [dnsHistory, setDnsHistory] = useState([]);
  const [igmpHistory, setIgmpHistory] = useState([]);

  // Full Protocol Metrics History
  const [tcpFullMetricsHistory, setTcpFullMetricsHistory] = useState([]);
  const [rtpFullMetricsHistory, setRtpFullMetricsHistory] = useState([]);

  // *** NEW: State for Top Talkers ***
  const [topTalkers, setTopTalkers] = useState([]);

  const isStopping = useRef(false);

  // AI Summary States
  const [captureSummary, setCaptureSummary] = useState(null);
  const [summaryStatus, setSummaryStatus] = useState('idle');

  useEffect(() => {
    let isInitialized = false;
    ws.current = new WebSocket(url);

    ws.current.onopen = () => {
      console.log('WebSocket CONNECTED - Waiting for initial_state');
      setWsConnected(true);
      setError(null);
       if (ws.current?.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({ command: "get_interfaces" }));
            ws.current.send(JSON.stringify({ command: "get_status" }));
       }
    };
    ws.current.onclose = () => {
      console.log('WebSocket DISCONNECTED');
      setWsConnected(false);
       setMetrics(prev => ({ ...(prev || {}), status: "stopped" }));
    };
    ws.current.onerror = (event) => {
        console.error("WebSocket error observed:", event);
        setError("WebSocket connection error. Is the backend running?");
        setWsConnected(false);
    };

    ws.current.onmessage = ({ data }) => {
      try {
        const msg = JSON.parse(data);
        setError(null);

        // Initialization checks (allow initial interfaces/status)
        if (!isInitialized && msg.type === 'initial_state') {
             console.log('=== Received initial_state ==='); isInitialized = true;
        } else if (!isInitialized && msg.type === 'interfaces_response') { console.log('Received interfaces before initial_state');
        } else if (!isInitialized && msg.type === 'status_response') {
             console.log('Received status before initial_state'); setMetrics(msg.metrics || null);
        } else if (!isInitialized && msg.type !== 'update') { console.warn(`Received ${msg.type} before explicit initial_state, processing...`); }

        // Stopping logic
        if (isStopping.current && msg.metrics?.status === "running" && msg.type === 'update') { console.log("Ignoring update..."); return; }
        if (msg.metrics?.status === "stopped") {
            setMetrics(prev => ({ ...(prev || {}), status: "stopped" }));
            if (isStopping.current) { console.log("Backend confirmed stopped."); isStopping.current = false; }
        }

        const timestamp = new Date().toLocaleTimeString();

        switch (msg.type) {
          case "initial_state":
             isInitialized = true; // Ensure flag is set
             setMetrics(msg.metrics || null);
             setPackets(msg.packets || []);
             setInterfaces(msg.interfaces || interfaces);
             setMetricsHistory([]);
             setProtocolDistribution(msg.metrics?.protocol_distribution || {});
             setCommandStatus(null);
             setTcpMetrics(msg.tcp_metrics || null);
             setRtpMetrics(msg.rtp_metrics || null);
             setUdpMetrics(msg.udp_metrics || null);
             setQuicMetrics(msg.quic_metrics || null);
             setIpv4Metrics(msg.ipv4_metrics || null);
             setIpv6Metrics(msg.ipv6_metrics || null);
             setDnsMetrics(msg.dns_metrics || null);
             setIgmpMetrics(msg.igmp_metrics || null);
             setIpComposition(msg.ip_composition || null);
             setEncryptionComposition(msg.encryption_composition || null);
             setTcpHistory([]); setRtpHistory([]); setUdpHistory([]);
             setQuicHistory([]); setIpv4History([]); setIpv6History([]);
             setDnsHistory([]); setIgmpHistory([]);
             setTcpFullMetricsHistory([]); setRtpFullMetricsHistory([]);
             // *** NEW: Reset Top Talkers on initial state ***
             setTopTalkers(msg.top_talkers || []);
             setCaptureSummary(null); setSummaryStatus('idle');
             isStopping.current = false;
            break;

          case "interfaces_response":
            setInterfaces(msg.interfaces || []);
            break;

          case "status_response":
             setMetrics(msg.metrics || null);
             setProtocolDistribution(msg.metrics?.protocol_distribution || {});
            break;

          case "update":
            setMetrics(msg.metrics);
            setProtocolDistribution(msg.metrics.protocol_distribution || {});
            setTcpMetrics(msg.tcp_metrics);
            setRtpMetrics(msg.rtp_metrics);
            setUdpMetrics(msg.udp_metrics);
            setQuicMetrics(msg.quic_metrics);
            setIpv4Metrics(msg.ipv4_metrics);
            setIpv6Metrics(msg.ipv6_metrics);
            setDnsMetrics(msg.dns_metrics);
            setIgmpMetrics(msg.igmp_metrics);
            setIpComposition(msg.ip_composition);
            setEncryptionComposition(msg.encryption_composition);
            // *** NEW: Update Top Talkers ***
            setTopTalkers(msg.top_talkers || []);

            // Update global metrics history
            if (msg.metrics) {
                setMetricsHistory(prevHistory => {
                  const newEntry = {
                    time: timestamp,
                    inbound: parseFloat((msg.metrics.inbound_throughput || 0).toFixed(2)),
                    outbound: parseFloat((msg.metrics.outbound_throughput || 0).toFixed(2)),
                    latency: parseFloat(msg.metrics.latency?.toFixed(1) || 0),
                    jitter: parseFloat((msg.metrics.jitter || 0).toFixed(1)),
                  };
                  return [...prevHistory, newEntry].slice(-MAX_HISTORY_LENGTH);
                });
            }

            // Update protocol-specific throughput history
            const updateProtocolHistory = (setter, metricsData) => {
              if (metricsData && metricsData.hasOwnProperty('inbound_throughput') && metricsData.hasOwnProperty('outbound_throughput')) {
                const inThrRaw = metricsData.inbound_throughput;
                const outThrRaw = metricsData.outbound_throughput;
                let inThrNum = parseFloat(inThrRaw || 0);
                let outThrNum = parseFloat(outThrRaw || 0);
                inThrNum = isNaN(inThrNum) ? 0 : inThrNum;
                outThrNum = isNaN(outThrNum) ? 0 : outThrNum;
                setter(prev => [
                  ...prev, { time: timestamp, inbound_throughput: inThrNum, outbound_throughput: outThrNum }
                ].slice(-MAX_HISTORY_LENGTH));
              }
            };
            updateProtocolHistory(setTcpHistory, msg.tcp_metrics);
            updateProtocolHistory(setRtpHistory, msg.rtp_metrics);
            updateProtocolHistory(setUdpHistory, msg.udp_metrics);
            updateProtocolHistory(setQuicHistory, msg.quic_metrics);
            updateProtocolHistory(setIpv4History, msg.ipv4_metrics);
            updateProtocolHistory(setIpv6History, msg.ipv6_metrics);
            updateProtocolHistory(setDnsHistory, msg.dns_metrics);
            updateProtocolHistory(setIgmpHistory, msg.igmp_metrics);

            // Update full metrics history for TCP and RTP
             if (msg.tcp_metrics) {
               setTcpFullMetricsHistory(prev => [
                   ...prev, { time: timestamp, ...msg.tcp_metrics, latency: Number(msg.tcp_metrics.latency || 0) }
               ].slice(-MAX_HISTORY_LENGTH));
             }
             if (msg.rtp_metrics) {
                 setRtpFullMetricsHistory(prev => [
                     ...prev, { time: timestamp, ...msg.rtp_metrics, jitter: Number(msg.rtp_metrics.jitter || 0) }
                 ].slice(-MAX_HISTORY_LENGTH));
             }

            // Handle packet updates
            if (msg.new_packets && Array.isArray(msg.new_packets) && msg.new_packets.length > 0) {
              setPackets(prevPackets => {
                  const updatedPackets = [...prevPackets, ...msg.new_packets];
                  return updatedPackets.length > MAX_PACKETS_TO_STORE
                      ? updatedPackets.slice(-MAX_PACKETS_TO_STORE)
                      : updatedPackets;
              });
            }
            break;

          case "command_response":
            setCommandStatus(msg);
            setLoading(false);
            if (msg.command === "start_capture" && msg.success) {
              isStopping.current = false;
              setMetrics(prev => ({ ...(prev || {}), status: "running" }));
              setPackets([]); setMetricsHistory([]); setProtocolDistribution({});
              setTcpMetrics(null); setRtpMetrics(null); setUdpMetrics(null);
              setQuicMetrics(null); setIpv4Metrics(null); setIpv6Metrics(null);
              setDnsMetrics(null); setIgmpMetrics(null);
              setIpComposition(null); setEncryptionComposition(null);
              setTcpHistory([]); setRtpHistory([]); setUdpHistory([]);
              setQuicHistory([]); setIpv4History([]); setIpv6History([]);
              setDnsHistory([]); setIgmpHistory([]);
              setTcpFullMetricsHistory([]); setRtpFullMetricsHistory([]);
              // *** NEW: Reset Top Talkers on start ***
              setTopTalkers([]);
              setCaptureSummary(null); setSummaryStatus('idle');
            } else if (msg.command === "start_capture" && !msg.success) {
                 setMetrics(prev => ({ ...(prev || {}), status: "stopped" }));
            } else if (msg.command === "stop_capture") {
                setMetrics(prev => ({ ...(prev || {}), status: "stopped" }));
                isStopping.current = false;
                 // Don't reset top talkers here, keep the final state
                if (msg.summary) {
                    setCaptureSummary(msg.summary); setSummaryStatus('ready');
                } else { setSummaryStatus('idle'); }
            }
             setTimeout(() => setCommandStatus(null), 5000);
            break;
          default:
             console.log("Received unknown message type:", msg.type);
            break;
        }
      } catch (e) {
        console.error("WebSocket onmessage error:", e);
        if (!(e instanceof DOMException && e.name === 'AbortError') && ws.current?.readyState !== WebSocket.CLOSED) {
           setError(`Error processing message: ${e.message}`);
        }
      }
    };

    return () => {
        if (ws.current) {
            console.log("Cleaning up WebSocket connection.");
            ws.current.close();
            isInitialized = false;
        }
    };
  }, [url]);

  const sendCommand = (command, payload = {}) => {
    // ... (keep existing implementation)
    console.log(`Sending command: ${command}`, payload);
    if (!ws.current || ws.current.readyState !== WebSocket.OPEN) {
      setError("Cannot send command: WebSocket is not connected.");
      setLoading(false);
      if (command === "stop_capture") { setSummaryStatus('idle'); isStopping.current = false; }
      return;
    }
    if (command === "stop_capture") {
      if (metrics?.status === 'running') {
        console.log("Initiating stop capture..."); isStopping.current = true;
        setMetrics(prev => ({ ...prev, status: "stopped" })); setSummaryStatus('loading');
      } else { console.log("Stop cmd sent, but not running."); }
    } else if (command === "start_capture") {
        setLoading(true); setError(null); setCommandStatus(null);
    } else { setLoading(true); }
    ws.current.send(JSON.stringify({ command, ...payload }));
  };

  // Calculate KPIs using useMemo (remains the same)
  const tcpKPIs = useMemo(() => calculateThroughputKPIs(tcpHistory), [tcpHistory]);
  const rtpKPIs = useMemo(() => calculateThroughputKPIs(rtpHistory), [rtpHistory]);
  const udpKPIs = useMemo(() => calculateThroughputKPIs(udpHistory), [udpHistory]);
  const quicKPIs = useMemo(() => calculateThroughputKPIs(quicHistory), [quicHistory]);
  const ipv4KPIs = useMemo(() => calculateThroughputKPIs(ipv4History), [ipv4History]);
  const ipv6KPIs = useMemo(() => calculateThroughputKPIs(ipv6History), [ipv6History]);
  const dnsKPIs = useMemo(() => calculateThroughputKPIs(dnsHistory), [dnsHistory]);
  const igmpKPIs = useMemo(() => calculateThroughputKPIs(igmpHistory), [igmpHistory]);

  return {
    wsConnected, metrics, packets, commandStatus, loading, error, sendCommand, interfaces, metricsHistory, protocolDistribution,
    // Protocol metrics
    tcpMetrics, rtpMetrics, udpMetrics, quicMetrics, ipv4Metrics, ipv6Metrics, dnsMetrics, igmpMetrics, ipComposition,
    // Protocol throughput history and KPIs
    tcpHistory, rtpHistory, udpHistory, quicHistory, ipv4History, ipv6History, dnsHistory, igmpHistory,
    tcpKPIs, rtpKPIs, udpKPIs, quicKPIs, ipv4KPIs, ipv6KPIs, dnsKPIs, igmpKPIs,
    // Full metrics history
    tcpFullMetricsHistory, rtpFullMetricsHistory,
    // AI Summary
    captureSummary, summaryStatus,
    //Encryption Export
    encryptionComposition,
    // *** NEW: Export Top Talkers ***
    topTalkers,
  };
}