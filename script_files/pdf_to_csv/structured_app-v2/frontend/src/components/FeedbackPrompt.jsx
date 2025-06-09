import React from "react";

const FeedbackPrompt = ({ onConfirm }) => (
  <div>
    <p>Was the extracted result accurate?</p>
    <button onClick={() => onConfirm("yes")}>Yes</button>
    <button onClick={() => onConfirm("no")}>No</button>
  </div>
);

export default FeedbackPrompt;
