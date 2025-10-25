// Frontend/src/App.jsx
 import { useState } from "react";
 import Sidebar from "./components/Sidebar";
 import Dashboard from "./pages/Dashboard";
 import RawData from "./pages/RawData";
 import ProtocolStatsPage from "./pages/ProtocolStatsPage";
 import TrafficCompositionPage from "./pages/TrafficCompositionPage"; // Import new page
 import useWebSocket from "./hooks/useWebsocket.js";

 const WEBSOCKET_URL = "ws://localhost:8765";

 function App() {
   const [view, setView] = useState("dashboard");

   const {
     wsConnected,
     metrics, // Contains overall packets_per_second now
     packets,
     commandStatus,
     loading,
     error,
     sendCommand,
     interfaces,
     metricsHistory, // Global throughput history
     protocolDistribution,
     // Protocol Metrics
     tcpMetrics,
     rtpMetrics,
     udpMetrics,
     quicMetrics,
     dnsMetrics, // <-- Get DNS
     igmpMetrics, // <-- Get IGMP
     // IP Specific Metrics (for new page)
     ipv4Metrics,
     ipv6Metrics,
     ipComposition, // Includes cumulative counts now
     // Protocol History & KPIs
     tcpHistory,
     rtpHistory,
     udpHistory,
     quicHistory,
     dnsHistory, // <-- Get DNS history
     igmpHistory, // <-- Get IGMP history
     // IP Specific History & KPIs (for new page)
     ipv4History,
     ipv6History,
     tcpKPIs,
     rtpKPIs,
     udpKPIs,
     quicKPIs,
     dnsKPIs, // <-- Get DNS KPIs
     igmpKPIs, // <-- Get IGMP KPIs
     // IP Specific KPIs (for new page)
     ipv4KPIs,
     ipv6KPIs,
     // Full Metrics History
     tcpFullMetricsHistory,
     rtpFullMetricsHistory,
     // AI Summary states
     captureSummary,
     summaryStatus,
   } = useWebSocket(WEBSOCKET_URL);

   return (
     <div className="bg-base-dark min-h-screen text-text-main font-sans flex">
       <Sidebar activeView={view} setActiveView={setView} />
       <main className="flex-1 p-8">
         {view === "dashboard" ? (
           <Dashboard
             wsConnected={wsConnected}
             metrics={metrics} // Pass whole metrics object
             commandStatus={commandStatus}
             loading={loading}
             error={error}
             sendCommand={sendCommand}
             interfaces={interfaces}
             metricsHistory={metricsHistory}
             protocolDistribution={protocolDistribution}
             captureSummary={captureSummary}
             summaryStatus={summaryStatus}
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
             metrics={metrics} // For status banner
             // Pass only non-IP protocol metrics/history/KPIs
             tcpMetrics={tcpMetrics} rtpMetrics={rtpMetrics} udpMetrics={udpMetrics} quicMetrics={quicMetrics} dnsMetrics={dnsMetrics} igmpMetrics={igmpMetrics}
             tcpHistory={tcpHistory} rtpHistory={rtpHistory} udpHistory={udpHistory} quicHistory={quicHistory} dnsHistory={dnsHistory} igmpHistory={igmpHistory}
             tcpKPIs={tcpKPIs} rtpKPIs={rtpKPIs} udpKPIs={udpKPIs} quicKPIs={quicKPIs} dnsKPIs={dnsKPIs} igmpKPIs={igmpKPIs}
             tcpFullMetricsHistory={tcpFullMetricsHistory}
             rtpFullMetricsHistory={rtpFullMetricsHistory}
           />
         ) : view === "trafficcomposition" ? ( // <-- Route for new page
            <TrafficCompositionPage
              wsConnected={wsConnected}
              error={error}
              metrics={metrics} // For status banner
              ipv4Metrics={ipv4Metrics}
              ipv6Metrics={ipv6Metrics}
              ipComposition={ipComposition}
              ipv4History={ipv4History}
              ipv6History={ipv6History}
              ipv4KPIs={ipv4KPIs}
              ipv6KPIs={ipv6KPIs}
            />
         ) : null}
       </main>
     </div>
   );
 }

 export default App;