// avi-maheshwari121/network-analysis-dashboard-hpe/Network-Analysis-Dashboard-HPE-d12cfd16410c6685dd2d171d8840126ca82c0967/Frontend/src/App.jsx

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
    streamCount,
    commandStatus,
    loading,
    error,
    sendCommand,
    interfaces,
    metricsHistory,
    protocolDistribution,
  } = useWebSocket(WEBSOCKET_URL);

  return (
    <div className="bg-base-dark min-h-screen text-text-main font-sans flex">
      <Sidebar activeView={view} setActiveView={setView} />
      <main className="flex-1 p-8">
        {view === "dashboard" ? (
          <Dashboard
            wsConnected={wsConnected}
            metrics={metrics}
            streamCount={streamCount}
            commandStatus={commandStatus}
            loading={loading}
            error={error}
            sendCommand={sendCommand}
            interfaces={interfaces}
            metricsHistory={metricsHistory}
            protocolDistribution={protocolDistribution}
          />
        ) : (
          <RawData
            wsConnected={wsConnected}
            packets={packets}
            error={error}
          />
        )}
      </main>
    </div>
  );
}

export default App;