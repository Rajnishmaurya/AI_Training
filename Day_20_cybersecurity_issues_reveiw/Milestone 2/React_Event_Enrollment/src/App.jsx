import {
  Navigate,
  Route,
  Routes
} from "react-router-dom";

import Navbar from "./components/Navbar";

import EventsPage from "./pages/EventsPage";

import RegistrationsPage from "./pages/RegistrationsPage";

export default function App() {

  return (

    <div className="app-shell">

      <Navbar />

      <main className="container">

        <Routes>

          <Route
            path="/"
            element={<EventsPage />}
          />

          <Route
            path="/registrations"
            element={<RegistrationsPage />}
          />

          <Route
            path="*"
            element={<Navigate to="/" replace />}
          />

        </Routes>

      </main>

      <footer className="footer">
        Event Enrollment Manager · Community Learning Centre
      </footer>

    </div>

  );

}