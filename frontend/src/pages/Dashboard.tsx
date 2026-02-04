import { useEffect, useState } from "react";
import { getAnalyticsSummary, getBudgets } from "../api/analytics";
import BudgetForm from "../components/BudgetForm";
import BudgetList from "../components/BudgetList";
import CsvUpload from "../components/CsvUpload";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
} from "recharts";

/* =========================
   TYPES (MATCH BACKEND)
========================= */
interface DashboardData {
  health_score: number;
  monthly_spend: number;
  top_category: string;
  risk_alerts: string[];
  category_breakdown: Record<string, number>;
  budget_vs_actual: {
    budget: number;
    actual: number;
  };
}

/* =========================
   HEALTH SCORE
========================= */
function getHealthMeta(score: number) {
  if (score <= 40)
    return { label: "Critical", color: "text-red-600", bg: "bg-red-100", bar: "bg-red-500" };
  if (score <= 70)
    return { label: "Moderate", color: "text-yellow-600", bg: "bg-yellow-100", bar: "bg-yellow-500" };
  return { label: "Good", color: "text-green-600", bg: "bg-green-100", bar: "bg-green-500" };
}

function HealthCard({ score }: { score: number }) {
  const meta = getHealthMeta(score);
  return (
    <div className="bg-white p-4 rounded shadow">
      <p className="text-gray-500 text-sm mb-1">Health Score</p>
      <div className="flex justify-between items-center mb-2">
        <span className="text-2xl font-bold">{score}</span>
        <span className={`text-sm px-2 py-1 rounded ${meta.bg} ${meta.color}`}>
          {meta.label}
        </span>
      </div>
      <div className="w-full bg-gray-200 h-2 rounded">
        <div className={`h-2 rounded ${meta.bar}`} style={{ width: `${Math.min(score, 100)}%` }} />
      </div>
    </div>
  );
}

function Card({ title, value }: { title: string; value: string | number }) {
  return (
    <div className="bg-white p-4 rounded shadow">
      <p className="text-gray-500 text-sm">{title}</p>
      <p className="text-xl font-bold">{value}</p>
    </div>
  );
}

/* =========================
   DASHBOARD
========================= */
export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [selectedMonth] = useState("2026-01");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [budgets, setBudgets] = useState<any[]>([]);

  /* ===== Manual Analytics Refresh (Used after CSV upload) ===== */
  const refreshAnalytics = () => {
    setLoading(true);
    setError(null);

    getAnalyticsSummary(selectedMonth)
      .then((res) => {
        if (!res?.data) throw new Error("No data received");
        setData(res.data as DashboardData);
      })
      .catch((err) => {
        console.error("Analytics error:", err);
        setError("Failed to load analytics data");
        setData(null);
      })
      .finally(() => setLoading(false));
  };

  /* ===== Initial Analytics Load ===== */
  useEffect(() => {
    refreshAnalytics();
  }, [selectedMonth]);

  /* ===== Fetch Budgets ===== */
  const fetchBudgets = () => {
    getBudgets()
      .then((res) => setBudgets(res.data || []))
      .catch(() => setBudgets([]));
  };

  useEffect(() => {
    fetchBudgets();
  }, []);

  /* ===== Transform Data ===== */
  const categoryData =
    data?.category_breakdown
      ? Object.entries(data.category_breakdown).map(([category, amount]) => ({
          name: category,
          value: amount,
        }))
      : [];

  const budgetData =
    data?.budget_vs_actual
      ? [
          { name: "Budget", value: data.budget_vs_actual.budget },
          { name: "Actual", value: data.budget_vs_actual.actual },
        ]
      : [];

  /* ===== UI States ===== */
  if (loading) return <div className="p-6">Loading analytics...</div>;
  if (error) return <div className="p-6 text-red-600">{error}</div>;
  if (!data) return null;

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-2xl font-bold mb-6">Financial Behavior Dashboard</h1>

      {/* ✅ CSV Upload Section */}
      <div className="mb-6">
        <CsvUpload
          onUploadSuccess={() => {
            refreshAnalytics(); // 🔥 auto refresh after upload
          }}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <HealthCard score={data.health_score} />
        <Card title="Monthly Spend" value={`₹ ${data.monthly_spend}`} />
        <Card title="Top Category" value={data.top_category} />
      </div>

      <div className="mt-6">
        <BudgetForm onBudgetAdded={fetchBudgets} />
      </div>

      <BudgetList budgets={budgets} />

      <div className="mt-6 bg-white p-4 rounded shadow">
        <h2 className="font-semibold mb-2">Risk Alerts</h2>
        {data.risk_alerts?.length ? (
          <ul className="list-disc pl-5">
            {data.risk_alerts.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-500">No risk alerts.</p>
        )}
      </div>

      <div className="mt-6 bg-white p-4 rounded shadow">
        <h2 className="font-semibold mb-4">Category Spending</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={categoryData}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-6 bg-white p-4 rounded shadow">
        <h2 className="font-semibold mb-4">Budget vs Actual</h2>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie data={budgetData} dataKey="value" label>
              {budgetData.map((_, i) => (
                <Cell key={i} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
