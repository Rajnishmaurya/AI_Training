import { useState } from "react";
import { ChevronDown, Clock, Gauge, Loader2, MessageSquare, Play, Square, ThumbsDown, ThumbsUp } from "lucide-react";
import { api } from "./api.js";
import { colorFor, initials, shortName } from "./utils.js";
import BenchmarkSummary from "./BenchmarkSummary.jsx";

export default function Playground(props) {
  const [tab, setTab] = useState("ask");
  return (
    <div className="two-col">
      <section className="panel">
        <div className="tabs" role="tablist">
          <button role="tab" aria-selected={tab === "ask"} className={tab === "ask" ? "is-current" : ""} onClick={() => setTab("ask")}>
            <MessageSquare size={17} /> Ask a question
          </button>
          <button role="tab" aria-selected={tab === "bench"} className={tab === "bench" ? "is-current" : ""} onClick={() => setTab("bench")}>
            <Gauge size={17} /> Run benchmark
          </button>
        </div>
        {/* both tabs stay mounted so your question and answers survive a tab switch */}
        <div hidden={tab !== "ask"}><AskTab {...props} /></div>
        <div hidden={tab !== "bench"}><BenchTab {...props} /></div>
      </section>
      <section className="panel">
        <BenchmarkSummary bench={props.bench} compact onRun={() => setTab("bench")} />
      </section>
    </div>
  );
}

function AskTab({ active, lineup }) {
  const [question, setQuestion] = useState("");
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [showSources, setShowSources] = useState(false);

  async function ask() {
    setBusy(true);
    setError("");
    setResult(null);
    try {
      setResult(await api.ask({ question, models: active.map((m) => m.id), mode: "playground" }));
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="tab-body">
      <label className="field-label" htmlFor="question">Your question</label>
      <textarea
        id="question"
        rows={3}
        value={question}
        placeholder="How many annual leave days do employees receive?"
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && (e.ctrlKey || e.metaKey) && !busy && question.trim() && active.length && ask()}
      />
      <button className="btn-primary wide" disabled={busy || !question.trim() || active.length === 0} onClick={ask}>
        {busy ? <Loader2 size={17} className="spin" /> : <Play size={16} />}
        {busy ? `Asking ${active.length} models…` : `Ask ${active.length} selected model${active.length === 1 ? "" : "s"}`}
      </button>
      {active.length === 0 && <p className="hint">Tick at least one model above.</p>}
      {error && <p className="error-text">{error}</p>}

      {result && (
        <div className="answers">
          {result.results.map((r) => (
            <AnswerCard key={r.log_id} result={r} lineup={lineup} />
          ))}
          <div className="sources">
            <button className="sources-toggle" aria-expanded={showSources} onClick={() => setShowSources((s) => !s)}>
              <span>Sources (top {result.chunks.length} chunks, found in {result.retrieval_seconds.toFixed(2)} s)</span>
              <ChevronDown size={18} className={showSources ? "flip" : ""} />
            </button>
            {showSources &&
              result.chunks.map((c) => (
                <div key={c.id} className="chunk">
                  <div className="chunk-head">
                    <code>{c.id}</code>
                    <span className="muted small">cosine distance {c.distance.toFixed(4)}</span>
                  </div>
                  <p>{c.text}</p>
                </div>
              ))}
          </div>
        </div>
      )}
    </div>
  );
}

function AnswerCard({ result, lineup }) {
  const model = lineup.find((m) => m.id === result.model) || { id: result.model, name: result.model };
  const [vote, setVote] = useState(null);
  const [voteError, setVoteError] = useState("");

  async function send(feedback) {
    setVoteError("");
    try {
      await api.feedback({ log_id: result.log_id, feedback });
      setVote(feedback);
    } catch (err) {
      setVoteError(err.message);
    }
  }

  return (
    <article className="answer" style={{ "--model": colorFor(result.model, lineup) }}>
      <header>
        <span className="avatar sm">{initials(model)}</span>
        <strong>{shortName(model)}</strong>
        <span className="time-badge"><Clock size={13} /> {result.seconds.toFixed(2)} s</span>
      </header>
      {result.error ? (
        <p className="answer-error">{result.error}</p>
      ) : (
        <>
          <p className="answer-text">{result.answer}</p>
          {result.served_by && result.served_by !== result.model && (
            <p className="muted small">Answered by {result.served_by}</p>
          )}
          <div className="vote-row">
            <span className="muted small">Was this correct?</span>
            <button className={`vote ${vote === "Correct" ? "is-yes" : ""}`} onClick={() => send("Correct")} aria-pressed={vote === "Correct"}>
              <ThumbsUp size={14} /> Correct
            </button>
            <button className={`vote ${vote === "Incorrect" ? "is-no" : ""}`} onClick={() => send("Incorrect")} aria-pressed={vote === "Incorrect"}>
              <ThumbsDown size={14} /> Incorrect
            </button>
            {vote && <span className="muted small">Saved to the log</span>}
          </div>
          {voteError && <p className="error-text small">{voteError}</p>}
        </>
      )}
    </article>
  );
}

function BenchTab({ config, active, bench, runBenchmark, stopBenchmark }) {
  const running = bench?.status === "running";
  const total = config.questions.length;
  return (
    <div className="tab-body">
      <p className="muted">
        Asks every selected model the {total} test questions and checks each answer against the expected facts in
        <code> benchmark_questions.json</code>.
      </p>
      <ol className="question-list">
        {config.questions.map((q, i) => (
          <li key={i} className={bench && bench.lineup && i < bench.done ? "is-done" : ""}>{q.question}</li>
        ))}
      </ol>
      {running ? (
        <button className="btn-ghost wide" onClick={stopBenchmark}>
          <Square size={15} /> Stop after this question
        </button>
      ) : (
        <button className="btn-primary wide" disabled={active.length === 0} onClick={runBenchmark}>
          <Play size={16} /> Run benchmark ({total} questions × {active.length} models)
        </button>
      )}
      {bench && (
        <div className="progress-wrap">
          <div className="progress" role="progressbar" aria-valuemin={0} aria-valuemax={bench.questions.length} aria-valuenow={bench.done}>
            <span style={{ width: `${(bench.done / bench.questions.length) * 100}%` }} />
          </div>
          <p className="muted small">
            {running && `Question ${bench.done + 1} of ${bench.questions.length}…`}
            {bench.status === "finished" && "Benchmark finished. Results are on the right and on the Benchmark page."}
            {bench.status === "stopped" && `Stopped after ${bench.done} questions.`}
            {bench.status === "failed" && <span className="error-text">{bench.error}</span>}
          </p>
        </div>
      )}
      <p className="hint">Free models are rate-limited, so a full run can take a minute or two.</p>
    </div>
  );
}
