import React, { useState } from "react";
import ModelSelector from "./ModelSelector";
import UploadForm from "./UploadForm";
import TablePreview from "./TablePreview";
import FeedbackPrompt from "./FeedbackPrompt";

const ParentComponent = () => {
  const [mode, setMode] = useState("ocr");
  const [imageSrc, setImageSrc] = useState("");
  const [feedback, setFeedback] = useState("");

  const handleModeSelect = (selected) => {
    console.log("Selected mode:", selected);
    setMode(selected);
  };

  const handlePreview = (imgUrl) => {
    setImageSrc(imgUrl);
  };

  const handleFeedback = (response) => {
    setFeedback(response);
    console.log("User feedback:", response);
  };

  return (
    <div>
      <h1>Smart PDF Extractor</h1>
      <ModelSelector onSelect={handleModeSelect} />
      <UploadForm mode={mode} onPreview={handlePreview} />
      <TablePreview imageSrc={imageSrc} />
      <FeedbackPrompt onConfirm={handleFeedback} />
    </div>
  );
};

export default ParentComponent;
