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
    <div className="min-h-screen flex items-center justify-center bg-zinc-950">
      <div className="absolute inset-0 -z-10 bg-gradient-to-br from-zinc-950 via-zinc-900 to-black" />
      <div className="absolute inset-0 -z-10 opacity-40 blur-3xl bg-[radial-gradient(circle_at_top,_rgba(16,185,129,0.35),_transparent_55%),_radial-gradient(circle_at_bottom,_rgba(15,118,110,0.25),_transparent_55%)]" />

      <div className="w-full max-w-md px-8 py-10 rounded-2xl border border-emerald-500/40 bg-zinc-950/80 shadow-[0_0_35px_rgba(16,185,129,0.35)] backdrop-blur-md">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-semibold text-white tracking-tight">
            Sport<span className="text-emerald-400">App</span>
          </h1>
          <p className="mt-2 text-sm text-zinc-400">
            Connecte-toi pour suivre tes séances et ta progression.
          </p>
        </div>

        {error && (
          <div className="mb-5 text-sm text-red-300 bg-red-950/40 px-3 py-2 rounded-lg border border-red-500/40">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="space-y-1.5">
            <label className="block text-sm font-medium text-zinc-200">
              Nom d'utilisateur
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="w-full px-3 py-2.5 rounded-lg bg-zinc-900/80 border border-zinc-700 text-white text-sm outline-none focus:border-emerald-400 focus:ring-2 focus:ring-emerald-500/60 transition"
            />
          </div>

          <div className="space-y-1.5">
            <label className="block text-sm font-medium text-zinc-200">
              Mot de passe
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-3 py-2.5 rounded-lg bg-zinc-900/80 border border-zinc-700 text-white text-sm outline-none focus:border-emerald-400 focus:ring-2 focus:ring-emerald-500/60 transition"
            />
          </div>
          <button
            type="submit"
            disabled={isSubmitting}
            className="mt-2 w-full py-2.5 rounded-lg bg-emerald-500 text-white font-semibold text-sm tracking-wide
             hover:bg-emerald-400 disabled:opacity-60 disabled:cursor-not-allowed
             transition"
          >
            {isSubmitting ? "Connexion..." : "Se connecter"}
          </button>
        </form>

        <p className="mt-6 text-xs text-center text-zinc-500">
          Tu n'as pas encore de compte ?{" "}
          <span
            onClick={() => navigate("/registration")}
            className="text-emerald-400 hover:text-emerald-300 cursor-pointer"
          >
            Créer un compte
          </span>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;
