import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import type { YoYChartProps } from "../../types/component.types";
import LoadingSpinner from "../common/LoadingSpinner";
import ErrorMessage from "../common/ErrorMessage";
import EmptyState from "../common/EmptyState";

/**
 * Custom tooltip component for the YoY chart
 */
const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-lg">
        <p className="font-semibold text-gray-900 mb-2">{label}</p>
        {payload.map((entry: any, index: number) => (
          <p key={index} className="text-sm" style={{ color: entry.color }}>
            <span className="font-medium">{entry.name}:</span>{" "}
            {entry.value?.toLocaleString()} kgCO2e
          </p>
        ))}
      </div>
    );
  }
  return null;
};

/**
 * Year-over-Year Emissions Chart Component
 * Displays a stacked bar chart comparing emissions by scope across years
 */
const YoYChart: React.FC<YoYChartProps> = ({
  data,
  loading = false,
  error = null,
  onRefresh,
}) => {
  // Handle loading state
  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-4 sm:p-6 border border-gray-200 h-64 sm:h-80 lg:h-96 flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  // Handle error state
  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-md p-4 sm:p-6 border border-gray-200 min-h-[16rem] sm:min-h-[20rem] lg:min-h-[24rem]">
        <h3 className="text-lg sm:text-xl font-semibold mb-3 sm:mb-4 text-gray-800">
          Year-over-Year Emissions
        </h3>
        <ErrorMessage message={error.message} onRetry={onRefresh} />
      </div>
    );
  }

  // Handle empty data state
  if (!data || !data.current_year_data || !data.previous_year_data) {
    return (
      <div className="bg-white rounded-lg shadow-md p-4 sm:p-6 border border-gray-200 min-h-[16rem] sm:min-h-[20rem] lg:min-h-[24rem]">
        <h3 className="text-lg sm:text-xl font-semibold mb-3 sm:mb-4 text-gray-800">
          Year-over-Year Emissions
        </h3>
        <EmptyState
          message="No data available"
          description="There is no emission data available for the selected years."
        />
      </div>
    );
  }

  // Transform API data for Recharts format
  const chartData = [
    {
      year: data.previous_year.toString(),
      "Scope 1":
        data.previous_year_data.find((s) => s.scope === 1)?.total_emissions ||
        0,
      "Scope 2":
        data.previous_year_data.find((s) => s.scope === 2)?.total_emissions ||
        0,
      "Scope 3":
        data.previous_year_data.find((s) => s.scope === 3)?.total_emissions ||
        0,
    },
    {
      year: data.current_year.toString(),
      "Scope 1":
        data.current_year_data.find((s) => s.scope === 1)?.total_emissions || 0,
      "Scope 2":
        data.current_year_data.find((s) => s.scope === 2)?.total_emissions || 0,
      "Scope 3":
        data.current_year_data.find((s) => s.scope === 3)?.total_emissions || 0,
    },
  ];

  // Calculate percentage change for display
  const changePercentage = data.comparison.change_percentage;
  const isIncrease = changePercentage > 0;

  return (
    <div
      className="bg-white rounded-lg shadow-md p-4 sm:p-6 border border-gray-200"
      role="region"
      aria-labelledby="yoy-chart-title"
    >
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-2 sm:gap-4 mb-3 sm:mb-4">
        <div className="flex-1 min-w-0">
          <h3
            id="yoy-chart-title"
            className="text-lg sm:text-xl font-semibold text-gray-800 truncate"
          >
            Year-over-Year Emissions
          </h3>
          <p className="text-xs sm:text-sm text-gray-600 mt-1">
            Comparison of emissions by scope
          </p>
        </div>
        <div className="text-left sm:text-right flex-shrink-0">
          <div
            className={`text-sm font-medium ${
              isIncrease ? "text-red-600" : "text-green-600"
            }`}
            aria-label={`Emissions ${
              isIncrease ? "increased" : "decreased"
            } by ${Math.abs(changePercentage).toFixed(
              1
            )} percent compared to previous year`}
          >
            {isIncrease ? "↑" : "↓"} {Math.abs(changePercentage).toFixed(1)}%
          </div>
          <div className="text-xs text-gray-500">vs previous year</div>
        </div>
      </div>

      {/* Screen reader description */}
      <div className="sr-only" role="status" aria-live="polite">
        Year-over-year emissions comparison chart. {data.previous_year} total
        emissions: {data.comparison.total_previous.toLocaleString()} kilograms
        CO2 equivalent. {data.current_year} total emissions:{" "}
        {data.comparison.total_current.toLocaleString()} kilograms CO2
        equivalent. This represents a {isIncrease ? "increase" : "decrease"} of{" "}
        {Math.abs(changePercentage).toFixed(1)} percent. The chart shows
        emissions broken down by Scope 1, Scope 2, and Scope 3 for both years.
      </div>

      <div
        role="img"
        aria-label="Bar chart comparing year-over-year emissions by scope"
      >
        <ResponsiveContainer
          width="100%"
          height={300}
          className="sm:!h-[350px]"
        >
          <BarChart
            data={chartData}
            margin={{
              top: 10,
              right: 10,
              left: 0,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis
              dataKey="year"
              tick={{ fill: "#6b7280" }}
              axisLine={{ stroke: "#d1d5db" }}
            />
            <YAxis
              label={{
                value: "Emissions (kgCO2e)",
                angle: -90,
                position: "insideLeft",
                style: { fill: "#6b7280" },
              }}
              tick={{ fill: "#6b7280" }}
              axisLine={{ stroke: "#d1d5db" }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend
              wrapperStyle={{ paddingTop: "20px" }}
              iconType="square"
              formatter={(value) => <span className="text-sm">{value}</span>}
            />
            <Bar
              dataKey="Scope 1"
              stackId="a"
              fill="#ef4444"
              name="Scope 1"
              radius={[0, 0, 0, 0]}
            />
            <Bar
              dataKey="Scope 2"
              stackId="a"
              fill="#3b82f6"
              name="Scope 2"
              radius={[0, 0, 0, 0]}
            />
            <Bar
              dataKey="Scope 3"
              stackId="a"
              fill="#10b981"
              name="Scope 3"
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-3 sm:mt-4 pt-3 sm:pt-4 border-t border-gray-200">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-4 text-xs sm:text-sm">
          <div className="flex flex-wrap items-baseline gap-1">
            <span className="text-gray-600">{data.previous_year} Total:</span>
            <span className="font-semibold text-gray-900">
              {data.comparison.total_previous.toLocaleString()} kgCO2e
            </span>
          </div>
          <div className="flex flex-wrap items-baseline gap-1">
            <span className="text-gray-600">{data.current_year} Total:</span>
            <span className="font-semibold text-gray-900">
              {data.comparison.total_current.toLocaleString()} kgCO2e
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default YoYChart;
