import { Bar, BarChart, CartesianGrid, Cell, LabelList, ResponsiveContainer, XAxis, YAxis } from "recharts";
import { Layers, Target, Zap } from "lucide-react";
import { colorFor, initials, pct, secs, shortName, summarize } from "./utils.js";

export default function BenchmarkSummary({ bench, onRun }) {
  const rows = summarize(bench);
  const hasData = bench && bench.done > 0;

  if (!hasData) {
    return (
      <div className="summary-empty">
        <h2>Benchmark results</h2>
        <p className="muted">
          {bench?.status === "running"
            ? "Waiting for the first question to finish…"
            : "No results yet. Run the benchmark to compare accuracy and speed across your models."}
        </p>
        {onRun && bench?.status !== "running" && (
          <button className="btn-ghost" onClick={onRun}>Set up a benchmark run</button>
        )}
      </div>
    );
  }

  const ranked = rows.filter((r) => r.accuracy !== null);
  const best = ranked.length ? ranked.reduce((a, b) => (b.accuracy > a.accuracy ? b : a)) : null;
  const latencies = rows.map((r) => r.latency).filter((v) => v !== null);
  const avgLatency = latencies.length ? latencies.reduce((a, b) => a + b, 0) / latencies.length : null;
  const chartData = rows.map((r) => ({
    name: shortName(r.model),
    accuracy: r.accuracy === null ? 0 : Math.round(r.accuracy * 100),
    latency: r.latency === null ? 0 : Number(r.latency.toFixed(2)),
    color: colorFor(r.model.id, bench.lineup),
  }));

  return (
    <div className="summary">
      <h2>Benchmark results</h2>
      <p className="muted">
        {bench.lineup.length} models on {bench.done} of {bench.questions.length} test questions
        {bench.status === "running" ? ", still running" : ""}.
      </p>

      <div className="stats">
        <div className="stat stat-green">
          <Target size={22} />
          <div>
            <span className="stat-label">Best accuracy</span>
            <strong>{best ? pct(best.accuracy) : "–"}</strong>
            <span className="stat-sub">{best ? shortName(best.model) : ""}</span>
          </div>
        </div>
        <div className="stat stat-blue">
          <Zap size={22} />
          <div>
            <span className="stat-label">Average response time</span>
            <strong>{secs(avgLatency)}</strong>
            <span className="stat-sub">across all models</span>
          </div>
        </div>
        <div className="stat stat-violet">
          <Layers size={22} />
          <div>
            <span className="stat-label">Questions</span>
            <strong>{bench.done}</strong>
            <span className="stat-sub">of {bench.questions.length}</span>
          </div>
        </div>
      </div>

      <div className="table-scroll">
        <table className="results-table">
          <thead>
            <tr>
              <th>Model</th>
              <th title="Answers that contain the expected facts">Accuracy</th>
              <th title="Answers that cite a retrieved chunk ID">Cites sources</th>
              <th>Avg. time</th>
              <th title="Requests that failed, e.g. rate limits">Errors</th>
              <th title="Answers whose verdict you set yourself">Reviewed</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.model.id} style={{ "--model": colorFor(r.model.id, bench.lineup) }}>
                <td>
                  <span className="avatar xs">{initials(r.model)}</span>
                  {shortName(r.model)}
                </td>
                <td className={best && r.model.id === best.model.id ? "is-best" : ""}>
                  {pct(r.accuracy)} <span className="muted">({r.correct}/{r.asked})</span>
                </td>
                <td>{pct(r.citeRate)}</td>
                <td>{secs(r.latency)}</td>
                <td className={r.errors ? "has-errors" : ""}>{r.errors}</td>
                <td>{r.reviewed}/{r.answered}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="charts">
        <HBarChart title="Accuracy" data={chartData} dataKey="accuracy" max={100} unit="%" />
        <HBarChart title="Average response time" data={chartData} dataKey="latency" unit=" s" />
      </div>
      <p className="hint">
        Accuracy uses your review where you gave one, otherwise the automatic check for the expected facts. Review
        answers on the Benchmark page.
      </p>
    </div>
  );
}

// Horizontal bars keep long model names readable with five models.
function HBarChart({ title, data, dataKey, max, unit }) {
  return (
    <figure className="chart">
      <figcaption>{title}</figcaption>
      <ResponsiveContainer width="100%" height={44 * data.length + 30}>
        <BarChart data={data} layout="vertical" margin={{ top: 4, right: 48, left: 4, bottom: 0 }}>
          <CartesianGrid horizontal={false} stroke="var(--line)" />
          <XAxis type="number" domain={max ? [0, max] : [0, "auto"]} tick={{ fontSize: 11, fill: "var(--muted)" }}
            tickFormatter={(v) => `${v}${unit.trim() === "%" ? "%" : ""}`} tickLine={false} axisLine={false} />
          <YAxis type="category" dataKey="name" width={120} tick={{ fontSize: 12, fill: "var(--text)" }} tickLine={false} axisLine={false} />
          <Bar dataKey={dataKey} radius={[0, 5, 5, 0]} barSize={20} isAnimationActive={false}>
            {data.map((d) => <Cell key={d.name} fill={d.color} />)}
            <LabelList dataKey={dataKey} position="right" formatter={(v) => `${v}${unit}`}
              style={{ fontSize: 12, fontWeight: 700, fill: "var(--text)" }} />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </figure>
  );
}