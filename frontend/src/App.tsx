import React from "react";
import LandingPage from "./LandingPage";
import Dashboard from "./Dashboard";
import { useAuth } from "./auth/AuthContext";

export default function App() {
  const { isAuthenticated, user } = useAuth();

  if (!isAuthenticated) {
    return <LandingPage />;
  }

  return <Dashboard user={user} />;
}
