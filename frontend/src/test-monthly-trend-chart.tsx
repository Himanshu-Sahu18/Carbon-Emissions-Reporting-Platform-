import React from "react";
import { createRoot } from "react-dom/client";
import MonthlyTrendChart from "./components/charts/MonthlyTrendChart";
import { useAnalytics } from "./hooks/useAnalytics";
import "./index.css";

/**
 * Test component for MonthlyTrendChart
 * This demonstrates the component with real data from the API
 */
function TestMonthlyTrendChart() {
  const { monthlyData, loading, error, refresh } = useAnalytics();

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Monthly Trend Chart Test
          </h1>
          <p className="text-gray-600">
            Testing the MonthlyTrendChart component with real API data
          </p>
          <button
            onClick={refresh}
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
          >
            Refresh Data
          </button>
        </div>

        <div className="space-y-8">
          <div>
            <h2 className="text-xl font-semibold mb-4">
              Monthly Trend Chart (with data from useAnalytics)
            </h2>
            <MonthlyTrendChart
              data={monthlyData}
              loading={loading}
              error={error}
              onRefresh={refresh}
            />
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-4">
              Monthly Trend Chart (loading state)
            </h2>
            <MonthlyTrendChart data={null} loading={true} error={null} />
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-4">
              Monthly Trend Chart (error state)
            </h2>
            <MonthlyTrendChart
              data={null}
              loading={false}
              error={new Error("Failed to fetch monthly data")}
              onRefresh={() => console.log("Retry clicked")}
            />
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-4">
              Monthly Trend Chart (empty state)
            </h2>
            <MonthlyTrendChart
              data={{ year: 2024, months: [] }}
              loading={false}
              error={null}
            />
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-4">
              Monthly Trend Chart (with mock data - partial year)
            </h2>
            <MonthlyTrendChart
              data={{
                year: 2024,
                months: [
                  {
                    month: 1,
                    month_name: "January",
                    total_emissions: 45000,
                    record_count: 12,
                  },
                  {
                    month: 2,
                    month_name: "February",
                    total_emissions: 52000,
                    record_count: 15,
                  },
                  {
                    month: 3,
                    month_name: "March",
                    total_emissions: 48000,
                    record_count: 14,
                  },
                  {
                    month: 4,
                    month_name: "April",
                    total_emissions: 55000,
                    record_count: 16,
                  },
                  {
                    month: 5,
                    month_name: "May",
                    total_emissions: 51000,
                    record_count: 13,
                  },
                  {
                    month: 6,
                    month_name: "June",
                    total_emissions: 58000,
                    record_count: 18,
                  },
                ],
              }}
              loading={false}
              error={null}
            />
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-4">
              Monthly Trend Chart (with mock data - full year with gaps)
            </h2>
            <MonthlyTrendChart
              data={{
                year: 2024,
                months: [
                  {
                    month: 1,
                    month_name: "January",
                    total_emissions: 45000,
                    record_count: 12,
                  },
                  {
                    month: 3,
                    month_name: "March",
                    total_emissions: 48000,
                    record_count: 14,
                  },
                  {
                    month: 5,
                    month_name: "May",
                    total_emissions: 51000,
                    record_count: 13,
                  },
                  {
                    month: 7,
                    month_name: "July",
                    total_emissions: 62000,
                    record_count: 19,
                  },
                  {
                    month: 9,
                    month_name: "September",
                    total_emissions: 58000,
                    record_count: 17,
                  },
                  {
                    month: 11,
                    month_name: "November",
                    total_emissions: 54000,
                    record_count: 15,
                  },
                ],
              }}
              loading={false}
              error={null}
            />
          </div>
        </div>

        <div className="mt-8 p-4 bg-white rounded-lg shadow">
          <h3 className="font-semibold mb-2">Debug Info:</h3>
          <pre className="text-xs overflow-auto">
            {JSON.stringify(
              { monthlyData, loading, error: error?.message },
              null,
              2
            )}
          </pre>
        </div>
      </div>
    </div>
  );
}

// Mount the test component
const container = document.getElementById("root");
if (container) {
  const root = createRoot(container);
  root.render(
    <React.StrictMode>
      <TestMonthlyTrendChart />
    </React.StrictMode>
  );
}
