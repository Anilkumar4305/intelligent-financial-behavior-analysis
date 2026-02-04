import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
} from "recharts";

/* =========================
   TYPES (MATCH BACKEND)
========================= */
type CategoryItem = {
  category: string;
  total: number;
};

type MonthlyItem = {
  month: string;
  total_spent: number;
};

type Props = {
  categoryData?: CategoryItem[];
  monthlyData?: MonthlyItem[];
};

/* Chart colors */
const COLORS = ["#2563eb", "#16a34a", "#f59e0b", "#dc2626", "#7c3aed"];

export default function ChartsSection({
  categoryData = [],
  monthlyData = [],
}: Props) {
  const hasCategoryData = Array.isArray(categoryData) && categoryData.length > 0;
  const hasMonthlyData = Array.isArray(monthlyData) && monthlyData.length > 0;

  return (
    <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* ================= PIE CHART ================= */}
      <div className="bg-white p-4 rounded shadow">
        <h3 className="font-semibold mb-4">Category-wise Spending</h3>

        {!hasCategoryData ? (
          <p className="text-gray-500 text-sm">No category data available.</p>
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={categoryData}
                dataKey="total"
                nameKey="category"
                outerRadius={100}
                label
              >
                {categoryData.map((_, index) => (
                  <Cell
                    key={index}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        )}
      </div>

      {/* ================= BAR CHART ================= */}
      <div className="bg-white p-4 rounded shadow">
        <h3 className="font-semibold mb-4">Monthly Spending Trend</h3>

        {!hasMonthlyData ? (
          <p className="text-gray-500 text-sm">No monthly data available.</p>
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={monthlyData}>
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="total_spent" />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}
