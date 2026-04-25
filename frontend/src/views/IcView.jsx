import React, { useEffect, useState } from "react";
import { getDevelopers, getMonths, getIcInsight } from "../api/client";
import MetricsGrid from "../components/MetricsGrid";
import InterpretationPanel from "../components/InterpretationPanel";
import EvidencePanel from "../components/EvidencePanel";
import NextStepsPanel from "../components/NextStepsPanel";

export default function IcView() {
  const [developers, setDevelopers] = useState([]);
  const [months, setMonths] = useState([]);
  const [selectedDeveloper, setSelectedDeveloper] = useState("");
  const [selectedMonth, setSelectedMonth] = useState("");
  const [insight, setInsight] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function bootstrap() {
      const [devs, availableMonths] = await Promise.all([
        getDevelopers(),
        getMonths()
      ]);
      setDevelopers(devs);
      setMonths(availableMonths);

      if (devs.length) setSelectedDeveloper(devs[0].developer_id);
      if (availableMonths.length) setSelectedMonth(availableMonths[availableMonths.length - 1]);
    }
    bootstrap();
  }, []);

  useEffect(() => {
    if (!selectedDeveloper || !selectedMonth) return;

    async function loadInsight() {
      setLoading(true);
      try {
        const data = await getIcInsight(selectedDeveloper, selectedMonth);
        setInsight(data);
      } finally {
        setLoading(false);
      }
    }

    loadInsight();
  }, [selectedDeveloper, selectedMonth]);

  return (
    <div className="page">
      <div className="selector-bar">
        <div className="field">
          <label>Developer</label>
          <select
            value={selectedDeveloper}
            onChange={(e) => setSelectedDeveloper(e.target.value)}
          >
            {developers.map((dev) => (
              <option key={dev.developer_id} value={dev.developer_id}>
                {dev.developer_name} — {dev.team_name}
              </option>
            ))}
          </select>
        </div>

        <div className="field">
          <label>Month</label>
          <select
            value={selectedMonth}
            onChange={(e) => setSelectedMonth(e.target.value)}
          >
            {months.map((month) => (
              <option key={month} value={month}>
                {month}
              </option>
            ))}
          </select>
        </div>
      </div>

      {loading && <div className="panel">Loading insight...</div>}

      {!loading && insight && (
        <>
          <MetricsGrid
            metrics={insight.metrics}
            title={`${insight.developer_name} — ${insight.month}`}
          />
          <InterpretationPanel
            patternHint={insight.pattern_hint}
            text={insight.interpretation}
          />
          <EvidencePanel evidence={insight.evidence} />
          <NextStepsPanel steps={insight.next_steps} />
        </>
      )}
    </div>
  );
}
