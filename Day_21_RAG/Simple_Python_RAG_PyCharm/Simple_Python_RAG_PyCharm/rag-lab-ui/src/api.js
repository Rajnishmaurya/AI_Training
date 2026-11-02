// All calls go to the Python server (11_rag_ui_server.py) through /api.
async function request(path, options = {}) {
  let res;
  try {
    res = await fetch(`/api${path}`, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch {
    throw new Error("Can't reach the Python server. Start it with: python 11_rag_ui_server.py");
  }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    if (res.status >= 500 && !data.detail) {
      throw new Error("Can't reach the Python server. Start it with: python 11_rag_ui_server.py");
    }
    throw new Error(data.detail || `Request failed (${res.status})`);
  }
  return data;
}

export const api = {
  config: () => request("/config"),
  models: () => request("/models"),
  ask: (body) => request("/ask", { method: "POST", body: JSON.stringify(body) }),
  feedback: (body) => request("/feedback", { method: "POST", body: JSON.stringify(body) }),
  logs: () => request("/logs"),
};
