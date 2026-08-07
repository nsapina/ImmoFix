const API_BASE = import.meta.env.VITE_API_BASE || "/api";
const TOKEN_KEY = "immofix_access_token";

export function getStoredToken() {
  return window.localStorage.getItem(TOKEN_KEY);
}

export function storeToken(token) {
  if (token) window.localStorage.setItem(TOKEN_KEY, token);
  else window.localStorage.removeItem(TOKEN_KEY);
}

async function request(path, options = {}) {
  const { auth = true, token: explicitToken, ...fetchOptions } = options;
  const token = explicitToken || (auth ? getStoredToken() : null);
  const headers = { "Content-Type": "application/json", ...(fetchOptions.headers || {}) };
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(`${API_BASE}${path}`, {
    ...fetchOptions,
    headers,
  });

  if (response.status === 204) return null;
  const body = await response.json().catch(() => ({}));

  if (!response.ok) {
    if (response.status === 401 && auth) {
      storeToken(null);
      window.dispatchEvent(new Event("immofix:unauthorized"));
    }
    const detail = Array.isArray(body.detail)
      ? body.detail.map((item) => item.msg).join(" · ")
      : body.detail;
    const error = new Error(detail || `HTTP ${response.status}`);
    error.status = response.status;
    throw error;
  }
  return body;
}

export const api = {
  login: (data) => request("/auth/login", { method: "POST", body: JSON.stringify(data), auth: false }),
  me: () => request("/auth/me"),

  publicProperties: () => request("/public/properties", { auth: false }),
  publicApartments: (propertyId) => {
    const query = propertyId ? `?property_id=${encodeURIComponent(propertyId)}` : "";
    return request(`/public/apartments${query}`, { auth: false });
  },
  createPublicTicket: (data) => request("/public/tickets", {
    method: "POST",
    body: JSON.stringify(data),
    auth: false,
  }),

  dashboard: () => request("/dashboard"),
  tickets: (params = {}) => {
    const query = new URLSearchParams(
      Object.entries(params).filter(([, value]) => value !== "" && value != null),
    );
    return request(`/tickets${query.size ? `?${query}` : ""}`);
  },
  ticket: (id) => request(`/tickets/${id}`),
  updateTicket: (id, data) => request(`/tickets/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  deleteTicket: (id) => request(`/tickets/${id}`, { method: "DELETE" }),
  events: (id) => request(`/tickets/${id}/events`),
  addNote: (id, data) => request(`/tickets/${id}/events`, { method: "POST", body: JSON.stringify(data) }),
  properties: () => request("/properties"),
  createProperty: (data) => request("/properties", { method: "POST", body: JSON.stringify(data) }),
  apartments: () => request("/apartments"),
  createApartment: (data) => request("/apartments", { method: "POST", body: JSON.stringify(data) }),
  contractors: () => request("/contractors"),
  createContractor: (data) => request("/contractors", { method: "POST", body: JSON.stringify(data) }),
};
