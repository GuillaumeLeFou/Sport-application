import { Routes, Route, Navigate } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";

import Login from "./pages/login";
import Registration from "./pages/registration";
import Home from "./pages/home";
import StatsPage from "./pages/stats";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/registration" element={<Registration />} />

      <Route element={<MainLayout />}>
        <Route path="/home" element={<Home />} />
        <Route path="/stats" element={<StatsPage />} />

        <Route path="/" element={<Navigate to="/home" replace />} />
      </Route>

      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}
