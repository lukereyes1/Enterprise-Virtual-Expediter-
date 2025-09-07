import React, { useState } from "react";
import FastCasualBoard from "./components/FastCasualBoard";
import FineDiningBoard from "./components/FineDiningBoard";
import ChainBoard from "./components/ChainBoard";
import CateringBoard from "./components/CateringBoard";
import VoiceCommandAgent from "./components/VoiceCommandAgent";
import VoiceVisualTwinBanner from "./components/VoiceVisualTwinBanner";
import { AgenticProvider } from "./agentic/AgenticContext";

export default function App() {
  const [mode, setMode] = useState("fastCasual");
  const [voiceBanner, setVoiceBanner] = useState("");

  function handleVoiceIntent(intent, transcript) {
    setVoiceBanner(transcript || intent);
    // Expand intent mapping here
    // e.g., if (intent === "acknowledge") { ... }
  }

  return (
    <AgenticProvider userRole="expo" location="US" kpiData={{}}>
      <div style={{ maxWidth: 1200, margin: "0 auto", padding: 32 }}>
        <VoiceCommandAgent userRole="expo" onIntent={handleVoiceIntent} />
        <VoiceVisualTwinBanner message={voiceBanner} />
        {mode === "fastCasual" && <FastCasualBoard />}
        {mode === "fineDining" && <FineDiningBoard />}
        {mode === "chain" && <ChainBoard />}
        {mode === "catering" && <CateringBoard />}
      </div>
    </AgenticProvider>
  );
}