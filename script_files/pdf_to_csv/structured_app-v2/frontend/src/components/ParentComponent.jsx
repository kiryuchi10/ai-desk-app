import React, { useState } from "react";
import ModelSelector from "./ModelSelector";
import UploadForm from "./UploadForm";
import TablePreview from "./TablePreview";
import FeedbackPrompt from "./FeedbackPrompt";
import "./ParentComponent.css";

const ParentComponent = () => {
  const [mode, setMode] = useState("ocr");
  const [imageSrc, setImageSrc] = useState("");
  const [, setFeedback] = useState("");  // ✅ suppress ESLint if unused

  const handleFeedback = (res) => {
    setFeedback(res);
    console.log("User feedback:", res);
  };

  return (
    <div className="container">
      <h1>Smart PDF Extractor</h1>

      <div className="section">
        <ModelSelector onSelect={setMode} />
      </div>

      <div className="section">
        <UploadForm mode={mode} onPreview={setImageSrc} />
      </div>

      <div className="section">
        <TablePreview imageSrc={imageSrc} />
      </div>

      <div className="section">
        <FeedbackPrompt onConfirm={handleFeedback} />
      </div>
    </div>
  );
};

export default ParentComponent;
