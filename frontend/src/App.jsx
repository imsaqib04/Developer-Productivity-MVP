import React, { useState } from "react";
import IcView from "./views/IcView";
import ManagerView from "./views/ManagerView";

export default function App() {
  const [activeTab, setActiveTab] = useState("ic");

  return (
    <div className="app-shell">
      <header className="hero">
        <h1>Developer Productivity MVP</h1>
        <p>Understand your metrics, what they likely mean, and what to do next.</p>
      </header>

      <div className="tabs">
        <button
          className={activeTab === "ic" ? "tab active" : "tab"}
          onClick={() => setActiveTab("ic")}
        >
          IC View
        </button>
        <button
          className={activeTab === "manager" ? "tab active" : "tab"}
          onClick={() => setActiveTab("manager")}
        >
          Manager View
        </button>
      </div>

      {activeTab === "ic" ? <IcView /> : <ManagerView />}
    </div>
  );
}
