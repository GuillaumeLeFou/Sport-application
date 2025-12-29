import { Link } from "react-router-dom";

function HomePage() {
  return (
    <>
      <h1 className="text-4xl font-bold mb-4">Accueil</h1>
      <p className="text-slate-300 mb-6">
        Ça, c'est la page d'accueil stylée 😎
      </p>
      <Link
        to="/stats"
        className="px-4 py-2 bg-emerald-500 hover:bg-emerald-600 rounded-lg font-semibold"
      >
        Aller vers les stats
      </Link>
    </>
  );
}

export default HomePage;
