export async function transcribeSpeech(audioBuffer: Buffer) {
  // Call real STT (e.g., OpenAI Whisper API, Azure Speech)
  // Example for Whisper:
  // const response = await openai.audio.transcriptions.create({
  //   file: audioBuffer,
  //   model: "whisper-1",
  // });
  // return response.text;
  return "Order ready for pickup";
}