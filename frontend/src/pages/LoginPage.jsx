import { useState } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { ErrorMessage } from "../components/Ui";

export default function LoginPage() {
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  if (user) return <Navigate to="/admin" replace />;

  async function submit(event) {
    event.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await login(form.email.trim(), form.password);
      const destination = location.state?.from?.pathname || "/admin";
      navigate(destination, { replace: true });
    } catch (err) {
      setError(err);
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="login-page">
      <Link className="public-brand login-brand" to="/">
        <span className="brand-mark">IF</span>
        <div>
          <strong>ImmoFix</strong>
          <small>Reparaturservice</small>
        </div>
      </Link>

      <main className="login-card">
        <span className="eyebrow">Interner Bereich</span>
        <h1>Verwaltung anmelden</h1>
        <p>Dieser Bereich ist ausschließlich für autorisierte Mitarbeiter vorgesehen.</p>
        {error && <ErrorMessage error={error} />}
        <form className="login-form" onSubmit={submit}>
          <label>
            E-Mail-Adresse
            <input
              required
              type="email"
              autoComplete="username"
              value={form.email}
              onChange={(event) => setForm({ ...form, email: event.target.value })}
              placeholder="admin@immofix.de"
            />
          </label>
          <label>
            Passwort
            <input
              required
              minLength="8"
              type="password"
              autoComplete="current-password"
              value={form.password}
              onChange={(event) => setForm({ ...form, password: event.target.value })}
              placeholder="Mindestens 8 Zeichen"
            />
          </label>
          <button className="button primary login-submit" disabled={saving}>
            {saving ? "Anmeldung läuft …" : "Anmelden"}
          </button>
        </form>
        <Link className="login-back" to="/">← Zur öffentlichen Meldeseite</Link>
      </main>
    </div>
  );
}
