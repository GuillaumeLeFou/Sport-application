import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";

function LoginPage() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      const response = await api.post("/auth/login", {
        username,
        password,
      });

      console.log("Réponse login:", response.data.username);

      const user = response.data;
      localStorage.setItem("user", JSON.stringify(user));
      navigate("/home");
    } catch (err: any) {
      console.error(err);
      setError(
        err?.response?.data?.detail ||
          "Identifiants incorrects ou erreur serveur."
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900">
      <div className="w-full max-w-md bg-slate-800 p-8 rounded-xl shadow-lg">
        <h1 className="text-2xl font-bold text-white mb-6 text-center">
          Sport App – Connexion
        </h1>

        {error && (
          <div className="mb-4 text-sm text-red-400 bg-red-950/40 px-3 py-2 rounded">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-slate-200 mb-1">
              Nom d'utilisateur
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="w-full px-3 py-2 rounded bg-slate-900 border border-slate-700 text-white outline-none focus:border-emerald-400"
            />
          </div>

          <div>
            <label className="block text-sm text-slate-200 mb-1">
              Mot de passe
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-3 py-2 rounded bg-slate-900 border border-slate-700 text-white outline-none focus:border-emerald-400"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full py-2 rounded bg-emerald-500 text-white font-semibold hover:bg-emerald-600 disabled:opacity-60"
          >
            {isSubmitting ? "Connexion..." : "Se connecter"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;
