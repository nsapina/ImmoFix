import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../api";
import { ErrorMessage } from "../components/Ui";

const initialForm = {
  property_id: "",
  apartment_id: "",
  reported_by: "",
  reporter_phone: "",
  reporter_email: "",
  description: "",
  is_emergency: false,
};

export default function LandingPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState(initialForm);
  const [properties, setProperties] = useState([]);
  const [apartments, setApartments] = useState([]);
  const [loadingProperties, setLoadingProperties] = useState(true);
  const [loadingApartments, setLoadingApartments] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.publicProperties()
      .then(setProperties)
      .catch(setError)
      .finally(() => setLoadingProperties(false));
  }, []);

  async function change(event) {
    const { name, value, checked, type } = event.target;
    setForm((current) => ({
      ...current,
      [name]: type === "checkbox" ? checked : value,
      ...(name === "property_id" ? { apartment_id: "" } : {}),
    }));

    if (name === "property_id") {
      setApartments([]);
      if (!value) return;
      setLoadingApartments(true);
      setError(null);
      try {
        setApartments(await api.publicApartments(value));
      } catch (err) {
        setError(err);
      } finally {
        setLoadingApartments(false);
      }
    }
  }

  async function submit(event) {
    event.preventDefault();
    setError(null);
    if (!form.reporter_phone.trim() && !form.reporter_email.trim()) {
      setError(new Error("Bitte geben Sie eine Telefonnummer oder E-Mail-Adresse an."));
      return;
    }

    setSaving(true);
    try {
      const ticket = await api.createPublicTicket({
        apartment_id: Number(form.apartment_id),
        reported_by: form.reported_by.trim(),
        reporter_phone: form.reporter_phone.trim() || null,
        reporter_email: form.reporter_email.trim() || null,
        description: form.description.trim(),
        is_emergency: form.is_emergency,
      });

      navigate(`/meldung-erfolgreich/${ticket.id}`, {
        state: { ticketNumber: ticket.ticket_number },
      });
    } catch (err) {
      setError(err);
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="public-page">
      <header className="public-header">
        <Link className="public-brand" to="/">
          <span className="brand-mark">IF</span>
          <div>
            <strong>ImmoFix</strong>
            <small>Reparaturservice</small>
          </div>
        </Link>
        <span className="public-help">Schnell. Einfach. Nachvollziehbar.</span>
      </header>

      <main className="landing-main">
        <section className="landing-copy">
          <span className="eyebrow">Reparatur & Wartung</span>
          <h1>Ein Problem in Ihrer Wohnung?</h1>
          <p>
            Senden Sie uns Ihre Reparaturmeldung in wenigen Schritten. Wir prüfen
            die Anfrage und kümmern uns um die weitere Organisation.
          </p>
          <div className="landing-points">
            <span>✓ Keine Registrierung nötig</span>
            <span>✓ Direkte Weiterleitung an die Verwaltung</span>
            <span>✓ Ticketnummer nach dem Absenden</span>
          </div>
        </section>

        <section className="public-form-card">
          <div className="public-form-heading">
            <span>Neue Meldung</span>
            <h2>Reparatur melden</h2>
            <p>Bitte füllen Sie die wichtigsten Angaben aus.</p>
          </div>

          {error && <ErrorMessage error={error} />}

          <form className="public-form" onSubmit={submit}>
            <label>
              Immobilie / Adresse
              <select
                required
                name="property_id"
                value={form.property_id}
                onChange={change}
                disabled={loadingProperties}
              >
                <option value="">
                  {loadingProperties ? "Wird geladen …" : "Bitte wählen"}
                </option>
                {properties.map((property) => (
                  <option key={property.id} value={property.id}>
                    {property.name} · {property.address}, {property.city}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Wohnung
              <select
                required
                name="apartment_id"
                value={form.apartment_id}
                onChange={change}
                disabled={!form.property_id || loadingApartments}
              >
                <option value="">
                  {!form.property_id
                    ? "Zuerst Immobilie wählen"
                    : loadingApartments
                      ? "Wohnungen werden geladen …"
                      : "Bitte wählen"}
                </option>
                {apartments.map((apartment) => (
                  <option key={apartment.id} value={apartment.id}>
                    Wohnung {apartment.apartment_number}
                    {apartment.floor ? ` · Etage ${apartment.floor}` : ""}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Ihr Name
              <input
                required
                minLength="2"
                name="reported_by"
                autoComplete="name"
                placeholder="Vor- und Nachname"
                value={form.reported_by}
                onChange={change}
              />
            </label>

            <div className="public-contact-grid">
              <label>
                Telefon
                <input
                  name="reporter_phone"
                  autoComplete="tel"
                  placeholder="z. B. +49 170 1234567"
                  value={form.reporter_phone}
                  onChange={change}
                />
              </label>
              <label>
                E-Mail
                <input
                  type="email"
                  name="reporter_email"
                  autoComplete="email"
                  placeholder="name@beispiel.de"
                  value={form.reporter_email}
                  onChange={change}
                />
              </label>
            </div>
            <small className="field-hint">Telefon oder E-Mail ist erforderlich.</small>

            <label>
              Was ist passiert?
              <textarea
                required
                minLength="5"
                rows="6"
                name="description"
                placeholder="Beschreiben Sie das Problem möglichst konkret …"
                value={form.description}
                onChange={change}
              />
            </label>

            <label className="emergency-check">
              <input
                type="checkbox"
                name="is_emergency"
                checked={form.is_emergency}
                onChange={change}
              />
              <span>
                <strong>Es handelt sich um einen Notfall</strong>
                <small>
                  Zum Beispiel Wasserschaden, Stromausfall oder Heizungsausfall im Winter.
                </small>
              </span>
            </label>

            <button className="button primary public-submit" disabled={saving}>
              {saving ? "Meldung wird gesendet …" : "Meldung absenden"}
            </button>
          </form>
        </section>
      </main>

      <Link className="admin-entry" to="/login" aria-label="Verwaltung öffnen">
        <span>⚙</span> Verwaltung
      </Link>
    </div>
  );
}
