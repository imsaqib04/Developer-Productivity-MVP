import React, { useEffect, useState } from "react";
import { getManagers, getMonths, getManagerSummary } from "../api/client";
import ManagerSummaryTable from "../components/ManagerSummaryTable";

export default function ManagerView() {
  const [managers, setManagers] = useState([]);
  const [months, setMonths] = useState([]);
  const [selectedManager, setSelectedManager] = useState("");
  const [selectedMonth, setSelectedMonth] = useState("");
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function bootstrap() {
      const [mgrs, availableMonths] = await Promise.all([
        getManagers(),
        getMonths()
      ]);

      setManagers(mgrs);
      setMonths(availableMonths);

      if (mgrs.length) setSelectedManager(mgrs[0].manager_id);
      if (availableMonths.length) setSelectedMonth(availableMonths[availableMonths.length - 1]);
    }

    bootstrap();
  }, []);

  useEffect(() => {
    if (!selectedManager || !selectedMonth) return;

    async function loadSummary() {
      setLoading(true);
      try {
        const data = await getManagerSummary(selectedManager, selectedMonth);
        setSummary(data);
      } finally {
        setLoading(false);
      }
    }

    loadSummary();
  }, [selectedManager, selectedMonth]);

  return (
    <div className="page">
      <div className="selector-bar">
        <div className="field">
          <label>Manager</label>
          <select
            value={selectedManager}
            onChange={(e) => setSelectedManager(e.target.value)}
          >
            {managers.map((manager) => (
              <option key={manager.manager_id} value={manager.manager_id}>
                {manager.manager_name} — {manager.team_name}
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

      {loading && <div className="panel">Loading manager summary...</div>}
      {!loading && summary && <ManagerSummaryTable summary={summary} />}
    </div>
  );
}
