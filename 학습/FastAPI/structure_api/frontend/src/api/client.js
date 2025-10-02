const BASE = import.meta.env.VITE_API_BASE_URL || "/api";

async function http(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!res.ok) {
    const msg = await res.text();
    throw new Error(`${res.status} ${res.statusText}: ${msg}`);
  }
  return res.headers.get("content-type")?.includes("application/json")
    ? res.json()
    : res.text();
}

export const runAnalysis = (payload) =>
  http("/analysis/run", { method: "POST", body: JSON.stringify(payload) });

export const getStatus = (jobId) => http(`/analysis/status/${jobId}`);

export const getResult = (jobId) => http(`/analysis/result/${jobId}`);