// Each model keeps one colour everywhere: cards, answers, table rows and charts.
export const MODEL_COLORS = ["#3B6FF5", "#1F9D63", "#8A57F2", "#E07A2E", "#D6457A"];

export function colorFor(modelId, lineup) {
  const i = lineup.findIndex((m) => m.id === modelId);
  return MODEL_COLORS[(i < 0 ? 0 : i) % MODEL_COLORS.length];
}

export function shortName(model) {
  const name = model?.name || model?.id || "";
  return name.replace(/\s*\(free\)\s*$/i, "").replace(/^[^:/]+:\s*/, "").replace(/:free$/, "");
}

export function providerName(model) {
  const name = model?.name || "";
  if (name.includes(":")) return name.split(":")[0].trim();
  return (model?.id || "").split("/")[0];
}

export function initials(model) {
  const words = shortName(model).split(/[\s\-_/.]+/).filter((w) => /[a-z0-9]/i.test(w));
  return words.slice(0, 2).map((w) => w[0]).join("").toUpperCase() || "AI";
}

export function formatContext(n) {
  if (!n) return null;
  return n >= 1_000_000 ? `${Math.round(n / 100_000) / 10}M context` : `${Math.round(n / 1000)}K context`;
}

// The final verdict for one answer: your review if you gave one, otherwise the auto-check.
export const finalVerdict = (a) => (a.human === true || a.human === false ? a.human : a.correct);

// Turn the raw benchmark answers into one row of numbers per model.
export function summarize(bench) {
  if (!bench) return [];
  return bench.lineup.map((model) => {
    const answers = bench.runs
      .filter(Boolean)
      .flatMap((run) => run.results.filter((r) => r.model === model.id));
    const ok = answers.filter((a) => !a.error);
    const correct = ok.filter((a) => finalVerdict(a) === true).length;
    const reviewed = ok.filter((a) => a.human === true || a.human === false).length;
    const latency = ok.length ? ok.reduce((s, a) => s + a.seconds, 0) / ok.length : null;
    return {
      model,
      asked: answers.length,
      correct,
      reviewed,
      answered: ok.length,
      accuracy: answers.length ? correct / answers.length : null,
      citeRate: ok.length ? ok.filter((a) => a.cites_source).length / ok.length : null,
      latency,
      errors: answers.length - ok.length,
    };
  });
}

export const pct = (v) => (v === null || v === undefined ? "–" : `${Math.round(v * 100)}%`);
export const secs = (v) => (v === null || v === undefined ? "–" : `${v.toFixed(2)} s`);