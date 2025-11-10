// Frontend/src/hooks/useWebsocket.js
import { useState, useRef, useEffect } from "react";

const MAX_PACKETS_TO_STORE = 10000;
const MAX_HISTORY_LENGTH = 30; // History length for charts

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
  const [geolocations, setGeolocations] = useState([]);

  // *** ADDED: State to hold KPIs calculated by the BACKEND ***
  const [tcpKPIs, setTcpKPIs] = useState(null);
  const [rtpKPIs, setRtpKPIs] = useState(null);
  const [udpKPIs, setUdpKPIs] = useState(null);
  const [quicKPIs, setQuicKPIs] = useState(null);
  const [ipv4KPIs, setIpv4KPIs] = useState(null);
  const [ipv6KPIs, setIpv6KPIs] = useState(null);
  const [dnsKPIs, setDnsKPIs] = useState(null);
  const [igmpKPIs, setIgmpKPIs] = useState(null);

  // Protocol Specific (Throughput-Only) History
  const [tcpHistory, setTcpHistory] = useState([]);
  const [rtpHistory, setRtpHistory] = useState([]);
  const [udpHistory, setUdpHistory] = useState([]);
  const [quicHistory, setQuicHistory] = useState([]);
  const [ipv4History, setIpv4History] = useState([]);
  const [ipv6History, setIpv6History] = useState([]);
  const [dnsHistory, setDnsHistory] = useState([]);
  const [igmpHistory, setIgmpHistory] = useState([]);

  // Full Protocol Metrics History (includes PPS, latency, jitter, etc.)
  const [tcpFullMetricsHistory, setTcpFullMetricsHistory] = useState([]);
  const [rtpFullMetricsHistory, setRtpFullMetricsHistory] = useState([]);
  const [ipv4FullMetricsHistory, setIpv4FullMetricsHistory] = useState([]);
  const [ipv6FullMetricsHistory, setIpv6FullMetricsHistory] = useState([]);
  const [udpFullMetricsHistory, setUdpFullMetricsHistory] = useState([]);
  const [quicFullMetricsHistory, setQuicFullMetricsHistory] = useState([]);
  const [dnsFullMetricsHistory, setDnsFullMetricsHistory] = useState([]);
  const [igmpFullMetricsHistory, setIgmpFullMetricsHistory] = useState([]);

  const [topTalkers, setTopTalkers] = useState([]);
  const isStopping = useRef(false);

  // AI Summary States
  const [captureSummary, setCaptureSummary] = useState(null);
  const [summaryStatus, setSummaryStatus] = useState('idle');
  
  // *** 1. ADD NEW STATES FOR PERIODIC SUMMARY ***
  const [periodicSummary, setPeriodicSummary] = useState(null); // For the notification
  const [periodicSummaryHistory, setPeriodicSummaryHistory] = useState([]); // For the log

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

        // Initialization checks
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
             isInitialized = true;
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
             
             // Reset all history arrays
             setTcpHistory([]); setRtpHistory([]); setUdpHistory([]);
             setQuicHistory([]); setIpv4History([]); setIpv6History([]);
             setDnsHistory([]); setIgmpHistory([]);
             setTcpFullMetricsHistory([]); setRtpFullMetricsHistory([]);
             setIpv4FullMetricsHistory([]); setIpv6FullMetricsHistory([]);
             setUdpFullMetricsHistory([]);
             setQuicFullMetricsHistory([]);
             setDnsFullMetricsHistory([]);
             setIgmpFullMetricsHistory([]);

             // *** ADDED: Reset KPI states ***
             setTcpKPIs(null); setRtpKPIs(null); setUdpKPIs(null);
             setQuicKPIs(null); setIpv4KPIs(null); setIpv6KPIs(null);
             setDnsKPIs(null); setIgmpKPIs(null);
             
             setTopTalkers(msg.top_talkers || []);
             setCaptureSummary(null); setSummaryStatus('idle');
             setGeolocations([]);
             // *** 2. RESET PERIODIC SUMMARY ON INIT ***
             setPeriodicSummary(null);
             setPeriodicSummaryHistory([]);
            break;

          case "interfaces_response":
            setInterfaces(msg.interfaces || []);
            break;

          case "status_response":
             setMetrics(msg.metrics || null);
             setProtocolDistribution(msg.metrics?.protocol_distribution || {});
            break;

          case "update":
            // Set current metrics
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
            
            // *** ADDED: Set KPI states from backend message ***
            // These keys match what your teammate added to websocket_server.py
            setTcpKPIs(msg.tcp_metrics);
            setRtpKPIs(msg.rtp_metrics);
            setUdpKPIs(msg.udp_metrics);
            setQuicKPIs(msg.quic_metrics);
            setIpv4KPIs(msg.ipv4_metrics);
            setIpv6KPIs(msg.ipv6_metrics);
            setDnsKPIs(msg.dns_metrics);
            setIgmpKPIs(msg.igmp_metrics);

            setTopTalkers(msg.top_talkers || []);

            // Update global metrics history (for Dashboard page)
            if (msg.metrics) {
                setMetricsHistory(prevHistory => {
                  const newEntry = {
                    time: timestamp,
                    inbound: msg.metrics.inbound_throughput || 0,
                    outbound: msg.metrics.outbound_throughput || 0,
                    latency: parseFloat(msg.metrics.latency?.toFixed(1) || 0),
                    jitter: parseFloat((msg.metrics.jitter || 0).toFixed(1)),
                    packets_per_sec: Math.round(msg.metrics.packets_per_second || 0)
                  };
                  return [...prevHistory, newEntry].slice(-MAX_HISTORY_LENGTH);
                });
            }
            
            if (msg.new_geolocations && Array.isArray(msg.new_geolocations) && msg.new_geolocations.length > 0) {
              setGeolocations(prevLocations => {
                const existingIps = new Set(prevLocations.map(l => l.ip));
                const newUniqueLocations = msg.new_geolocations.filter(l => !existingIps.has(l.ip));
                return [...prevLocations, ...newUniqueLocations];
              });
            }

            // Update protocol-specific *throughput-only* history
            const updateProtocolHistory = (setter, metricsData) => {
              if (metricsData && metricsData.hasOwnProperty('inbound_throughput') && metricsData.hasOwnProperty('outbound_throughput')) {
                setter(prev => [
                  ...prev, { 
                    time: timestamp, 
                    inbound_throughput: metricsData.inbound_throughput || 0, 
                    outbound_throughput: metricsData.outbound_throughput || 0 
                  }
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

            // Update *full* metrics history (for PPS, Latency, Jitter charts)
             if (msg.tcp_metrics) {
               setTcpFullMetricsHistory(prev => [
                   ...prev, { time: timestamp, ...msg.tcp_metrics }
               ].slice(-MAX_HISTORY_LENGTH));
             }
             if (msg.rtp_metrics) {
                 setRtpFullMetricsHistory(prev => [
                     ...prev, { time: timestamp, ...msg.rtp_metrics }
                 ].slice(-MAX_HISTORY_LENGTH));
             }
             if (msg.ipv4_metrics) {
               setIpv4FullMetricsHistory(prev => [
                   ...prev, { time: timestamp, ...msg.ipv4_metrics }
               ].slice(-MAX_HISTORY_LENGTH));
             }
             if (msg.ipv6_metrics) {
                 setIpv6FullMetricsHistory(prev => [
                     ...prev, { time: timestamp, ...msg.ipv6_metrics }
                 ].slice(-MAX_HISTORY_LENGTH));
             }
             if (msg.udp_metrics) {
               setUdpFullMetricsHistory(prev => [
                   ...prev, { time: timestamp, ...msg.udp_metrics }
               ].slice(-MAX_HISTORY_LENGTH));
             }
             if (msg.quic_metrics) {
               setQuicFullMetricsHistory(prev => [
                   ...prev, { time: timestamp, ...msg.quic_metrics }
               ].slice(-MAX_HISTORY_LENGTH));
             }
             if (msg.dns_metrics) {
               setDnsFullMetricsHistory(prev => [
                   ...prev, { time: timestamp, ...msg.dns_metrics }
               ].slice(-MAX_HISTORY_LENGTH));
             }
             if (msg.igmp_metrics) {
               setIgmpFullMetricsHistory(prev => [
                   ...prev, { time: timestamp, ...msg.igmp_metrics }
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

          // *** 3. ADD CASE FOR THE NEW MESSAGE TYPE ***
          case "periodic_summary":
            console.log("Received periodic summary:", msg.summary);
            setPeriodicSummary(msg.summary); // Set for notification
            setPeriodicSummaryHistory(prev => [...prev, msg.summary]); // Add to log
            break;

          case "command_response":
            setLoading(false);

            if (msg.command === "stop_capture_ack") {
              // This is the INSTANT "Tshark stopped" message.
              setCommandStatus(msg);
              setMetrics(prev => ({ ...(prev || {}), status: "stopped" })); //to stop the timer immediately
              setTimeout(() => setCommandStatus(null), 1500); // 1.5-second timer

            } else if (msg.command === "start_capture" && !msg.success) {
              // This is the RED "Please wait..." ERROR.
              setCommandStatus(msg);
              setMetrics(prev => ({ ...(prev || {}), status: "stopped" }));
              setTimeout(() => setCommandStatus(null), 5000); // 5-second timer

            } else if (msg.command === "start_capture" && msg.success) {
              // This is the GREEN "Start Capture" success.
              setCommandStatus(msg);
              isStopping.current = false;
              setMetrics(prev => ({ ...(prev || {}), status: "running" }));
              setPackets([]); setMetricsHistory([]); setProtocolDistribution({});
              // Reset all metrics
              setTcpMetrics(null); setRtpMetrics(null); setUdpMetrics(null);
              setQuicMetrics(null); setIpv4Metrics(null); setIpv6Metrics(null);
              setDnsMetrics(null); setIgmpMetrics(null);
              setIpComposition(null); setEncryptionComposition(null);
              
              // Reset all history arrays
              setTcpHistory([]); setRtpHistory([]); setUdpHistory([]);
              setQuicHistory([]); setIpv4History([]); setIpv6History([]);
              setDnsHistory([]); setIgmpHistory([]);
              setTcpFullMetricsHistory([]); setRtpFullMetricsHistory([]);
              setTopTalkers([]);
              setCaptureSummary(null); setSummaryStatus('idle');
              setGeolocations([]);
              // *** 4. RESET PERIODIC SUMMARY ON START ***
              setPeriodicSummary(null);
              setPeriodicSummaryHistory([]);
              setTimeout(() => setCommandStatus(null), 3000); // 3-second timer

            } else if (msg.command === "stop_capture") {
              // This is the FINAL "stop_capture" with the summary.
              // Do NOT show a popup. Just open the modal.
              setMetrics(prev => ({ ...(prev || {}), status: "stopped" }));
              isStopping.current = false;
              if (msg.summary) {
                  setCaptureSummary(msg.summary); setSummaryStatus('ready');
              } else { 
                  setSummaryStatus('idle'); 
              }
            }
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
        // We now expect an immediate 'stop_capture_ack' and a later 'stop_capture'
        setSummaryStatus('loading');
      } else { 
        console.log("Stop cmd sent, but not running."); 
      }
    } else if (command === "start_capture") {
        setLoading(true); setError(null); setCommandStatus(null);
    } else { setLoading(true); }
    ws.current.send(JSON.stringify({ command, ...payload }));
  };

  // *** 5. EXPORT THE NEW HISTORY STATE ***
  return {
    wsConnected, metrics, packets, commandStatus, loading, error, sendCommand, interfaces, metricsHistory, protocolDistribution,
    // Protocol metrics
    tcpMetrics, rtpMetrics, udpMetrics, quicMetrics, ipv4Metrics, ipv6Metrics, dnsMetrics, igmpMetrics, ipComposition,
    // Protocol throughput history (for charts)
    tcpHistory, rtpHistory, udpHistory, quicHistory, ipv4History, ipv6History, dnsHistory, igmpHistory,
    
    // *** CHANGED: Pass through KPI state from backend ***
    tcpKPIs, rtpKPIs, udpKPIs, quicKPIs, ipv4KPIs, ipv6KPIs, dnsKPIs, igmpKPIs,
    
    // Full metrics history (for charts)
    tcpFullMetricsHistory, rtpFullMetricsHistory,
    ipv4FullMetricsHistory, ipv6FullMetricsHistory,
    udpFullMetricsHistory,
    quicFullMetricsHistory,
    dnsFullMetricsHistory,
    igmpFullMetricsHistory,
    
    // AI Summary
    captureSummary, summaryStatus,
    //Encryption Export
    encryptionComposition,
    topTalkers,
    geolocations,
    // Export the new summary states
    periodicSummary, 
    periodicSummaryHistory,
  };
}