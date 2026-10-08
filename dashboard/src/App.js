import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Dashboard from "./pages/Dashboard/Dashboard";
import IndexInfo from "./pages/IndexInfo/IndexInfo";

// The SPA is served by the dashboard blueprint under /dashboard; the basename
// strips that prefix so react-router routes stay relative to it.
export default function App() {
  return (
    <BrowserRouter basename="/dashboard">
      <Routes>
        <Route exact path="/" Component={Dashboard} />
        <Route path="/indexInfo" Component={IndexInfo} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
