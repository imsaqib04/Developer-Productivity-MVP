import React from "react";

export default function MetricCard({ title, value, subtitle, accent = "blue" }) {
  return (
    <div className={`metric-card ${accent}`}>
      <div className="metric-title">{title}</div>
      <div className="metric-value">{value}</div>
      <div className="metric-subtitle">{subtitle}</div>
    </div>
  );
}
