import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../api";
import { ErrorMessage, Loading, PageHeader, PriorityBadge, StatusBadge, formatDate } from "../components/Ui";
import { EVENT_LABELS, PRIORITY_LABELS, STATUS_LABELS } from "../constants";

export default function TicketDetail() {
  const { id } = useParams(); const navigate = useNavigate();
  const [ticket, setTicket] = useState(null); const [events, setEvents] = useState([]); const [contractors, setContractors] = useState([]);
  const [error, setError] = useState(null); const [note, setNote] = useState("");
  const load = () => Promise.all([api.ticket(id), api.events(id), api.contractors()]).then(([t,e,c]) => { setTicket(t); setEvents(e); setContractors(c); }).catch(setError);
  useEffect(() => { load(); }, [id]);
  async function update(field, value) { try { const next = await api.updateTicket(id, { [field]: field === "contractor_id" ? (value ? Number(value) : null) : value }); setTicket(next); setEvents(await api.events(id)); } catch (e) { setError(e); } }
  async function addNote(e) { e.preventDefault(); if (!note.trim()) return; try { await api.addNote(id, { message: note }); setNote(""); setEvents(await api.events(id)); } catch (err) { setError(err); } }
  async function remove() { if (!window.confirm("Ticket wirklich löschen?")) return; try { await api.deleteTicket(id); navigate("/admin/tickets"); } catch (e) { setError(e); } }
  if (error && !ticket) return <ErrorMessage error={error} />; if (!ticket) return <Loading />;
  return <>
    <PageHeader title={`${ticket.ticket_number} · ${ticket.title}`} subtitle={`${ticket.property_name} · ${ticket.apartment_label}`} action={<button className="button danger" onClick={remove}>Löschen</button>} />
    {error && <ErrorMessage error={error} />}
    <div className="detail-grid">
      <section className="panel">
        <div className="panel-heading"><h2>Ticketdaten</h2><div className="badge-row"><PriorityBadge priority={ticket.priority}/><StatusBadge status={ticket.status}/></div></div>
        <dl className="details"><div><dt>Adresse</dt><dd>{ticket.property_address}</dd></div><div><dt>Wohnung</dt><dd>{ticket.apartment_label}</dd></div><div><dt>Gemeldet von</dt><dd>{ticket.reported_by}</dd></div><div><dt>Kontakt</dt><dd>{ticket.reporter_phone || ticket.reporter_email || "–"}</dd></div><div><dt>Erstellt</dt><dd>{formatDate(ticket.created_at)}</dd></div><div><dt>Aktualisiert</dt><dd>{formatDate(ticket.updated_at)}</dd></div></dl>
        <h3>Beschreibung</h3><p className="description">{ticket.description}</p>
        <div className="edit-row">
          <label>Status<select value={ticket.status} onChange={(e) => update("status", e.target.value)}>{Object.entries(STATUS_LABELS).map(([v,l]) => <option key={v} value={v}>{l}</option>)}</select></label>
          <label>Priorität<select value={ticket.priority} onChange={(e) => update("priority", e.target.value)}>{Object.entries(PRIORITY_LABELS).map(([v,l]) => <option key={v} value={v}>{l}</option>)}</select></label>
          <label>Handwerker<select value={ticket.contractor_id || ""} onChange={(e) => update("contractor_id", e.target.value)}><option value="">Nicht zugewiesen</option>{contractors.map(c => <option key={c.id} value={c.id}>{c.name} · {c.specialization}</option>)}</select></label>
        </div>
      </section>
      <section className="panel"><h2>Aktivitätsverlauf</h2>
        <form className="note-form" onSubmit={addNote}><textarea rows="3" placeholder="Interne Notiz hinzufügen …" value={note} onChange={(e) => setNote(e.target.value)} /><button className="button" type="submit">Notiz speichern</button></form>
        <div className="timeline">{events.length ? events.map(event => <article key={event.id}><span className="timeline-dot"/><div><strong>{EVENT_LABELS[event.event_type] || event.event_type}</strong><small>{event.actor} · {formatDate(event.created_at)}</small>{event.data.message && <p>{event.data.message}</p>}{event.data.contractor && <p>Handwerker: {event.data.contractor}</p>}{event.data.changes && <pre>{JSON.stringify(event.data.changes, null, 2)}</pre>}</div></article>) : <p>Noch keine Aktivitäten vorhanden.</p>}</div>
      </section>
    </div>
  </>;
}
