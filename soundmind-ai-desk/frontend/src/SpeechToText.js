import React, { useState, useEffect } from "react";
import { ReactMic } from "react-mic";
import SpeechRecognition, { useSpeechRecognition } from "react-speech-recognition";

const SpeechToText = ({ onTextSubmit }) => {
  const [recording, setRecording] = useState(false);
  const [progress, setProgress] = useState(0); // For progress bar
  const { transcript, resetTranscript, browserSupportsSpeechRecognition } = useSpeechRecognition();

  useEffect(() => {
    let timer;
    let progressInterval;

    if (recording) {
      setProgress(0);

      progressInterval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 100) {
            clearInterval(progressInterval);
            return 100;
          }
          return prev + 1;
        });
      }, 50); // 50ms * 100 = 5s

      timer = setTimeout(() => {
        stopRecording();
      }, 5000); // stop after 5s
    }

    return () => {
      clearInterval(progressInterval);
      clearTimeout(timer);
    };
  }, [recording]);

  if (!browserSupportsSpeechRecognition) {
    return <span>❌ Browser doesn't support speech recognition.</span>;
  }

  const startRecording = async () => {
    setRecording(true);
    resetTranscript();
    SpeechRecognition.startListening({ continuous: true });

    try {
      const res = await fetch("http://localhost:5000/start-recording", { method: "POST" });
      if (!res.ok) throw new Error(await res.text());
    } catch (err) {
      console.error("Start error:", err);
    }
  };

  const stopRecording = async () => {
    setRecording(false);
    SpeechRecognition.stopListening();

    try {
      const res = await fetch("http://localhost:5000/stop-recording", { method: "POST" });
      if (!res.ok) throw new Error(await res.text());
    } catch (err) {
      console.error("Stop error:", err);
    }
  };

  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <ReactMic
        record={recording}
        className="sound-wave"
        onStop={() => {}}
        strokeColor="#FF3CAC"
        backgroundColor="#FFF0F5"
        mimeType="audio/wav"
      />

      <div style={{ marginTop: "20px" }}>
        <p><strong>🎧 Transcribed Text:</strong></p>
        <div style={{
          padding: "10px",
          backgroundColor: "#f0f0f0",
          borderRadius: "5px",
          minHeight: "80px"
        }}>
          {transcript}
        </div>
      </div>

      <div style={{
        marginTop: "10px",
        height: "5px",
        backgroundColor: "#ddd",
        borderRadius: "5px",
      }}>
        <div style={{
          width: `${progress}%`,
          height: "100%",
          backgroundColor: "#007bff",
          borderRadius: "5px",
        }} />
      </div>

      <div style={{ display: "flex", justifyContent: "space-between", marginTop: "20px" }}>
        <button onClick={startRecording} disabled={recording} style={{ flex: 1, margin: "0 5px" }}>
          ▶ Start
        </button>
        <button onClick={stopRecording} disabled={!recording} style={{ flex: 1, margin: "0 5px" }}>
          ⏹ Stop
        </button>
        <button onClick={resetTranscript} style={{ flex: 1, margin: "0 5px" }}>
          🔄 Reset
        </button>
        <button onClick={() => onTextSubmit(transcript)} disabled={!transcript} style={{ flex: 1, margin: "0 5px" }}>
          🚀 Submit
        </button>
      </div>
    </div>
  );
};

export default SpeechToText;
