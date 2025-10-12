import React from "react";
import { createRoot } from "react-dom/client";
import IntensityKPICard from "./components/charts/IntensityKPICard";
import type { IntensityResponse } from "./types/api.types";
import "./index.css";

/**
 * Test component for IntensityKPICard
 * Tests different states: loading, error, no data, no production data, and success
 */
const TestIntensityKPICard: React.FC = () => {
  const [state, setState] = React.useState<
    "loading" | "error" | "empty" | "no-production" | "low" | "medium" | "high"
  >("low");

  // Mock data for different intensity levels
  const lowIntensityData: IntensityResponse = {
    period: {
      start_date: "2024-01-01",
      end_date: "2024-03-31",
    },
    metric_name: "Tons of Steel Produced",
    total_emissions: 75000,
    total_production: 200000,
    production_unit: "tons",
    intensity: 0.375,
    intensity_unit: "kgCO2e per ton",
    record_count: 45,
  };

  const mediumIntensityData: IntensityResponse = {
    period: {
      start_date: "2024-04-01",
      end_date: "2024-06-30",
    },
    metric_name: "Tons of Steel Produced",
    total_emissions: 125000,
    total_production: 150000,
    production_unit: "tons",
    intensity: 0.833,
    intensity_unit: "kgCO2e per ton",
    record_count: 52,
  };

  const highIntensityData: IntensityResponse = {
    period: {
      start_date: "2024-07-01",
      end_date: "2024-09-30",
    },
    metric_name: "Tons of Steel Produced",
    total_emissions: 180000,
    total_production: 120000,
    production_unit: "tons",
    intensity: 1.5,
    intensity_unit: "kgCO2e per ton",
    record_count: 38,
  };

  const noProductionData: IntensityResponse = {
    period: {
      start_date: "2024-01-01",
      end_date: "2024-03-31",
    },
    metric_name: "Tons of Steel Produced",
    total_emissions: 75000,
    total_production: 0,
    production_unit: "tons",
    intensity: 0,
    intensity_unit: "kgCO2e per ton",
    record_count: 0,
  };

  const getData = () => {
    switch (state) {
      case "low":
        return lowIntensityData;
      case "medium":
        return mediumIntensityData;
      case "high":
        return highIntensityData;
      case "no-production":
        return noProductionData;
      case "empty":
        return null;
      default:
        return lowIntensityData;
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Intensity KPI Card Test
        </h1>

        {/* State Controls */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Test States</h2>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setState("loading")}
              className={`px-4 py-2 rounded-md ${
                state === "loading"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200 text-gray-800"
              }`}
            >
              Loading
            </button>
            <button
              onClick={() => setState("error")}
              className={`px-4 py-2 rounded-md ${
                state === "error"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200 text-gray-800"
              }`}
            >
              Error
            </button>
            <button
              onClick={() => setState("empty")}
              className={`px-4 py-2 rounded-md ${
                state === "empty"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200 text-gray-800"
              }`}
            >
              No Data
            </button>
            <button
              onClick={() => setState("no-production")}
              className={`px-4 py-2 rounded-md ${
                state === "no-production"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200 text-gray-800"
              }`}
            >
              No Production Data
            </button>
            <button
              onClick={() => setState("low")}
              className={`px-4 py-2 rounded-md ${
                state === "low"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200 text-gray-800"
              }`}
            >
              Low Intensity (0.375)
            </button>
            <button
              onClick={() => setState("medium")}
              className={`px-4 py-2 rounded-md ${
                state === "medium"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200 text-gray-800"
              }`}
            >
              Medium Intensity (0.833)
            </button>
            <button
              onClick={() => setState("high")}
              className={`px-4 py-2 rounded-md ${
                state === "high"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200 text-gray-800"
              }`}
            >
              High Intensity (1.5)
            </button>
          </div>
        </div>

        {/* Component Display */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <h2 className="text-xl font-semibold mb-4">Component</h2>
            <IntensityKPICard
              data={getData()}
              loading={state === "loading"}
              error={
                state === "error"
                  ? new Error("Failed to fetch intensity data")
                  : null
              }
              startDate={new Date("2024-01-01")}
              endDate={new Date("2024-03-31")}
              metricName="Tons of Steel Produced"
              onRefresh={() => console.log("Refresh clicked")}
            />
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-4">Data Preview</h2>
            <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
              <pre className="text-xs overflow-auto">
                {JSON.stringify(
                  {
                    state,
                    data: getData(),
                    loading: state === "loading",
                    error: state === "error" ? "Error object" : null,
                  },
                  null,
                  2
                )}
              </pre>
            </div>
          </div>
        </div>

        {/* Feature Checklist */}
        <div className="mt-8 bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Feature Checklist</h2>
          <ul className="space-y-2 text-sm">
            <li className="flex items-center">
              <span className="text-green-600 mr-2">✓</span>
              Display intensity value prominently with large font
            </li>
            <li className="flex items-center">
              <span className="text-green-600 mr-2">✓</span>
              Show intensity unit below the value
            </li>
            <li className="flex items-center">
              <span className="text-green-600 mr-2">✓</span>
              Display date range used for calculation
            </li>
            <li className="flex items-center">
              <span className="text-green-600 mr-2">✓</span>
              Show supporting metrics (total emissions, total production)
            </li>
            <li className="flex items-center">
              <span className="text-green-600 mr-2">✓</span>
              Apply color coding based on intensity value (green/yellow/red)
            </li>
            <li className="flex items-center">
              <span className="text-green-600 mr-2">✓</span>
              Handle loading state
            </li>
            <li className="flex items-center">
              <span className="text-green-600 mr-2">✓</span>
              Handle error state with retry option
            </li>
            <li className="flex items-center">
              <span className="text-green-600 mr-2">✓</span>
              Display message when production data unavailable
            </li>
            <li className="flex items-center">
              <span className="text-green-600 mr-2">✓</span>
              Display empty state when no data available
            </li>
            <li className="flex items-center">
              <span className="text-green-600 mr-2">✓</span>
              Show intensity level indicator legend
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

// Mount the test component
const container = document.getElementById("root");
if (container) {
  const root = createRoot(container);
  root.render(<TestIntensityKPICard />);
}
