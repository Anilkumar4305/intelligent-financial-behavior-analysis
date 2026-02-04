import axios from "axios";

/* =========================
   AXIOS INSTANCE
========================= */
const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

/* =========================
   TYPES FROM BACKEND
========================= */
export interface AnalyticsSummary {
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
   API CALLS (TYPED)
========================= */

// ✅ This tells TS what res.data contains
export const getAnalyticsSummary = (month: string) =>
  api.get<AnalyticsSummary>(`/analytics/summary?month=${month}`);

export const getBudgets = () =>
  api.get<any[]>(`/budgets`);
