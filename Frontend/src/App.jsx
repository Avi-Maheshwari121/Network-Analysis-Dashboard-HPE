// App.jsx

import { useState } from "react";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import RawData from "./pages/RawData";
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
    // --- NEW: Get summary states from hook ---
    captureSummary,
    summaryStatus,
    // --- End of NEW section ---
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
            // --- NEW: Pass summary props down ---
            captureSummary={captureSummary}
            summaryStatus={summaryStatus}
            // --- End of NEW section ---
          />
        ) : (
          <RawData
            wsConnected={wsConnected}
            packets={packets}
            error={error}
            metrics={metrics}
          />
        )}
      </main>
    </div>
  );
}

export default App;