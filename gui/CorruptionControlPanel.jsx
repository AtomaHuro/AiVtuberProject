import React, { useState } from "react";

function CorruptionControlPanel() {
  const [corruptionLevel, setCorruptionLevel] = useState(42);

  return (
    <div className="panel">
      <h2>🧬 Corruption Control</h2>
      <div className="meter">
        <label>Level: {corruptionLevel}</label>
        <progress value={corruptionLevel} max="100" />
      </div>
      <button onClick={() => setCorruptionLevel(c => Math.max(0, c - 10))}>Decay</button>
      <button onClick={() => setCorruptionLevel(c => Math.min(100, c + 10))}>Trigger</button>
    </div>
  );
}

export default CorruptionControlPanel;
