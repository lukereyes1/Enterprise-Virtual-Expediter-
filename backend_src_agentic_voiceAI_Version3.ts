import { classifyIntent, transcribeSpeech } from "./aiLib";

export async function handleVoiceInput(audioBuffer: Buffer, userRole: string) {
  const transcript = await transcribeSpeech(audioBuffer);
  const intent = classifyIntent(transcript, userRole);
  return { transcript, intent };
}