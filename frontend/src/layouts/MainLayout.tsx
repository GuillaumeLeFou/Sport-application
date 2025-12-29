import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useEffect, useRef, useState } from "react";

type User = {
  username?: string;
};

export default function MainLayout() {
  const navigate = useNavigate();
  const [user, setUser] = useState<User | null>(null);
  const [open, setOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Load user from localStorage
  useEffect(() => {
    const raw = localStorage.getItem("user");
    if (raw) setUser(JSON.parse(raw));
  }, []);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(e.target as Node)
      ) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `px-3 py-2 rounded-lg text-sm font-medium transition ${
      isActive ? "bg-emerald-500 text-white" : "text-zinc-200 hover:bg-zinc-800"
    }`;

  const handleLogout = () => {
    localStorage.removeItem("user");
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-white">
      {/* HEADER */}
      <header className="sticky top-0 z-50 border-b border-zinc-800 bg-zinc-950/80 backdrop-blur">
        <div className="mx-auto max-w-6xl px-4 py-3 flex items-center justify-between">
          {/* Brand */}
          <div
            className="cursor-pointer select-none text-lg font-semibold"
            onClick={() => navigate("/home")}
          >
            Sport<span className="text-emerald-400">App</span>
          </div>

          {/* Nav */}
          <nav className="flex items-center gap-2">
            <NavLink to="/home" className={linkClass}>
              Home
            </NavLink>
            <NavLink to="/stats" className={linkClass}>
              Statistics
            </NavLink>

            {/* Profile dropdown */}
            <div className="relative ml-4" ref={dropdownRef}>
              <button
                onClick={() => setOpen((v) => !v)}
                className="flex items-center gap-2 px-3 py-2 rounded-lg bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 transition"
              >
                <span className="text-sm">{user?.username ?? "Profile"}</span>
                <span className="text-xs opacity-70">▾</span>
              </button>

              {open && (
                <div className="absolute right-0 mt-2 w-44 rounded-xl border border-zinc-800 bg-zinc-900 shadow-lg overflow-hidden">
                  <button
                    onClick={() => {
                      setOpen(false);
                      navigate("/profile");
                    }}
                    className="w-full text-left px-4 py-2 text-sm hover:bg-zinc-800 transition"
                  >
                    Profile
                  </button>

                  <div className="h-px bg-zinc-800" />

                  <button
                    onClick={handleLogout}
                    className="w-full text-left px-4 py-2 text-sm text-red-400 hover:bg-zinc-800 transition"
                  >
                    Logout
                  </button>
                </div>
              )}
            </div>
          </nav>
        </div>
      </header>

      {/* PAGE CONTENT */}
      <main className="mx-auto max-w-6xl px-4 py-6">
        <Outlet />
      </main>
    </div>
  );
}
