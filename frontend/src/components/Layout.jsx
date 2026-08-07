import { Link, NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

const links = [
  ["/admin", "Dashboard"],
  ["/admin/tickets", "Tickets"],
  ["/admin/apartments", "Wohnungen"],
  ["/admin/contractors", "Handwerker"],
];

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function signOut() {
    logout();
    navigate("/login", { replace: true });
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <Link className="brand" to="/" aria-label="Zur ImmoFix Startseite">
          <span className="brand-mark">IF</span>
          <div>
            <strong>ImmoFix</strong>
            <small>Property Service</small>
          </div>
        </Link>

        <nav>
          {links.map(([to, label]) => (
            <NavLink
              key={to}
              to={to}
              end={to === "/admin"}
              className={({ isActive }) => (isActive ? "active" : "")}
            >
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-account">
          <div className="sidebar-user">
            <span>{user?.full_name?.slice(0, 1).toUpperCase() || "A"}</span>
            <div>
              <strong>{user?.full_name}</strong>
              <small>{user?.email}</small>
            </div>
          </div>
          <Link className="sidebar-home" to="/">← Zur Meldeseite</Link>
          <button className="sidebar-logout" type="button" onClick={signOut}>Abmelden</button>
        </div>
      </aside>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
