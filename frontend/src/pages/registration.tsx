import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";

function RegisterPage() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [firstname, setFirstname] = useState("");
  const [lastname, setLastname] = useState("");
  const [dateOfBirth, setDateOfBirth] = useState<string>("");
  const [weight, setWeight] = useState<string>("");
  const [height, setHeight] = useState<string>("");

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const dateInputRef = useRef<HTMLInputElement | null>(null);

  const openDatePicker = () => {
    const input = dateInputRef.current;
    if (!input) return;

    // @ts-ignore : showPicker n'est pas encore dans le type standard
    if (input.showPicker) {
      // @ts-ignore
      input.showPicker();
    } else {
      input.focus();
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      const payload = {
        username,
        password,
        firstname,
        lastname,
        birthday: dateOfBirth, // ex: "2000-12-07"
        weight: Number(weight),
        height: Number(height),
      };

      console.log("Payload envoyé :", payload);

      const response = await api.post("/users/", payload);

      console.log("User created:", response.data);
      navigate("/login");
    } catch (err: any) {
      console.error("ERR REGISTER:", err);

      const detail = err?.response?.data?.detail;

      if (Array.isArray(detail)) {
        const msg = detail.map((d: any) => d.msg).join(" | ");
        setError(msg);
      } else if (typeof detail === "string") {
        setError(detail);
      } else {
        setError("Erreur lors de la création du compte. Vérifie les champs.");
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  // Classe de base pour tous les inputs "simples"
  const baseInputClasses =
    "w-full px-3 py-2.5 rounded-lg bg-zinc-900/80 border border-zinc-700 text-white text-sm outline-none focus:border-emerald-400 focus:ring-2 focus:ring-emerald-500/60 transition";

  return (
    <div className="h-screen overflow-hidden flex items-center justify-center bg-zinc-950 relative">
      {/* Fond */}
      <div className="absolute inset-0 -z-10 bg-gradient-to-br from-zinc-950 via-zinc-900 to-black" />
      <div className="absolute inset-0 -z-10 opacity-40 blur-3xl bg-[radial-gradient(circle_at_top,_rgba(16,185,129,0.35),_transparent_55%),_radial-gradient(circle_at_bottom,_rgba(15,118,110,0.25),_transparent_55%)]" />

      {/* Carte */}
      <div className="w-full max-w-md max-h-[92vh] overflow-y-auto px-6 py-7 md:px-8 md:py-8 rounded-2xl border border-emerald-500/40 bg-zinc-950/80 shadow-[0_0_35px_rgba(16,185,129,0.35)] backdrop-blur-md">
        {/* Titre */}
        <div className="mb-6 text-center">
          <h1 className="text-2xl md:text-3xl font-semibold text-white tracking-tight">
            Créer un compte
          </h1>
          <p className="mt-1 text-xs md:text-sm text-zinc-400">
            Rejoins Sport<span className="text-emerald-400">App</span> et
            commence à suivre tes entraînements.
          </p>
        </div>

        {/* Erreur */}
        {error && (
          <div className="mb-4 text-sm text-red-300 bg-red-950/40 px-3 py-2 rounded-lg border border-red-500/40">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Prénom / Nom */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="space-y-1">
              <label className="block text-sm font-medium text-zinc-200">
                Prénom
              </label>
              <input
                type="text"
                value={firstname}
                onChange={(e) => setFirstname(e.target.value)}
                required
                className={baseInputClasses}
              />
            </div>
            <div className="space-y-1">
              <label className="block text-sm font-medium text-zinc-200">
                Nom
              </label>
              <input
                type="text"
                value={lastname}
                onChange={(e) => setLastname(e.target.value)}
                required
                className={baseInputClasses}
              />
            </div>
          </div>

          {/* Username / Mot de passe */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="space-y-1">
              <label className="block text-sm font-medium text-zinc-200">
                Nom d&apos;utilisateur
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className={baseInputClasses}
              />
            </div>
            <div className="space-y-1">
              <label className="block text-sm font-medium text-zinc-200">
                Mot de passe
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className={baseInputClasses}
              />
            </div>
          </div>

          {/* Date de naissance + Poids + Taille */}
          <div className="flex flex-col sm:flex-row gap-3 mt-1">
            {/* Date de naissance */}
            <div className="flex-1 space-y-1">
              <label className="block text-sm font-medium text-zinc-200">
                Date de naissance
              </label>
              <div className="relative">
                <button
                  type="button"
                  onClick={openDatePicker}
                  className="absolute inset-y-0 left-0 pl-3 pr-2 flex items-center text-zinc-500 hover:text-emerald-400 transition"
                >
                  <svg
                    className="w-4 h-4"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                    <line x1="16" y1="2" x2="16" y2="6" />
                    <line x1="8" y1="2" x2="8" y2="6" />
                    <line x1="3" y1="10" x2="21" y2="10" />
                  </svg>
                </button>

                <input
                  ref={dateInputRef}
                  type="date"
                  value={dateOfBirth}
                  onChange={(e) => setDateOfBirth(e.target.value)}
                  required
                  className="
                    w-full 
                    pl-10 pr-3 py-2.5
                    rounded-lg bg-zinc-900/80 border border-zinc-700
                    text-white text-sm outline-none
                    focus:border-emerald-400 focus:ring-2 focus:ring-emerald-500/60
                    transition [color-scheme:dark]
                    [&::-webkit-calendar-picker-indicator]:opacity-0
                    [&::-webkit-calendar-picker-indicator]:pointer-events-none
                  "
                />
              </div>
            </div>

            {/* Poids */}
            <div className="sm:w-28 flex-1 space-y-1">
              <label className="block text-sm font-medium text-zinc-200">
                Poids
              </label>
              <div className="relative">
                <input
                  type="number"
                  step="0.1"
                  min={0}
                  value={weight}
                  onChange={(e) => setWeight(e.target.value)}
                  required
                  className="
                    w-full 
                    pr-10 pl-3 py-2.5
                    rounded-lg bg-zinc-900/80 border border-zinc-700
                    text-white text-sm outline-none
                    focus:border-emerald-400 focus:ring-2 focus:ring-emerald-500/60
                    transition
                  "
                />
                <span className="absolute inset-y-0 right-3 flex items-center text-zinc-500 text-xs">
                  kg
                </span>
              </div>
            </div>

            {/* Taille */}
            <div className="sm:w-28 flex-1 space-y-1">
              <label className="block text-sm font-medium text-zinc-200">
                Taille
              </label>
              <div className="relative">
                <input
                  type="number"
                  min={0}
                  value={height}
                  onChange={(e) => setHeight(e.target.value)}
                  required
                  className="
                    w-full 
                    pr-10 pl-3 py-2.5
                    rounded-lg bg-zinc-900/80 border border-zinc-700
                    text-white text-sm outline-none
                    focus:border-emerald-400 focus:ring-2 focus:ring-emerald-500/60
                    transition
                  "
                />
                <span className="absolute inset-y-0 right-3 flex items-center text-zinc-500 text-xs">
                  cm
                </span>
              </div>
            </div>
          </div>

          {/* Bouton */}
          <button
            type="submit"
            disabled={isSubmitting}
            className="mt-2 w-full py-2.5 rounded-lg bg-emerald-500 text-white font-semibold text-sm tracking-wide hover:bg-emerald-400 disabled:opacity-60 disabled:cursor-not-allowed transition"
          >
            {isSubmitting ? "Création du compte..." : "Créer un compte"}
          </button>
        </form>

        <p className="mt-4 text-xs text-center text-zinc-500">
          Tu as déjà un compte ?{" "}
          <span
            onClick={() => navigate("/login")}
            className="text-emerald-400 hover:text-emerald-300 cursor-pointer"
          >
            Retour à la connexion
          </span>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;
