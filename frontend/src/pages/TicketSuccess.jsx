import { Link, useLocation, useParams } from "react-router-dom";

export default function TicketSuccess() {
  const { id } = useParams();
  const location = useLocation();
  const ticketNumber = location.state?.ticketNumber || `Ticket #${id}`;

  return (
    <div className="success-page">
      <Link className="public-brand success-brand" to="/">
        <span className="brand-mark">IF</span>
        <div>
          <strong>ImmoFix</strong>
          <small>Reparaturservice</small>
        </div>
      </Link>

      <main className="success-card">
        <span className="success-icon">✓</span>
        <span className="eyebrow">Meldung erfolgreich</span>
        <h1>Vielen Dank!</h1>
        <p>
          Ihre Reparaturmeldung wurde übermittelt und wird von der Verwaltung geprüft.
        </p>
        <div className="ticket-number-box">
          <small>Ihre Ticketnummer</small>
          <strong>{ticketNumber}</strong>
        </div>
        <p className="success-note">
          Bitte notieren Sie diese Nummer für spätere Rückfragen.
        </p>
        <Link className="button primary" to="/">
          Neue Meldung erstellen
        </Link>
      </main>
    </div>
  );
}
