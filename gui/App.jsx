import React from "react";
import Sidebar from "./Sidebar";
import CorruptionControlPanel from "./CorruptionControlPanel";
import GlitchLogControlPanel from "./GlitchLogControlPanel";
import "./style.css";
import "./dark_theme.css";

function App() {
  const [currentTab, setCurrentTab] = React.useState("corruption");

  const renderPanel = () => {
    switch (currentTab) {
      case "corruption": return <CorruptionControlPanel />;
      case "logs": return <GlitchLogControlPanel />;
      default: return <CorruptionControlPanel />;
    }
  };

  return (
    <div className="app-container">
      <Sidebar setTab={setCurrentTab} />
      <main>{renderPanel()}</main>
    </div>
  );
}

export default App;
