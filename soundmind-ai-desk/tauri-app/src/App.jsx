import React, { useState } from "react";
import { ReactMic } from "react-mic";

function App() {
  const [recording, setRecording] = useState(false);
  const [response, setResponse] = useState("");
  const [transcript, setTranscript] = useState("");
  const [keywords, setKeywords] = useState("");

  const onStop = async (recordedBlob) => {
    const formData = new FormData();
    formData.append("file", recordedBlob.blob, "recording.wav");

    try {
      const res = await fetch("http://localhost:5000/api/voice", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setTranscript(data.transcribed_text);
      setKeywords(data.keywords);
      setResponse(data.response);
    } catch (err) {
      console.error("Upload failed:", err);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>🎙️ SoundMind AI Desk</h2>

      <ReactMic
        record={recording}
        className="sound-wave"
        onStop={onStop}
        strokeColor="#000000"
        backgroundColor="#FFCDD2"
      />

      <button onClick={() => setRecording(true)}>Start Recording</button>
      <button onClick={() => setRecording(false)}>Stop & Upload</button>

      <div style={{ marginTop: 20 }}>
        <p><strong>Transcript:</strong> {transcript}</p>
        <p><strong>Keywords:</strong> {keywords}</p>
        <p><strong>AI Response:</strong> {response}</p>
      </div>
    </div>
  );
}

export default App;
