// Frontend/src/App.jsx
 import { useState } from "react";
 import Sidebar from "./components/Sidebar";
 import Dashboard from "./pages/Dashboard";
 import RawData from "./pages/RawData";
 import ProtocolStatsPage from "./pages/ProtocolStatsPage";
 import TrafficCompositionPage from "./pages/TrafficCompositionPage";
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
     // Protocol History & KPIs
     tcpHistory, rtpHistory, udpHistory, quicHistory, dnsHistory, igmpHistory,
     // IP Specific History & KPIs
     ipv4History, ipv6History,
     tcpKPIs, rtpKPIs, udpKPIs, quicKPIs, dnsKPIs, igmpKPIs,
     // IP Specific KPIs
     ipv4KPIs, ipv6KPIs,
     // Full Metrics History
     tcpFullMetricsHistory, rtpFullMetricsHistory,
     // AI Summary states
     captureSummary, summaryStatus,
     encryptionComposition,
     // *** NEW: Get topTalkers from hook ***
     topTalkers,
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
             // *** NEW: Pass topTalkers to Dashboard ***
             topTalkers={topTalkers}
           />
         ) : view === "rawdata" ? (
            // ... (RawData props remain the same)
           <RawData
             wsConnected={wsConnected}
             packets={packets}
             error={error}
             metrics={metrics}
           />
         ) : view === "protocolstats" ? (
            // ... (ProtocolStatsPage props remain the same)
            <ProtocolStatsPage
             wsConnected={wsConnected}
             error={error}
             metrics={metrics}
             tcpMetrics={tcpMetrics} rtpMetrics={rtpMetrics} udpMetrics={udpMetrics} quicMetrics={quicMetrics} dnsMetrics={dnsMetrics} igmpMetrics={igmpMetrics}
             tcpHistory={tcpHistory} rtpHistory={rtpHistory} udpHistory={udpHistory} quicHistory={quicHistory} dnsHistory={dnsHistory} igmpHistory={igmpHistory}
             tcpKPIs={tcpKPIs} rtpKPIs={rtpKPIs} udpKPIs={udpKPIs} quicKPIs={quicKPIs} dnsKPIs={dnsKPIs} igmpKPIs={igmpKPIs}
             tcpFullMetricsHistory={tcpFullMetricsHistory}
             rtpFullMetricsHistory={rtpFullMetricsHistory}
           />
         ) : view === "trafficcomposition" ? (
             // ... (TrafficCompositionPage props remain the same)
            <TrafficCompositionPage
              wsConnected={wsConnected}
              error={error}
              metrics={metrics}
              ipv4Metrics={ipv4Metrics}
              ipv6Metrics={ipv6Metrics}
              ipComposition={ipComposition}
              ipv4History={ipv4History}
              ipv6History={ipv6History}
              ipv4KPIs={ipv4KPIs}
              ipv6KPIs={ipv6KPIs}
              encryptionComposition={encryptionComposition}
            />
         ) : null}
       </main>
     </div>
   );
 }

 export default App;