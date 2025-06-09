import React, { useState } from "react";
import axios from "axios";

const UploadForm = ({ mode, onPreview }) => {
  const [file, setFile] = useState(null);
  const [dpi, setDpi] = useState(200);

  const handleSubmit = async () => {
    if (!file) {
      alert("Please select a PDF file");
      return;
    }

    const formData = new FormData();
    formData.append("pdf", file);
    formData.append("mode", mode);
    formData.append("dpi", dpi);

    try {
      const res = await axios.post("http://localhost:5000/upload", formData);
      alert("Extraction complete");

      // 🧠 Assume server returns image URL for preview
      if (res.data.preview_url) {
        onPreview(res.data.preview_url);
      }
    } catch (err) {
      console.error("Upload failed", err);
      alert("Extraction failed");
    }
  };

  return (
    <div>
      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <input
        type="number"
        placeholder="DPI (e.g., 200)"
        value={dpi}
        onChange={(e) => setDpi(e.target.value)}
      />
      <br />
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
};

export default UploadForm;
