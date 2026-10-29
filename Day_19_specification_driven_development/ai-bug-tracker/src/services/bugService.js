
const API_BASE_URL = "http://127.0.0.1:8000/api";

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    let message = `API request failed (${response.status})`;

    try {
      const errorData = await response.json();
      message = errorData.detail || message;
    } catch {
      // Keep the default error message if the response isn't JSON.
    }

    throw new Error(
      typeof message === "string" ? message : JSON.stringify(message)
    );
  }

  return response.json();
}


export function getBugs() {
  return apiRequest("/bugs");
}

export function getBugStats() {
  return apiRequest("/bugs/stats");
}

export function createBug(bugData) {
  return apiRequest("/bugs", {
    method: "POST",
    body: JSON.stringify(bugData),
  });
}

export function updateBug(bugId, updates) {
  return apiRequest(`/bugs/${encodeURIComponent(bugId)}`, {
    method: "PUT",
    body: JSON.stringify(updates),
  });
}
