import React from "react";

export default function NextStepsPanel({ steps }) {
  return (
    <section className="panel">
      <h2>Recommended next steps</h2>
      <div className="steps">
        {steps.map((step, index) => (
          <div className="step-card" key={index}>
            <div className="step-number">{index + 1}</div>
            <div>
              <h3>{step.title}</h3>
              <p>{step.description}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
