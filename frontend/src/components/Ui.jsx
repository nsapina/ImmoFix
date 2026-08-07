import { PRIORITY_LABELS, STATUS_LABELS } from "../constants";

export function PageHeader({ title, subtitle, action }) {
  return <header className="page-header"><div><h1>{title}</h1>{subtitle && <p>{subtitle}</p>}</div>{action}</header>;
}

export function Loading() { return <div className="state-card">Daten werden geladen …</div>; }
export function Empty({ children = "Keine Daten vorhanden." }) { return <div className="state-card">{children}</div>; }
export function ErrorMessage({ error }) { return <div className="alert error">{error?.message || String(error)}</div>; }
export function SuccessMessage({ children }) { return <div className="alert success">{children}</div>; }

export function StatusBadge({ status }) {
  return <span className={`badge status-${status}`}>{STATUS_LABELS[status] || status}</span>;
}

export function PriorityBadge({ priority }) {
  return <span className={`badge priority-${priority}`}>{PRIORITY_LABELS[priority] || priority}</span>;
}

export function formatDate(value) {
  return value ? new Intl.DateTimeFormat("de-DE", { dateStyle: "medium", timeStyle: "short" }).format(new Date(value)) : "–";
}
