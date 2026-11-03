import { useEffect, useMemo, useState } from "react";
import { Search, X } from "lucide-react";
import { api } from "./api.js";
import { formatContext, providerName, shortName } from "./utils.js";

export default function ModelPicker({ current, max, onClose, onSave }) {
  const [catalog, setCatalog] = useState(null);
  const [error, setError] = useState("");
  const [chosen, setChosen] = useState(current.map((m) => m.id));
  const [query, setQuery] = useState("");

  useEffect(() => {
    api.models().then((d) => setCatalog(d.models)).catch((e) => setError(e.message));
    const onKey = (e) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  const shown = useMemo(() => {
    const q = query.toLowerCase();
    return (catalog || []).filter((m) => `${m.name} ${m.id}`.toLowerCase().includes(q));
  }, [catalog, query]);

  const flip = (id) =>
    setChosen((c) => (c.includes(id) ? c.filter((x) => x !== id) : c.length < max ? [...c, id] : c));

  function save() {
    const byId = Object.fromEntries([...current, ...(catalog || [])].map((m) => [m.id, m]));
    onSave(chosen.map((id) => byId[id]).filter(Boolean));
  }

  return (
    <div className="overlay" onMouseDown={(e) => e.target === e.currentTarget && onClose()}>
      <div className="dialog" role="dialog" aria-modal="true" aria-labelledby="picker-title">
        <div className="dialog-head">
          <div>
            <h2 id="picker-title">Choose models</h2>
            <p className="muted">Free models available on OpenRouter right now. Pick up to {max}.</p>
          </div>
          <button className="icon-btn" onClick={onClose} aria-label="Close">
            <X size={18} />
          </button>
        </div>
        <label className="search">
          <Search size={16} />
          <input autoFocus placeholder="Search models" value={query} onChange={(e) => setQuery(e.target.value)} />
        </label>
        <div className="picker-list">
          {error && <p className="error-text">{error}</p>}
          {!catalog && !error && <p className="muted">Loading the free model list…</p>}
          {shown.map((m) => {
            const isOn = chosen.includes(m.id);
            const full = !isOn && chosen.length >= max;
            return (
              <label key={m.id} className={`picker-row ${full ? "is-full" : ""}`}>
                <input type="checkbox" checked={isOn} disabled={full} onChange={() => flip(m.id)} />
                <span>
                  <strong>{shortName(m)}</strong>
                  <span className="muted small">
                    {providerName(m)}
                    {formatContext(m.context_length) ? `, ${formatContext(m.context_length)}` : ""}
                  </span>
                  <code className="small">{m.id}</code>
                </span>
              </label>
            );
          })}
        </div>
        <div className="dialog-foot">
          <span className="muted">{chosen.length} of {max} chosen</span>
          <button className="btn-ghost" onClick={onClose}>Cancel</button>
          <button className="btn-primary" disabled={chosen.length === 0} onClick={save}>Use these models</button>
        </div>
      </div>
    </div>
  );
}
