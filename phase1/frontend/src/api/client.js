const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";
const API_USERNAME = import.meta.env.VITE_API_USERNAME || "admin";
const API_PASSWORD = import.meta.env.VITE_API_PASSWORD || "admin123";

function authHeader() {
  return `Basic ${btoa(`${API_USERNAME}:${API_PASSWORD}`)}`;
}

export async function apiGet(path) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      Authorization: authHeader()
    }
  });
  return handleResponse(response);
}

export async function apiUpload(dataset, file) {
  const form = new FormData();
  form.append("file", file);

  const response = await fetch(`${API_BASE_URL}/imports/${dataset}`, {
    method: "POST",
    headers: {
      Authorization: authHeader()
    },
    body: form
  });
  return handleResponse(response);
}

async function handleResponse(response) {
  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json") ? await response.json() : await response.text();
  if (!response.ok) {
    const detail = typeof payload === "object" ? payload.detail || JSON.stringify(payload) : payload;
    throw new Error(detail || `Request failed with ${response.status}`);
  }
  return payload;
}
