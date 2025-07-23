import React from "react";

function Sidebar({ setTab }) {
  return (
    <nav className="sidebar">
      <button onClick={() => setTab("corruption")}>Corruption Control</button>
      <button onClick={() => setTab("logs")}>Glitch Logs</button>
    </nav>
  );
}

export default Sidebar;
