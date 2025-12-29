import { useEffect, useMemo, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

import BodyWeightUpdateCard from "../components/bodyWeightUpdateCard";
import { getBodyStatsByUser, type BodyStat } from "../api/bodyStat";

type PR = {
  name: string;
  value: number;
  unit: string;
  date: string;
};

type WeightPoint = {
  date: string;
  weight: number;
};

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

function formatLabel(isoDate: string) {
  const d = new Date(`${isoDate}T00:00:00`);
  return d.toLocaleDateString(undefined, { month: "short", day: "2-digit" });
}

function ProgressBar({ value, max }: { value: number; max: number }) {
  const pct = Math.max(0, Math.min(100, Math.round((value / max) * 100)));
  return (
    <div className="w-full">
      <div className="flex items-center justify-between text-sm text-zinc-300 mb-2">
        <span>Progress</span>
        <span className="text-zinc-200 font-medium">{pct}%</span>
      </div>
      <div className="h-3 w-full rounded-full bg-zinc-800 overflow-hidden border border-zinc-700">
        <div
          className="h-full rounded-full bg-emerald-500 transition-all"
          style={{ width: `${pct}%` }}
        />
      </div>
      <div className="mt-2 text-xs text-zinc-400">
        {value} / {max}
      </div>
    </div>
  );
}

function Card({
  title,
  subtitle,
  children,
  className = "",
  action,
}: {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  className?: string;
  action?: React.ReactNode;
}) {
  return (
    <div
      className={[
        "rounded-2xl border border-zinc-800 bg-zinc-950/60",
        "shadow-[0_0_30px_rgba(0,0,0,0.35)]",
        "p-5",
        className,
      ].join(" ")}
    >
      <div className="mb-4 flex items-start justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold text-white">{title}</h2>
          {subtitle && <p className="text-sm text-zinc-400 mt-1">{subtitle}</p>}
        </div>
        {action}
      </div>
      {children}
    </div>
  );
}

export default function StatsPage() {
  const userId = getUserId();

  const prs: PR[] = [
    { name: "Bench Press", value: 85, unit: "kg", date: "2025-12-01" },
    { name: "Squat", value: 110, unit: "kg", date: "2025-11-20" },
    { name: "Deadlift", value: 140, unit: "kg", date: "2025-11-10" },
    { name: "Pull-ups", value: 12, unit: "reps", date: "2025-12-05" },
    { name: "Shoulder Press", value: 55, unit: "kg", date: "2025-10-28" },
  ];

  const [bodyStats, setBodyStats] = useState<BodyStat[]>([]);
  const [loadingWeights, setLoadingWeights] = useState(false);

  useEffect(() => {
    const load = async () => {
      setLoadingWeights(true);
      try {
        const data = await getBodyStatsByUser(userId);
        setBodyStats(data);
      } finally {
        setLoadingWeights(false);
      }
    };

    load();
  }, [userId]);

  const weightData: WeightPoint[] = useMemo(() => {
    const sorted = [...bodyStats].sort((a, b) =>
      a.measured_at.localeCompare(b.measured_at)
    );

    return sorted.map((s) => ({
      date: formatLabel(s.measured_at),
      weight: s.body_weight,
    }));
  }, [bodyStats]);

  const currentWeight = weightData.length
    ? weightData[weightData.length - 1].weight
    : 0;

  const goalWeight = 80;

  const weeklySessionsDone = 3;
  const weeklySessionsGoal = 4;

  const weightGainSoFar = currentWeight ? currentWeight - 70 : 0;
  const totalToGain = goalWeight - 70;

  return (
    <div className="min-h-[calc(100vh-96px)]">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-white">Statistics</h1>
        <p className="text-zinc-400 mt-1">
          Your progress overview (PRs, body weight, and goals).
        </p>
      </div>

      <div className="grid gap-4 grid-cols-1 md:grid-cols-12">
        <Card
          title="Personal Records"
          subtitle="Your best lifts / performances"
          className="md:col-span-5 lg:col-span-4"
        >
          <ul className="space-y-3">
            {prs.map((pr) => (
              <li
                key={pr.name}
                className="flex items-center justify-between rounded-xl border border-zinc-800 bg-zinc-950/40 px-4 py-3"
              >
                <div>
                  <div className="text-white font-medium">{pr.name}</div>
                  <div className="text-xs text-zinc-400 mt-1">
                    Last PR: {pr.date}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-white font-semibold">
                    {pr.value}{" "}
                    <span className="text-zinc-300 font-medium">{pr.unit}</span>
                  </div>
                  <div className="text-xs text-emerald-400 mt-1">PR</div>
                </div>
              </li>
            ))}
          </ul>
        </Card>

        <Card
          title="Body Weight"
          subtitle="Trend over time"
          className="md:col-span-7 lg:col-span-5"
          action={<BodyWeightUpdateCard />}
        >
          {loadingWeights ? (
            <div className="text-zinc-400">Loading body weight…</div>
          ) : weightData.length === 0 ? (
            <div className="text-zinc-400">
              No body weight entries yet. Add your first one.
            </div>
          ) : (
            <>
              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={weightData}>
                    <CartesianGrid strokeDasharray="3 3" opacity={0.15} />
                    <XAxis dataKey="date" />
                    <YAxis domain={["dataMin - 0.5", "dataMax + 0.5"]} />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="weight"
                      strokeWidth={3}
                      dot={{ r: 3 }}
                      activeDot={{ r: 5 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              <div className="mt-4 grid grid-cols-3 gap-3">
                <div className="rounded-xl border border-zinc-800 bg-zinc-950/40 p-3">
                  <div className="text-xs text-zinc-400">Current</div>
                  <div className="text-lg font-semibold text-white">
                    {currentWeight.toFixed(1)} kg
                  </div>
                </div>
                <div className="rounded-xl border border-zinc-800 bg-zinc-950/40 p-3">
                  <div className="text-xs text-zinc-400">Goal</div>
                  <div className="text-lg font-semibold text-white">
                    {goalWeight} kg
                  </div>
                </div>
                <div className="rounded-xl border border-zinc-800 bg-zinc-950/40 p-3">
                  <div className="text-xs text-zinc-400">To gain</div>
                  <div className="text-lg font-semibold text-white">
                    {Math.max(0, goalWeight - currentWeight).toFixed(1)} kg
                  </div>
                </div>
              </div>
            </>
          )}
        </Card>

        <Card
          title="Weekly Goal"
          subtitle="Sessions completed this week"
          className="md:col-span-12 lg:col-span-3"
        >
          <ProgressBar value={weeklySessionsDone} max={weeklySessionsGoal} />

          <div className="mt-5 rounded-xl border border-zinc-800 bg-zinc-950/40 p-4">
            <div className="text-sm text-zinc-300 mb-2">Mass gain progress</div>
            <ProgressBar
              value={Math.max(0, Math.round(weightGainSoFar * 10) / 10)}
              max={Math.max(1, Math.round(totalToGain * 10) / 10)}
            />
          </div>
        </Card>
      </div>
    </div>
  );
}
