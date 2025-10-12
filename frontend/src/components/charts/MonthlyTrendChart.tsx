import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import type { MonthlyTrendChartProps } from "../../types/component.types";
import LoadingSpinner from "../common/LoadingSpinner";
import ErrorMessage from "../common/ErrorMessage";
import EmptyState from "../common/EmptyState";

/**
 * Custom tooltip component for the Monthly Trend chart
 */
const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-lg">
        <p className="font-semibold text-gray-900 mb-2">{label}</p>
        {payload.map((entry: any, index: number) => (
          <p key={index} className="text-sm" style={{ color: entry.color }}>
            <span className="font-medium">Emissions:</span>{" "}
            {entry.value?.toLocaleString()} kgCO2e
          </p>
        ))}
      </div>
    );
  }
  return null;
};

/**
 * Monthly Emissions Trend Line Chart Component
 * Displays a line chart tracking total monthly emissions over the current year
 */
const MonthlyTrendChart: React.FC<MonthlyTrendChartProps> = ({
  data,
  loading = false,
  error = null,
  year,
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
          Monthly Emissions Trend
        </h3>
        <ErrorMessage message={error.message} onRetry={onRefresh} />
      </div>
    );
  }

  // Handle empty data state
  if (!data || !data.months || data.months.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-4 sm:p-6 border border-gray-200 min-h-[16rem] sm:min-h-[20rem] lg:min-h-[24rem]">
        <h3 className="text-lg sm:text-xl font-semibold mb-3 sm:mb-4 text-gray-800">
          Monthly Emissions Trend
        </h3>
        <EmptyState
          message="No data available"
          description="There is no monthly emission data available for the selected year."
        />
      </div>
    );
  }

  // Transform API data for Recharts format
  // Create array with all 12 months, filling in missing data with null
  const monthNames = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];

  const chartData = monthNames.map((monthName, index) => {
    const monthNumber = index + 1;
    const monthData = data.months.find((m) => m.month === monthNumber);

    return {
      month: monthName,
      monthNumber: monthNumber,
      emissions: monthData ? monthData.total_emissions : null,
      recordCount: monthData ? monthData.record_count : 0,
    };
  });

  // Calculate statistics
  const totalEmissions = data.months.reduce(
    (sum, month) => sum + month.total_emissions,
    0
  );
  const averageEmissions =
    data.months.length > 0 ? totalEmissions / data.months.length : 0;
  const maxEmissions = Math.max(
    ...data.months.map((m) => m.total_emissions),
    0
  );
  const minEmissions = Math.min(
    ...data.months.map((m) => m.total_emissions),
    Infinity
  );

  // Calculate trend (simple linear regression slope)
  const calculateTrend = () => {
    const validData = chartData.filter((d) => d.emissions !== null);
    if (validData.length < 2) return 0;

    const n = validData.length;
    const sumX = validData.reduce((sum, d) => sum + d.monthNumber, 0);
    const sumY = validData.reduce((sum, d) => sum + (d.emissions || 0), 0);
    const sumXY = validData.reduce(
      (sum, d) => sum + d.monthNumber * (d.emissions || 0),
      0
    );
    const sumX2 = validData.reduce((sum, d) => sum + d.monthNumber ** 2, 0);

    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX ** 2);
    return slope;
  };

  const trend = calculateTrend();
  const isIncreasing = trend > 0;

  return (
    <div
      className="bg-white rounded-lg shadow-md p-4 sm:p-6 border border-gray-200"
      role="region"
      aria-labelledby="monthly-trend-title"
    >
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-2 sm:gap-4 mb-3 sm:mb-4">
        <div className="flex-1 min-w-0">
          <h3
            id="monthly-trend-title"
            className="text-lg sm:text-xl font-semibold text-gray-800 truncate"
          >
            Monthly Emissions Trend
          </h3>
          <p className="text-xs sm:text-sm text-gray-600 mt-1">
            {year || data.year} emissions by month
          </p>
        </div>
        <div className="text-left sm:text-right flex-shrink-0">
          <div
            className={`text-sm font-medium ${
              isIncreasing ? "text-red-600" : "text-green-600"
            }`}
            aria-label={`Emissions trend is ${
              isIncreasing ? "increasing" : "decreasing"
            } over time`}
          >
            {isIncreasing ? "↑" : "↓"}{" "}
            {isIncreasing ? "Increasing" : "Decreasing"}
          </div>
          <div className="text-xs text-gray-500">trend</div>
        </div>
      </div>

      {/* Screen reader description */}
      <div className="sr-only" role="status" aria-live="polite">
        Monthly emissions trend chart for {year || data.year}. Total emissions:{" "}
        {totalEmissions.toLocaleString()} kilograms CO2 equivalent. Average
        monthly emissions:{" "}
        {averageEmissions.toLocaleString(undefined, {
          maximumFractionDigits: 0,
        })}{" "}
        kilograms CO2 equivalent. Peak month: {maxEmissions.toLocaleString()}{" "}
        kilograms CO2 equivalent. The trend is{" "}
        {isIncreasing ? "increasing" : "decreasing"} over the year.
      </div>

      <div role="img" aria-label="Line chart showing monthly emissions trend">
        <ResponsiveContainer
          width="100%"
          height={300}
          className="sm:!h-[350px]"
        >
          <LineChart
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
              dataKey="month"
              tick={{ fill: "#6b7280" }}
              axisLine={{ stroke: "#d1d5db" }}
              label={{
                value: "Month",
                position: "insideBottom",
                offset: -5,
                style: { fill: "#6b7280" },
              }}
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
              iconType="line"
              formatter={(value) => <span className="text-sm">{value}</span>}
            />
            <Line
              type="monotone"
              dataKey="emissions"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={{ fill: "#3b82f6", r: 4 }}
              activeDot={{ r: 6 }}
              name="Monthly Emissions"
              connectNulls={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-3 sm:mt-4 pt-3 sm:pt-4 border-t border-gray-200">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-2 sm:gap-4 text-xs sm:text-sm">
          <div className="flex flex-col sm:flex-row sm:items-baseline gap-1">
            <span className="text-gray-600">Total:</span>
            <span className="font-semibold text-gray-900">
              {totalEmissions.toLocaleString()} kgCO2e
            </span>
          </div>
          <div className="flex flex-col sm:flex-row sm:items-baseline gap-1">
            <span className="text-gray-600">Average:</span>
            <span className="font-semibold text-gray-900">
              {averageEmissions.toLocaleString(undefined, {
                maximumFractionDigits: 0,
              })}{" "}
              kgCO2e
            </span>
          </div>
          <div className="flex flex-col sm:flex-row sm:items-baseline gap-1">
            <span className="text-gray-600">Peak:</span>
            <span className="font-semibold text-gray-900">
              {maxEmissions.toLocaleString()} kgCO2e
            </span>
          </div>
          <div className="flex flex-col sm:flex-row sm:items-baseline gap-1">
            <span className="text-gray-600">Lowest:</span>
            <span className="font-semibold text-gray-900">
              {minEmissions === Infinity
                ? "N/A"
                : minEmissions.toLocaleString()}{" "}
              {minEmissions !== Infinity && "kgCO2e"}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MonthlyTrendChart;
