import { useEffect, useRef, useState } from "react";
import { BarChart3, Check, FileText, Layers, MessageSquare, SlidersHorizontal } from "lucide-react";
import { api } from "./api.js";
import { colorFor, formatContext, initials, providerName, shortName } from "./utils.js";
import Playground from "./Playground.jsx";
import BenchmarkPage from "./BenchmarkPage.jsx";
import LogsPage from "./LogsPage.jsx";
import ModelPicker from "./ModelPicker.jsx";

const PAGES = [
  { id: "playground", label: "Playground", icon: MessageSquare },
  { id: "benchmark", label: "Benchmark", icon: BarChart3 },
  { id: "logs", label: "Logs", icon: FileText },
];

export default function App() {
  const [page, setPage] = useState("playground");
  const [config, setConfig] = useState(null);
  const [loadError, setLoadError] = useState("");
  const [lineup, setLineup] = useState([]); // up to 5 models: {id, name, context_length, on}
  const [pickerOpen, setPickerOpen] = useState(false);
  const [bench, setBench] = useState(null); // {lineup, questions, runs, status, done, error}
  const stopRef = useRef(false);

  useEffect(() => {
    api
      .config()
      .then((cfg) => {
        setConfig(cfg);
        setLineup(cfg.default_models.map((m) => ({ ...m, on: true })));
      })
      .catch((err) => setLoadError(err.message));
  }, []);

  const active = lineup.filter((m) => m.on);
  const toggle = (id) => setLineup((l) => l.map((m) => (m.id === id ? { ...m, on: !m.on } : m)));

  async function runBenchmark() {
    const models = active;
    const questions = config.questions;
    stopRef.current = false;
    setBench({ lineup: models, questions, runs: Array(questions.length).fill(null), status: "running", done: 0, error: "" });
    for (let i = 0; i < questions.length; i++) {
      if (stopRef.current) {
        setBench((b) => ({ ...b, status: "stopped" }));
        return;
      }
      try {
        const run = await api.ask({
          question: questions[i].question,
          models: models.map((m) => m.id),
          mode: "benchmark",
          must_include: questions[i].must_include,
        });
        setBench((b) => {
          const runs = [...b.runs];
          runs[i] = run;
          return { ...b, runs, done: i + 1 };
        });
      } catch (err) {
        setBench((b) => ({ ...b, status: "failed", error: err.message }));
        return;
      }
    }
    setBench((b) => ({ ...b, status: "finished" }));
  }

  // verdict: true = correct, false = incorrect, null = undo (back to the auto-check)
  async function reviewAnswer(questionIndex, modelId, verdict) {
    const result = bench.runs[questionIndex]?.results.find((r) => r.model === modelId);
    if (!result) return;
    setBench((b) => {
      const runs = [...b.runs];
      runs[questionIndex] = {
        ...runs[questionIndex],
        results: runs[questionIndex].results.map((r) => (r.model === modelId ? { ...r, human: verdict } : r)),
      };
      return { ...b, runs, reviewError: "" };
    });
    try {
      await api.feedback({
        log_id: result.log_id,
        feedback: verdict === null ? "Not rated" : verdict ? "Correct" : "Incorrect",
      });
    } catch (err) {
      setBench((b) => ({ ...b, reviewError: `Your review is shown but wasn't saved to the log: ${err.message}` }));
    }
  }

  const shared = {
    config,
    lineup,
    active,
    bench,
    runBenchmark,
    reviewAnswer,
    stopBenchmark: () => (stopRef.current = true),
    goTo: setPage,
  };

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">
          <Layers size={26} strokeWidth={2.2} />
          <span>RAG Lab</span>
        </div>
        <nav>
          {PAGES.map(({ id, label, icon: Icon }) => (
            <button key={id} className={`nav-item ${page === id ? "is-current" : ""}`} onClick={() => setPage(id)}>
              <Icon size={19} />
              {label}
              {id === "benchmark" && bench?.status === "running" && <span className="nav-dot" aria-label="Benchmark running" />}
            </button>
          ))}
        </nav>
        <p className="sidebar-note">Free models via OpenRouter. Answers come only from your documents.</p>
      </aside>

      <main className="main">
        <header className="page-head">
          <div>
            <h1>RAG Playground &amp; Model Benchmark</h1>
            <p>Ask questions about your documents and compare how free models answer them.</p>
          </div>
          {config && (
            <div className="doc-pill" title={config.documents.join("\n")}>
              <FileText size={17} />
              <span>
                {config.documents.length === 0
                  ? "Documents loaded"
                  : config.documents.length === 1
                  ? config.documents[0]
                  : `${config.documents.length} documents`}
              </span>
              <Check size={15} className="doc-ok" />
            </div>
          )}
        </header>

        {loadError && (
          <div className="banner-error">
            <strong>The UI can't load.</strong> {loadError}
          </div>
        )}

        {config && (
          <>
            <section className="panel models-panel">
              <div className="panel-title-row">
                <h2>
                  Models <span className="muted">({active.length} of {lineup.length} selected, up to {config.max_models})</span>
                </h2>
                <button className="btn-ghost" onClick={() => setPickerOpen(true)}>
                  <SlidersHorizontal size={16} /> Change models
                </button>
              </div>
              <div className="model-grid">
                {lineup.map((m) => (
                  <label key={m.id} className={`model-card ${m.on ? "is-on" : ""}`} style={{ "--model": colorFor(m.id, lineup) }}>
                    <input type="checkbox" checked={m.on} onChange={() => toggle(m.id)} />
                    <span className="avatar">{initials(m)}</span>
                    <span className="model-text">
                      <span className="model-name" title={m.id}>{shortName(m)}</span>
                      <span className="model-meta">
                        {providerName(m)}
                        {formatContext(m.context_length) ? `, ${formatContext(m.context_length)}` : ""}
                      </span>
                    </span>
                    <span className="tag">Free</span>
                  </label>
                ))}
                {lineup.length === 0 && (
                  <p className="empty">No models yet. Choose up to five with Change models.</p>
                )}
              </div>
            </section>

            {page === "playground" && <Playground {...shared} />}
            {page === "benchmark" && <BenchmarkPage {...shared} />}
            {page === "logs" && <LogsPage />}
          </>
        )}
      </main>

      {pickerOpen && config && (
        <ModelPicker
          current={lineup}
          max={config.max_models}
          onClose={() => setPickerOpen(false)}
          onSave={(models) => {
            setLineup(models.map((m) => ({ ...m, on: true })));
            setPickerOpen(false);
          }}
        />
      )}
    </div>
  );
}