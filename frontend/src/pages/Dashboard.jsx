import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import TicketTable from "../components/TicketTable";
import { ErrorMessage, Loading, PageHeader } from "../components/Ui";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.dashboard().then(setData).catch(setError);
  }, []);

  if (error) return <ErrorMessage error={error} />;
  if (!data) return <Loading />;

  const stats = [
    ["Offene Tickets", data.open_tickets],
    ["Dringend", data.urgent_tickets],
    ["Ohne Handwerker", data.unassigned_tickets],
    ["Gelöst / geschlossen", data.resolved_tickets],
  ];

  return (
    <>
      <PageHeader
        title="Dashboard"
        subtitle="Interner Überblick über Reparaturen und Wartungsanfragen."
        action={
          <Link className="button primary" to="/">
            Öffentliche Meldeseite
          </Link>
        }
      />
      <section className="stat-grid">
        {stats.map(([label, value]) => (
          <article className="stat-card" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
          </article>
        ))}
      </section>
      <section className="panel">
        <div className="panel-heading">
          <h2>Zuletzt bearbeitet</h2>
          <Link to="/admin/tickets">Alle Tickets</Link>
        </div>
        <TicketTable tickets={data.recent_tickets} />
      </section>
    </>
  );
}
