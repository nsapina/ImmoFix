import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import TicketTable from "../components/TicketTable";
import { ErrorMessage, Loading, PageHeader } from "../components/Ui";
import { PRIORITY_LABELS, STATUS_LABELS } from "../constants";

export default function Tickets() {
  const [tickets, setTickets] = useState(null);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({ search: "", status: "", priority: "" });

  const load = () => {
    setError(null);
    api.tickets(filters).then(setTickets).catch(setError);
  };

  useEffect(load, []);

  function submit(event) {
    event.preventDefault();
    load();
  }

  return (
    <>
      <PageHeader
        title="Tickets"
        subtitle="Alle eingegangenen Reparaturmeldungen verwalten."
        action={
          <Link className="button primary" to="/">
            Meldung erfassen
          </Link>
        }
      />
      <form className="filter-bar" onSubmit={submit}>
        <input
          placeholder="Suche nach Problem oder Person"
          value={filters.search}
          onChange={(event) => setFilters({ ...filters, search: event.target.value })}
        />
        <select
          value={filters.status}
          onChange={(event) => setFilters({ ...filters, status: event.target.value })}
        >
          <option value="">Alle Status</option>
          {Object.entries(STATUS_LABELS).map(([value, label]) => (
            <option key={value} value={value}>{label}</option>
          ))}
        </select>
        <select
          value={filters.priority}
          onChange={(event) => setFilters({ ...filters, priority: event.target.value })}
        >
          <option value="">Alle Prioritäten</option>
          {Object.entries(PRIORITY_LABELS).map(([value, label]) => (
            <option key={value} value={value}>{label}</option>
          ))}
        </select>
        <button className="button" type="submit">Filtern</button>
      </form>
      {error && <ErrorMessage error={error} />}
      {!tickets && !error ? <Loading /> : <TicketTable tickets={tickets || []} />}
    </>
  );
}
