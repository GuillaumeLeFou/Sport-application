import { useState } from "react";
import { createBodyStat } from "../api/bodyStat";

function getUserId(): number {
  try {
    const raw = localStorage.getItem("user");
    if (!raw) return 1;
    const user = JSON.parse(raw);
    return Number(user?.id) || 1;
  } catch {
    return 1;
  }
}

export default function BodyWeightUpdateCard() {
  const userId = getUserId();

  const [open, setOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [measuredAt, setMeasuredAt] = useState(
    new Date().toISOString().slice(0, 10)
  );
  const [bodyWeight, setBodyWeight] = useState("");
  const [notes, setNotes] = useState("");

  const handleSave = async () => {
    setError(null);

    const weight = Number(bodyWeight);
    if (!Number.isFinite(weight) || weight <= 0) {
      setError("Please enter a valid weight.");
      return;
    }

    setIsSubmitting(true);
    try {
      await createBodyStat({
        user_id: userId,
        measured_at: measuredAt,
        body_weight: weight,
        notes: notes.trim() ? notes.trim() : null,
      });

      setOpen(false);
      setBodyWeight("");
      setNotes("");
    } catch (err: any) {
      console.error(err);
      setError(
        err?.response?.data?.detail ||
          "Erreur serveur lors de l'enregistrement."
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      {/* BUTTON (for Card header) */}
      <button
        onClick={() => setOpen(true)}
        className="rounded-xl border border-zinc-800 bg-zinc-950/40 px-3 py-2 text-sm text-zinc-200 hover:bg-zinc-900 transition"
      >
        Update
      </button>

      {/* MODAL */}
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div
            className="absolute inset-0 bg-black/60"
            onClick={() => !isSubmitting && setOpen(false)}
          />

          <div className="relative w-full max-w-sm rounded-2xl border border-zinc-800 bg-zinc-950 p-5">
            <div className="flex items-start justify-between gap-3 mb-4">
              <div>
                <h3 className="text-lg font-semibold text-white">
                  Update body weight
                </h3>
                <p className="text-sm text-zinc-400 mt-1">
                  Add a new body weight entry
                </p>
              </div>
              <button
                onClick={() => !isSubmitting && setOpen(false)}
                className="text-zinc-400 hover:text-white"
              >
                ✕
              </button>
            </div>

            {error && (
              <div className="mb-4 text-sm text-red-300 bg-red-950/40 px-3 py-2 rounded-lg border border-red-500/40">
                {error}
              </div>
            )}

            <div className="grid gap-3">
              <label className="text-sm text-zinc-300">
                Date
                <input
                  type="date"
                  value={measuredAt}
                  onChange={(e) => setMeasuredAt(e.target.value)}
                  className="mt-1 w-full rounded-xl border border-zinc-800 bg-zinc-900 px-3 py-2 text-white"
                />
              </label>

              <label className="text-sm text-zinc-300">
                Weight (kg)
                <input
                  type="number"
                  step="0.1"
                  value={bodyWeight}
                  onChange={(e) => setBodyWeight(e.target.value)}
                  placeholder="e.g. 71.4"
                  className="mt-1 w-full rounded-xl border border-zinc-800 bg-zinc-900 px-3 py-2 text-white"
                />
              </label>

              <label className="text-sm text-zinc-300">
                Notes (optional)
                <textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  rows={3}
                  className="mt-1 w-full rounded-xl border border-zinc-800 bg-zinc-900 px-3 py-2 text-white"
                  placeholder="Morning, after workout, etc."
                />
              </label>
            </div>

            <div className="mt-5 flex justify-end gap-3">
              <button
                onClick={() => setOpen(false)}
                disabled={isSubmitting}
                className="rounded-xl border border-zinc-800 bg-zinc-900 px-4 py-2 text-zinc-300 hover:bg-zinc-800 disabled:opacity-60"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                disabled={isSubmitting}
                className="rounded-xl bg-emerald-500 px-4 py-2 text-white font-semibold hover:bg-emerald-400 disabled:opacity-60"
              >
                {isSubmitting ? "Saving..." : "Save"}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
