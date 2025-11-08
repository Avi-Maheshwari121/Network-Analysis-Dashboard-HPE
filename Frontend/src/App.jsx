// Frontend/src/App.jsx
 import { useState } from "react";
 import Sidebar from "./components/Sidebar";
 import Dashboard from "./pages/Dashboard";
 import RawData from "./pages/RawData";
 import ProtocolStatsPage from "./pages/ProtocolStatsPage";
 import TrafficCompositionPage from "./pages/TrafficCompositionPage";
 import GeoMapPage from "./pages/GeoMapPage";
 import useWebSocket from "./hooks/useWebsocket.js";

 const WEBSOCKET_URL = "ws://localhost:8765";

 function App() {
   const [view, setView] = useState("dashboard");

   const {
     wsConnected,
     metrics,
     packets,
     commandStatus,
     loading,
     error,
     sendCommand,
     interfaces,
     metricsHistory,
     protocolDistribution,
     // Protocol Metrics
     tcpMetrics, rtpMetrics, udpMetrics, quicMetrics, dnsMetrics, igmpMetrics,
     // IP Specific Metrics
     ipv4Metrics, ipv6Metrics, ipComposition,
     // Protocol History (Throughput-only)
     tcpHistory, rtpHistory, udpHistory, quicHistory, dnsHistory, igmpHistory,
     ipv4History, ipv6History,
     
     // *** ADDED: Get all KPI objects ***
     tcpKPIs, rtpKPIs, udpKPIs, quicKPIs, dnsKPIs, igmpKPIs,
     ipv4KPIs, ipv6KPIs,
     
     // Full Metrics History
     tcpFullMetricsHistory, rtpFullMetricsHistory,
     ipv4FullMetricsHistory, ipv6FullMetricsHistory,
     udpFullMetricsHistory,
     quicFullMetricsHistory,
     dnsFullMetricsHistory,
     igmpFullMetricsHistory,
     
     // Other states
     captureSummary, summaryStatus,
     encryptionComposition,
     topTalkers,
     geolocations,
   } = useWebSocket(WEBSOCKET_URL);

return (
     <div className="bg-base-dark min-h-screen text-text-main font-sans flex">
       <Sidebar activeView={view} setActiveView={setView} />
       <main className="flex-1 p-8">
         {view === "dashboard" ? (
           <Dashboard
             wsConnected={wsConnected}
             metrics={metrics}
             commandStatus={commandStatus}
             loading={loading}
             error={error}
             sendCommand={sendCommand}
             interfaces={interfaces}
             metricsHistory={metricsHistory}
             protocolDistribution={protocolDistribution}
             captureSummary={captureSummary}
             summaryStatus={summaryStatus}
             topTalkers={topTalkers}
           />
         ) : view === "rawdata" ? (
           <RawData
             wsConnected={wsConnected}
             packets={packets}
             error={error}
             metrics={metrics}
           />
         ) : view === "protocolstats" ? (
            <ProtocolStatsPage
             wsConnected={wsConnected}
             error={error}
             metrics={metrics}
             // Current metrics
             tcpMetrics={tcpMetrics} rtpMetrics={rtpMetrics} udpMetrics={udpMetrics} quicMetrics={quicMetrics} dnsMetrics={dnsMetrics} igmpMetrics={igmpMetrics}
             // Throughput history
             tcpHistory={tcpHistory} rtpHistory={rtpHistory} udpHistory={udpHistory} quicHistory={quicHistory} dnsHistory={dnsHistory} igmpHistory={igmpHistory}
             
             // *** ADDED: Pass all KPI objects down ***
             tcpKPIs={tcpKPIs} rtpKPIs={rtpKPIs} udpKPIs={udpKPIs} quicKPIs={quicKPIs} dnsKPIs={dnsKPIs} igmpKPIs={igmpKPIs}
             
             // Full metrics history
             tcpFullMetricsHistory={tcpFullMetricsHistory}
             rtpFullMetricsHistory={rtpFullMetricsHistory}
             udpFullMetricsHistory={udpFullMetricsHistory}
             quicFullMetricsHistory={quicFullMetricsHistory}
             dnsFullMetricsHistory={dnsFullMetricsHistory}
             igmpFullMetricsHistory={igmpFullMetricsHistory}
           />
         ) : view === "trafficcomposition" ? (
            <TrafficCompositionPage
             wsConnected={wsConnected}
             error={error}
             metrics={metrics}
             ipv4Metrics={ipv4Metrics}
             ipv6Metrics={ipv6Metrics}
             ipComposition={ipComposition}
             ipv4History={ipv4History}
             ipv6History={ipv6History}
             ipv4KPIs={ipv4KPIs} // Pass the KPIs
             ipv6KPIs={ipv6KPIs} // Pass the KPIs
             ipv4FullMetricsHistory={ipv4FullMetricsHistory}
             ipv6FullMetricsHistory={ipv6FullMetricsHistory}
             encryptionComposition={encryptionComposition}
            />
         ) : view === "geomap" ? (
           <GeoMapPage
             wsConnected={wsConnected}
             error={error}
             metrics={metrics}
             geolocations={geolocations}
           />
         ) : null}
       </main>
     </div>
   );
 }

 export default App;