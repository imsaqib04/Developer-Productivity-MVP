import React from "react";

export default function InterpretationPanel({ patternHint, text }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>What this means</h2>
        <span className="badge">{patternHint}</span>
      </div>
      <p className="body-text">{text}</p>
    </section>
  );
}
