import React from "react";

export default function EvidencePanel({ evidence }) {
  return (
    <section className="panel">
      <h2>Why you are seeing this</h2>
      <ul className="evidence-list">
        {evidence.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </section>
  );
}
