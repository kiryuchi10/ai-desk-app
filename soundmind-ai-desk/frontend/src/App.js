import React, { useState } from "react";
import SpeechToText from "./SpeechToText"; // Import the component below

function App() {
  const [aiResponse, setAiResponse] = useState("");
  const [keywords, setKeywords] = useState("");
  const [transcript, setTranscript] = useState("");

  // Called when user submits recorded text to backend
  const handleTextSubmit = async (text) => {
    try {
      const res = await fetch("http://localhost:5000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });

      const data = await res.json();
      setAiResponse(data.response || "");
      setKeywords(data.keywords || "");
      setTranscript(data.transcribed_text || text);
    } catch (error) {
      console.error("API error:", error);
      setAiResponse("Error connecting to backend.");
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>🎙️ SoundMind AI Desk</h1>
      <SpeechToText onTextSubmit={handleTextSubmit} />

      <div style={{ marginTop: "30px", textAlign: "left" }}>
        <h3>📝 Final Transcript:</h3>
        <p style={{ backgroundColor: "#eee", padding: "10px" }}>{transcript}</p>

        <h3>🔍 Extracted Keywords:</h3>
        <p style={{ backgroundColor: "#ffe0b2", padding: "10px" }}>{keywords}</p>

        <h3>🤖 ChatGPT Response:</h3>
        <p style={{ backgroundColor: "#dcedc8", padding: "10px" }}>{aiResponse}</p>
      </div>
    </div>
  );
}

export default App;
