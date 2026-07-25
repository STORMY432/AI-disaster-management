import React from "react";
import "./AnalyticsDashboard.css";

function AnalyticsDashboard({ messages }) {
  // Calculate analytics metrics from the messages array
  const totalQueries = messages.filter((m) => m.role === "ai").length;

  const severityCounts = messages
    .filter((m) => m.role === "ai" && m.severity)
    .reduce((acc, m) => {
      const sev = m.severity.toLowerCase();
      acc[sev] = (acc[sev] || 0) + 1;
      return acc;
    }, {});

  const disasterCounts = messages
    .filter((m) => m.role === "ai" && m.disaster)
    .reduce((acc, m) => {
      const type = m.disaster;
      acc[type] = (acc[type] || 0) + 1;
      return acc;
    }, {});

  return (
    <div className="analytics-dashboard">
      <h2>📈 Disaster Intelligence Dashboard</h2>

      <div className="metrics-grid">
        <div className="metric-card">
          <h3>Total Analyzed</h3>
          <p className="metric-value">{totalQueries}</p>
        </div>

        <div className="metric-card severity-high">
          <h3>High Severity Alerts</h3>
          <p className="metric-value">{severityCounts["high"] || 0}</p>
        </div>

        <div className="metric-card severity-medium">
          <h3>Medium Severity</h3>
          <p className="metric-value">{severityCounts["medium"] || 0}</p>
        </div>

        <div className="metric-card severity-low">
          <h3>Low Severity</h3>
          <p className="metric-value">{severityCounts["low"] || 0}</p>
        </div>
      </div>

      <div className="analytics-breakdown-row">
        <div className="breakdown-box">
          <h4>🌪️ Disaster Type Breakdown</h4>
          {Object.keys(disasterCounts).length === 0 ? (
            <p className="no-data">No active disaster data recorded yet.</p>
          ) : (
            <ul>
              {Object.entries(disasterCounts).map(([type, count], i) => (
                <li key={i}>
                  <span>{type}</span>
                  <span className="badge">{count}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

export default AnalyticsDashboard;