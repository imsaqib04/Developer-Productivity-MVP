const API_BASE="https://developer-productivity-mvp-backned.onrender.com";
async function apiGet(path) {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  return response.json();
}

export function getDevelopers() {
  return apiGet("api/developers/");
}

export function getManagers() {
  return apiGet("api/managers/");
}

export function getMonths() {
  return apiGet("api/months/");
}

export function getIcInsight(developerId, month) {
  return apiGet(`api/insights/ic/?developer_id=${developerId}&month=${month}`);
}

export function getManagerSummary(managerId, month) {
  return apiGet(`api/insights/manager/?manager_id=${managerId}&month=${month}`);
}
