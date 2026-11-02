import { AlertTriangle, Check, CheckCircle2, Clock, Play, RotateCcw, Square, X, XCircle } from "lucide-react";
import { colorFor, finalVerdict, initials, shortName } from "./utils.js";
import BenchmarkSummary from "./BenchmarkSummary.jsx";

export default function BenchmarkPage({ config, active, bench, runBenchmark, stopBenchmark, reviewAnswer }) {
  const running = bench?.status === "running";
  return (
    <>
      <section className="panel bench-bar">
        <div>
          <h2>Benchmark</h2>
          <p className="muted">
            {config.questions.length} test questions from <code>benchmark_questions.json</code>, asked to each selected model.
          </p>
        </div>
        {running ? (
          <button className="btn-ghost" onClick={stopBenchmark}><Square size={15} /> Stop after this question</button>
        ) : (
          <button className="btn-primary" disabled={active.length === 0} onClick={runBenchmark}>
            <Play size={16} /> {bench ? "Run again" : "Run benchmark"} ({active.length} models)
          </button>
        )}
      </section>

      <section className="panel">
        <BenchmarkSummary bench={bench} />
      </section>

      {bench && bench.done > 0 && (
        <section className="panel">
          <h2>Answers by question</h2>
          <p className="muted">
            Pass or Fail comes from the automatic check. If it got an answer wrong, use Correct or Incorrect to
            overrule it; the results above then use your decision. Hover an answer to read it in full.
          </p>
          {bench.reviewError && <p className="error-text">{bench.reviewError}</p>}
          <div className="table-scroll">
            <table className="matrix">
              <thead>
                <tr>
                  <th>Question</th>
                  {bench.lineup.map((m) => (
                    <th key={m.id} style={{ "--model": colorFor(m.id, bench.lineup) }}>
                      <span className="avatar xs">{initials(m)}</span>{shortName(m)}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {bench.questions.map((q, i) => {
                  const run = bench.runs[i];
                  return (
                    <tr key={i}>
                      <th scope="row">
                        {q.question}
                        <span className="muted small">
                          Expects: {q.must_include.map((item) => item.split("|")[0]).join(", ")}
                        </span>
                      </th>
                      {bench.lineup.map((m) => {
                        const r = run?.results.find((x) => x.model === m.id);
                        if (!r) return <td key={m.id} className="muted small">{running && i === bench.done ? "Asking…" : "–"}</td>;
                        if (r.error) {
                          return (
                            <td key={m.id} title={r.error}>
                              <span className="verdict is-error">
                                <AlertTriangle size={15} /> Error
                                <span className="muted small"><Clock size={11} /> {r.seconds.toFixed(1)} s</span>
                              </span>
                              <span className="cell-answer">{r.error}</span>
                            </td>
                          );
                        }
                        const reviewed = r.human === true || r.human === false;
                        const pass = finalVerdict(r) === true;
                        return (
                          <td key={m.id} title={r.answer} className={reviewed ? "is-reviewed" : ""}>
                            <span className={`verdict ${pass ? "is-pass" : "is-fail"}`}>
                              {pass ? <CheckCircle2 size={15} /> : <XCircle size={15} />}
                              {pass ? "Pass" : "Fail"}
                              <span className="verdict-source">{reviewed ? "your review" : "auto"}</span>
                              <span className="muted small"><Clock size={11} /> {r.seconds.toFixed(1)} s</span>
                            </span>
                            <span className="cell-answer">{r.answer}</span>
                            {reviewed && r.human !== r.correct && (
                              <span className="muted small">Auto-check said {r.correct ? "Pass" : "Fail"}</span>
                            )}
                            <span className="review-row">
                              <button
                                className={`review-btn ${r.human === true ? "is-yes" : ""}`}
                                aria-pressed={r.human === true}
                                onClick={() => reviewAnswer(i, m.id, true)}
                              >
                                <Check size={13} /> Correct
                              </button>
                              <button
                                className={`review-btn ${r.human === false ? "is-no" : ""}`}
                                aria-pressed={r.human === false}
                                onClick={() => reviewAnswer(i, m.id, false)}
                              >
                                <X size={13} /> Incorrect
                              </button>
                              {reviewed && (
                                <button className="review-btn undo" onClick={() => reviewAnswer(i, m.id, null)} title="Undo your review and use the auto-check">
                                  <RotateCcw size={13} />
                                  <span className="sr-only">Undo review</span>
                                </button>
                              )}
                            </span>
                          </td>
                        );
                      })}
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>
      )}
    </>
  );
}