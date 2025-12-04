import { Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/login";
import HomePage from "./pages/home";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/home" element={<HomePage />} />
      {/* plus tard : <Route path="/dashboard" element={<Dashboard />} /> */}
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}

export default App;
