const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

async function parseResponse(response) {
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

export async function getJson(path) {
  const response = await fetch(`${API_BASE_URL}${path}`);
  return parseResponse(response);
}

export async function postJson(path) {
  const response = await fetch(`${API_BASE_URL}${path}`, { method: "POST" });
  return parseResponse(response);
}

export { API_BASE_URL };
