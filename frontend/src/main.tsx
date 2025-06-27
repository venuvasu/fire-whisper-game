import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "./App";
import Game from "./Game";
import Callback from "./Callback";
import "./tailwind.css";
import CreateCharacterPage from "./CreateCharacterPage";
import CreateSagaPage from "./CreateSagaPage";
import CharacterPage from "./CharacterPage";
import * as amplitude from "@amplitude/analytics-browser";
import {
  EnrichmentPlugin,
  Event,
  BrowserClient,
  BrowserConfig,
} from "@amplitude/analytics-types";
import { AuthProvider, useAuth } from "./auth/AuthContext";
import ProtectedRoute from "./auth/ProtectedRoute";
import GameLoading from "./GameLoading";

const globalMetadataPlugin: EnrichmentPlugin = {
  name: "global-metadata-plugin",
  type: "enrichment",
  setup: async (config: BrowserConfig, client: BrowserClient) => {},
  execute: async (event: Event) => {
    return {
      ...event,
      event_properties: {
        ...event.event_properties,
        environment: window.location.hostname,
      },
    };
  },
};

// Initialize Amplitude analytics unless running on localhost
if (window.location.hostname !== "localhost") {
  amplitude.init("e8fbd42ed1d90d161e89c5b0a8114d87", { autocapture: true });
  amplitude.add(globalMetadataPlugin);
}

const Root = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) return <GameLoading />;

  return (
    <BrowserRouter>
      <Routes>
        {/* Public route */}
        <Route path="/callback" element={<Callback />} />
        <Route path="/*" element={<App />} />

        {/* Protected routes */}
        <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} />}>
          <Route path="/game/:gameid" element={<Game />} />
          <Route path="/createcharacter" element={<CreateCharacterPage />} />
          <Route path="/createsaga/:characterId" element={<CreateSagaPage />} />
          <Route path="/character/:characterId" element={<CharacterPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

ReactDOM.createRoot(document.getElementById("root")!).render(
  <AuthProvider>
    <Root />
  </AuthProvider>
);
