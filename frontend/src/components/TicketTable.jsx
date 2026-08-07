import { Link } from "react-router-dom";
import { Empty, PriorityBadge, StatusBadge, formatDate } from "./Ui";

export default function TicketTable({ tickets }) {
  if (!tickets?.length) return <Empty>Keine Tickets für diese Auswahl.</Empty>;

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Ticket</th>
            <th>Objekt</th>
            <th>Priorität</th>
            <th>Status</th>
            <th>Handwerker</th>
            <th>Aktualisiert</th>
          </tr>
        </thead>
        <tbody>
          {tickets.map((ticket) => (
            <tr key={ticket.id}>
              <td>
                <Link className="ticket-link" to={`/admin/tickets/${ticket.id}`}>
                  {ticket.ticket_number} · {ticket.title}
                </Link>
                <small>Gemeldet von {ticket.reported_by}</small>
              </td>
              <td>
                {ticket.property_name}
                <small>{ticket.apartment_label}</small>
              </td>
              <td><PriorityBadge priority={ticket.priority} /></td>
              <td><StatusBadge status={ticket.status} /></td>
              <td>{ticket.contractor_name || "Nicht zugewiesen"}</td>
              <td>{formatDate(ticket.updated_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
