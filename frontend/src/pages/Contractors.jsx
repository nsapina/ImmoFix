import { useEffect, useState } from "react";
import { api } from "../api";
import { Empty, ErrorMessage, Loading, PageHeader, SuccessMessage } from "../components/Ui";

const initialForm = {
  name: "",
  company: "",
  phone: "",
  email: "",
  specialization: "",
};

export default function Contractors() {
  const [items, setItems] = useState(null);
  const [form, setForm] = useState(initialForm);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState("");
  const [saving, setSaving] = useState(false);

  async function load() {
    try {
      setItems(await api.contractors());
      setError(null);
    } catch (err) {
      setError(err);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function submit(event) {
    event.preventDefault();
    setSaving(true);
    setError(null);
    setSuccess("");

    try {
      await api.createContractor({
        ...form,
        company: form.company.trim() || null,
        phone: form.phone.trim() || null,
        email: form.email.trim() || null,
      });
      setForm(initialForm);
      setSuccess("Handwerker wurde erfolgreich gespeichert.");
      await load();
    } catch (err) {
      setError(err);
    } finally {
      setSaving(false);
    }
  }

  if (!items && !error) return <Loading />;

  return (
    <>
      <PageHeader
        title="Handwerker"
        subtitle="Externe Dienstleister und Fachgebiete verwalten."
      />
      {error && <ErrorMessage error={error} />}
      {success && <SuccessMessage>{success}</SuccessMessage>}

      <div className="split-grid">
        <section className="panel">
          <h2>Aktive Handwerker</h2>
          {(items || []).length === 0 ? (
            <Empty>Noch keine Handwerker vorhanden.</Empty>
          ) : (
            <div className="card-list">
              {(items || []).map((contractor) => (
                <article key={contractor.id}>
                  <strong>{contractor.name}</strong>
                  <span>
                    {contractor.company || "Selbstständig"} · {contractor.specialization}
                  </span>
                  <small>{contractor.phone || contractor.email || "Keine Kontaktdaten"}</small>
                </article>
              ))}
            </div>
          )}
        </section>

        <section className="panel">
          <h2>Handwerker hinzufügen</h2>
          <form className="stack-form" onSubmit={submit}>
            <label>
              Name
              <input
                required
                minLength="2"
                value={form.name}
                onChange={(event) => setForm({ ...form, name: event.target.value })}
              />
            </label>
            <label>
              Firma
              <input
                value={form.company}
                onChange={(event) => setForm({ ...form, company: event.target.value })}
              />
            </label>
            <label>
              Fachgebiet
              <input
                required
                minLength="2"
                placeholder="z. B. Sanitär"
                value={form.specialization}
                onChange={(event) => setForm({ ...form, specialization: event.target.value })}
              />
            </label>
            <label>
              Telefon
              <input
                value={form.phone}
                onChange={(event) => setForm({ ...form, phone: event.target.value })}
              />
            </label>
            <label>
              E-Mail
              <input
                type="email"
                value={form.email}
                onChange={(event) => setForm({ ...form, email: event.target.value })}
              />
            </label>
            <button className="button primary" disabled={saving}>
              {saving ? "Wird gespeichert …" : "Speichern"}
            </button>
          </form>
        </section>
      </div>
    </>
  );
}
