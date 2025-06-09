import React from 'react';

const UploadPDF = ({ onFileSelect }) => (
  <div>
    <label htmlFor="pdfUpload">Upload a PDF:</label>
    <input
      type="file"
      id="pdfUpload"
      accept="application/pdf"
      onChange={e => onFileSelect(e.target.files[0])}
    />
  </div>
);

export default UploadPDF;
