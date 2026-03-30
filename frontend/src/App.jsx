import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import "./App.css";

const API = "http://localhost:8000/api";
const PIE_COLORS = ["#3b82f6", "#ef4444"];

function App() {
  const [summary, setSummary] = useState({});
  const [alerts, setAlerts] = useState([]);
  const [riskDistribution, setRiskDistribution] = useState([]);
  const [reasonBreakdown, setReasonBreakdown] = useState([]);
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [lastUpdated, setLastUpdated] = useState("");

  const loadData = async () => {
    try {
      const [summaryRes, alertsRes, riskRes, reasonRes] = await Promise.all([
        axios.get(`${API}/summary`),
        axios.get(`${API}/alerts`),
        axios.get(`${API}/risk-distribution`),
        axios.get(`${API}/reason-breakdown`),
      ]);

      setSummary(summaryRes.data);
      setAlerts(alertsRes.data);
      setRiskDistribution(riskRes.data);
      setReasonBreakdown(reasonRes.data);
      setSelectedAlert((prev) => {
        if (!alertsRes.data?.length) return null;
        if (prev) {
          const found = alertsRes.data.find((a) => a.tx_id === prev.tx_id);
          return found || alertsRes.data[0];
        }
        return alertsRes.data[0];
      });
      setLastUpdated(new Date().toLocaleTimeString());
    } catch (error) {
      console.error("Dashboard load failed:", error);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 4000);
    return () => clearInterval(interval);
  }, []);

  const topReasons = useMemo(
    () => [...reasonBreakdown].sort((a, b) => b.count - a.count).slice(0, 6),
    [reasonBreakdown]
  );

  const suspectRate = useMemo(() => {
    if (!summary.total_transactions) return "0.0";
    return (
      ((summary.suspect_transactions || 0) / summary.total_transactions) *
      100
    ).toFixed(1);
  }, [summary]);

  const pieData = useMemo(() => {
    const suspect = summary.suspect_transactions || 0;
    const total = summary.total_transactions || 0;
    const normal = Math.max(total - suspect, 0);
    return [
      { name: "Normal", value: normal },
      { name: "Suspect", value: suspect },
    ];
  }, [summary]);

  return (
    <div className="page">
      <header className="hero">
        <div>
          <p className="eyebrow">FINANCIAL CRIME MONITORING</p>
          <h1>Bitcoin AML Intelligence Dashboard</h1>
          <p className="subtext">
            Real-time suspicious transaction detection using Kafka, Neo4j,
            FastAPI, and explainable risk scoring.
          </p>
        </div>
        <div className="hero-meta">
          <div className="live-row">
            <span className="live-dot"></span>
            <span>Live stream active</span>
          </div>
          <small>Last updated: {lastUpdated || "--:--:--"}</small>
        </div>
      </header>

      <section className="card-grid">
        <StatCard
          title="Total Transactions"
          value={summary.total_transactions ?? 0}
          subtitle="All ingested transactions"
        />
        <StatCard
          title="Suspect Transactions"
          value={summary.suspect_transactions ?? 0}
          subtitle={`${suspectRate}% flagged as suspicious`}
          danger
        />
        <StatCard
          title="Average Risk Score"
          value={summary.avg_risk_score ?? 0}
          subtitle="Mean explainable score"
        />
        <StatCard
          title="Total Volume"
          value={`$${Number(summary.total_amount ?? 0).toLocaleString()}`}
          subtitle="Observed transaction volume"
        />
      </section>

      <section className="main-grid">
        <div className="panel">
          <div className="panel-header">
            <h2>Risk Score Distribution</h2>
            <span>Suspicious transaction buckets</span>
          </div>
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={riskDistribution}>
                <CartesianGrid strokeDasharray="3 3" stroke="#24415f" />
                <XAxis dataKey="bucket" stroke="#9ab3d1" />
                <YAxis allowDecimals={false} stroke="#9ab3d1" />
                <Tooltip />
                <Bar dataKey="count" fill="#4f8cff" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <h2>Normal vs Suspect Share</h2>
            <span>Pipeline outcome</span>
          </div>
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie
                  data={pieData}
                  dataKey="value"
                  nameKey="name"
                  outerRadius={90}
                  label
                >
                  {pieData.map((entry, index) => (
                    <Cell key={entry.name} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <h2>Top Suspicion Reasons</h2>
            <span>Why alerts were triggered</span>
          </div>
          <div className="reason-list">
            {topReasons.map((item) => (
              <div className="reason-row" key={item.reason}>
                <strong>{formatReason(item.reason)}</strong>
                <span>{item.count}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <h2>Selected Alert Explanation</h2>
            <span>How the system decides</span>
          </div>
          {selectedAlert ? (
            <div className="explain-box">
              <div className="explain-top">
                <div>
                  <p className="mini-label">Transaction ID</p>
                  <h3>{selectedAlert.tx_id}</h3>
                </div>
                <div className="risk-badge">{selectedAlert.risk_score}</div>
              </div>

              <div className="explain-grid">
                <InfoBlock label="Source" value={selectedAlert.source} />
                <InfoBlock label="Target" value={selectedAlert.target} />
                <InfoBlock
                  label="Amount"
                  value={`$${Number(selectedAlert.amount).toLocaleString()}`}
                />
                <InfoBlock label="Timestamp" value={selectedAlert.timestamp} />
              </div>

              <div className="reason-tags">
                {selectedAlert.reasons.map((reason) => (
                  <span className="tag" key={reason}>
                    {formatReason(reason)}
                  </span>
                ))}
              </div>

              <div className="logic-box">
                <strong>Why this was flagged:</strong> the score increased due to one or
                more of these behaviors: high-risk wallet linkage, abnormal transfer
                amount, high transaction velocity, multi-hop layering, or use of a
                newly seen wallet.
              </div>
            </div>
          ) : (
            <p>No suspicious alerts available.</p>
          )}
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <h2>Live Suspicious Alerts</h2>
          <span>Click a row to inspect it</span>
        </div>

        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>TX ID</th>
                <th>Amount</th>
                <th>Risk</th>
                <th>Source</th>
                <th>Target</th>
                <th>Reasons</th>
              </tr>
            </thead>
            <tbody>
              {alerts.map((alert) => (
                <tr
                  key={alert.tx_id}
                  onClick={() => setSelectedAlert(alert)}
                  className={selectedAlert?.tx_id === alert.tx_id ? "active-row" : ""}
                >
                  <td>{alert.tx_id}</td>
                  <td>${Number(alert.amount).toLocaleString()}</td>
                  <td>{alert.risk_score}</td>
                  <td>{alert.source}</td>
                  <td>{alert.target}</td>
                  <td>{alert.reasons.map(formatReason).join(", ")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

function StatCard({ title, value, subtitle, danger = false }) {
  return (
    <div className={`stat-card ${danger ? "danger" : ""}`}>
      <p>{title}</p>
      <h2>{value}</h2>
      <span>{subtitle}</span>
    </div>
  );
}

function InfoBlock({ label, value }) {
  return (
    <div className="info-block">
      <p className="mini-label">{label}</p>
      <strong>{value}</strong>
    </div>
  );
}

function formatReason(reason) {
  return reason.replaceAll("_", " ");
}

export default App;
