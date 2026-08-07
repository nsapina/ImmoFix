import { Navigate, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import Apartments from "./pages/Apartments";
import Contractors from "./pages/Contractors";
import Dashboard from "./pages/Dashboard";
import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import TicketDetail from "./pages/TicketDetail";
import Tickets from "./pages/Tickets";
import TicketSuccess from "./pages/TicketSuccess";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/meldung-erfolgreich/:id" element={<TicketSuccess />} />
      <Route path="/login" element={<LoginPage />} />

      <Route element={<ProtectedRoute />}>
        <Route path="/admin" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="tickets" element={<Tickets />} />
          <Route path="tickets/:id" element={<TicketDetail />} />
          <Route path="apartments" element={<Apartments />} />
          <Route path="contractors" element={<Contractors />} />
        </Route>
      </Route>

      <Route path="/dashboard" element={<Navigate to="/admin" replace />} />
      <Route path="/tickets" element={<Navigate to="/admin/tickets" replace />} />
      <Route path="/apartments" element={<Navigate to="/admin/apartments" replace />} />
      <Route path="/contractors" element={<Navigate to="/admin/contractors" replace />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
