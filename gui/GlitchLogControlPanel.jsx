import React, { useState, useEffect } from "react";

function GlitchLogControlPanel() {
  const [logs, setLogs] = useState([]);
  const [autoRefresh, setAutoRefresh] = useState(true);

  useEffect(() => {
    if (autoRefresh) {
      const interval = setInterval(() => {
        // Mock refresh logic
        setLogs(prev => [...prev, "New log entry @ " + new Date().toLocaleTimeString()]);
      }, 3000);
      return () => clearInterval(interval);
    }
  }, [autoRefresh]);

  return (
    <div className="panel">
      <h2>📓 Glitch Logs</h2>
      <button onClick={() => setLogs([])}>Clear</button>
      <label>
        <input
          type="checkbox"
          checked={autoRefresh}
          onChange={() => setAutoRefresh(!autoRefresh)}
        />
        Auto Refresh
      </label>
      <div className="log-output">
        {logs.slice().reverse().map((log, i) => <div key={i}>{log}</div>)}
      </div>
    </div>
  );
}

export default GlitchLogControlPanel;
