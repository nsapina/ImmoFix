import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { api, getStoredToken, storeToken } from "../api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(Boolean(getStoredToken()));

  useEffect(() => {
    let active = true;
    const token = getStoredToken();
    if (!token) {
      setLoading(false);
      return () => { active = false; };
    }

    api.me()
      .then((currentUser) => {
        if (active) setUser(currentUser);
      })
      .catch(() => {
        storeToken(null);
        if (active) setUser(null);
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => { active = false; };
  }, []);

  useEffect(() => {
    function handleUnauthorized() {
      setUser(null);
      setLoading(false);
    }
    window.addEventListener("immofix:unauthorized", handleUnauthorized);
    return () => window.removeEventListener("immofix:unauthorized", handleUnauthorized);
  }, []);

  async function login(email, password) {
    const result = await api.login({ email, password });
    storeToken(result.access_token);
    setUser(result.user);
    return result.user;
  }

  function logout() {
    storeToken(null);
    setUser(null);
  }

  const value = useMemo(() => ({ user, loading, login, logout }), [user, loading]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) throw new Error("useAuth muss innerhalb von AuthProvider verwendet werden");
  return value;
}
