// ModelSelector.jsx
import React from 'react';

const ModelSelector = ({ onSelect }) => {
  const handleChange = (e) => {
    onSelect(e.target.value); // 👈 This line causes the error if onSelect is undefined
  };

  return (
    <select onChange={handleChange}>
      <option value="ocr">OCR</option>
      <option value="table">Table</option>
      <option value="hybrid">Hybrid</option>
    </select>
  );
};

export default ModelSelector;
