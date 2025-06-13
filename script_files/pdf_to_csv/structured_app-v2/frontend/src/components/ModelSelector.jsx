import React from 'react';

const ModelSelector = ({ onSelect }) => {
  const handleChange = (e) => {
    if (onSelect) {
      onSelect(e.target.value);
    }
  };

  return (
    <select onChange={handleChange} defaultValue="ocr">
      <option value="ocr">OCR</option>
      <option value="cv">CV</option>
      <option value="hybrid">Hybrid</option>
      <option value="tabular">Tabular</option> {/* ✅ Added */}
    </select>
  );
};

export default ModelSelector;
