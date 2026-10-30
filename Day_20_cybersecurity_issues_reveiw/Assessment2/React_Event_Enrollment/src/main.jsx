import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { EnrollmentProvider } from "./context/EnrollmentContext";
import "./styles.css";
import App from "./App";

ReactDOM.createRoot(
  document.getElementById("root")
).render(

  <React.StrictMode>

    <BrowserRouter>

      <EnrollmentProvider>

        <App />

      </EnrollmentProvider>

    </BrowserRouter>

  </React.StrictMode>

);