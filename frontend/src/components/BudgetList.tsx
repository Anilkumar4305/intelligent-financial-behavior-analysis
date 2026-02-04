type Budget = {
  id: number;
  category: string;
  month: string;
  monthly_budget: number;
};

export default function BudgetList({ budgets }: { budgets: Budget[] }) {
  // Safe empty state
  if (!budgets || budgets.length === 0) {
    return (
      <p className="text-gray-500 text-sm">
        No budgets added yet.
      </p>
    );
  }

  return (
    <div className="bg-white p-4 rounded-lg shadow mt-4">
      <h2 className="text-lg font-semibold mb-3">Your Budgets</h2>

      {/* Makes table scrollable on mobile */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm border">
          <thead className="bg-gray-100">
            <tr>
              <th className="border px-3 py-2 text-left">Category</th>
              <th className="border px-3 py-2 text-left">Month</th>
              <th className="border px-3 py-2 text-right">Monthly Budget (₹)</th>
            </tr>
          </thead>

          <tbody>
            {budgets.map((b) => (
              <tr key={b.id}>
                <td className="border px-3 py-2">{b.category}</td>
                <td className="border px-3 py-2">{b.month}</td>
                <td className="border px-3 py-2 text-right font-medium">
                  ₹ {b.monthly_budget.toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
