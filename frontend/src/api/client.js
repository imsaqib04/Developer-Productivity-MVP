const API_BASE = "http://127.0.0.1:8000/api";

async function apiGet(path) {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  return response.json();
}

export function getDevelopers() {
  return apiGet("/developers/");
}

export function getManagers() {
  return apiGet("/managers/");
}

export function getMonths() {
  return apiGet("/months/");
}

export function getIcInsight(developerId, month) {
  return apiGet(`/insights/ic/?developer_id=${developerId}&month=${month}`);
}

export function getManagerSummary(managerId, month) {
  return apiGet(`/insights/manager/?manager_id=${managerId}&month=${month}`);
}
