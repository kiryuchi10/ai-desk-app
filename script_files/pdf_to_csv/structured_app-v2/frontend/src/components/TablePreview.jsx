import React from "react";

const TablePreview = ({ imageSrc }) => (
  <div>
    <h3>Preview</h3>
    {imageSrc ? <img src={imageSrc} alt="PDF Preview" style={{ maxWidth: "100%" }} /> : <p>No preview yet.</p>}
  </div>
);

export default TablePreview;
