import { Link } from "react-router-dom";

function HomePage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-900">
      <h1 className="text-4xl font-bold mb-4">Accueil</h1>
      <p className="text-slate-300 mb-6">
        Ça, c'est la page d'accueil stylée 😎
      </p>
      <Link
        to="/login"
        className="px-4 py-2 bg-emerald-500 hover:bg-emerald-600 rounded-lg font-semibold"
      >
        Aller vers le login
      </Link>
    </div>
  );
}

export default HomePage;
