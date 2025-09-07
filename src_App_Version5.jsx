function handleVoiceIntent(intent, transcript) {
  setVoiceBanner(transcript || intent);
  if (intent === "acknowledge") {
    // Find and acknowledge ticket in board state
  } else if (intent === "markReady") {
    // Mark ticket ready
  } else if (intent === "escalate") {
    // Escalate action
  }
  // Add more mappings as needed
}