import { useEffect, useState } from "react";
import { RefreshCw } from "lucide-react";
import { api } from "./api.js";

export default function LogsPage() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState("all");

  const load = () => {
    setError("");
    api.logs().then(setData).catch((e) => setError(e.message));
  };
  useEffect(load, []);

  const rows = (data?.rows || []).filter((r) => filter === "all" || r.mode === filter);

  return (
    <section className="panel">
      <div className="panel-title-row">
        <div>
          <h2>Logs</h2>
          <p className="muted">Every answer is saved with its timing and feedback{data ? <> in <code>{data.path}</code></> : ""}.</p>
        </div>
        <div className="log-tools">
          <select value={filter} onChange={(e) => setFilter(e.target.value)} aria-label="Show">
            <option value="all">All answers</option>
            <option value="playground">Playground</option>
            <option value="benchmark">Benchmark</option>
          </select>
          <button className="btn-ghost" onClick={load}><RefreshCw size={15} /> Refresh</button>
        </div>
      </div>
      {error && <p className="error-text">{error}</p>}
      {data && rows.length === 0 && <p className="empty">No answers logged yet. Ask a question in the playground to create the first entry.</p>}
      {rows.length > 0 && (
        <div className="table-scroll">
          <table className="log-table">
            <thead>
              <tr>
                <th>Time</th><th>Source</th><th>Model</th><th>Question</th><th>Answer</th>
                <th>Chunks</th><th>Distance</th><th>Time (s)</th><th>Auto check</th><th>Feedback</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.log_id}>
                  <td className="nowrap">{r.timestamp.replace("T", " ")}</td>
                  <td>{r.mode}</td>
                  <td className="nowrap" title={r.served_by}>{r.model}</td>
                  <td>{r.question}</td>
                  <td className="log-answer" title={r.answer}>{r.answer}</td>
                  <td className="nowrap">{r.retrieved_chunk_ids}</td>
                  <td>{r.best_distance}</td>
                  <td>{r.total_seconds}</td>
                  <td className={r.auto_check === "Pass" ? "pass" : r.auto_check === "Fail" ? "fail" : ""}>{r.auto_check || "–"}</td>
                  <td className={r.feedback === "Correct" ? "pass" : r.feedback === "Incorrect" ? "fail" : "muted"}>{r.feedback}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
