import React from "react";
import MetricCard from "./MetricCard";

export default function MetricsGrid({ metrics, title }) {
  return (
    <section className="panel">
      <h2>{title}</h2>
      <div className="metrics-grid">
        <MetricCard
          title="Lead Time for Changes"
          value={metrics.avg_lead_time_days ?? "N/A"}
          subtitle="Average PR open → production"
          accent="green"
        />
        <MetricCard
          title="Cycle Time"
          value={metrics.avg_cycle_time_days ?? "N/A"}
          subtitle="Average In Progress → Done"
          accent="blue"
        />
        <MetricCard
          title="Bug Rate"
          value={`${metrics.bug_rate_pct}%`}
          subtitle={`${metrics.escaped_bugs} bug(s) / ${metrics.issues_done} issue(s)`}
          accent={metrics.escaped_bugs > 0 ? "red" : "green"}
        />
        <MetricCard
          title="Deployment Frequency"
          value={metrics.prod_deployments}
          subtitle="Successful prod deployments"
          accent="orange"
        />
        <MetricCard
          title="PR Throughput"
          value={metrics.merged_prs}
          subtitle="Merged PRs this month"
          accent="purple"
        />
      </div>
    </section>
  );
}
