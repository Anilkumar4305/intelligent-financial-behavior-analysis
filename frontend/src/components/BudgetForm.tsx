import { useState } from "react";
import api from "../api/client";

type BudgetFormProps = {
  onBudgetAdded: () => void;
};

export default function BudgetForm({ onBudgetAdded }: BudgetFormProps) {
  const [category, setCategory] = useState("");
  const [month, setMonth] = useState("2026-01");
  const [monthlyBudget, setMonthlyBudget] = useState("");
  const [loading, setLoading] = useState(false);

  const submitBudget = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await api.post("/budgets/", {
        category,
        month,
        monthly_budget: Number(monthlyBudget),
      });

      // refresh budget list in dashboard
      onBudgetAdded();

      // reset form
      setCategory("");
      setMonthlyBudget("");
    } catch (err) {
      console.error("Budget create failed:", err);
      alert("Failed to add budget");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-4 rounded shadow">
      <h2 className="font-semibold mb-3">Add Monthly Budget</h2>

      <form onSubmit={submitBudget} className="grid grid-cols-1 md:grid-cols-4 gap-3">
        <input
          type="text"
          placeholder="Category (FOOD)"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          required
          className="border px-3 py-2 rounded"
        />

        <input
          type="month"
          value={month}
          onChange={(e) => setMonth(e.target.value)}
          required
          className="border px-3 py-2 rounded"
        />

        <input
          type="number"
          placeholder="Monthly Budget"
          value={monthlyBudget}
          onChange={(e) => setMonthlyBudget(e.target.value)}
          required
          className="border px-3 py-2 rounded"
        />

        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 text-white rounded px-4 py-2"
        >
          {loading ? "Saving..." : "Add Budget"}
        </button>
      </form>
    </div>
  );
}
