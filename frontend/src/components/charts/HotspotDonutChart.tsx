import React from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import type { HotspotDonutChartProps } from "../../types/component.types";
import LoadingSpinner from "../common/LoadingSpinner";
import ErrorMessage from "../common/ErrorMessage";
import EmptyState from "../common/EmptyState";

// Color palette for emission sources
const COLORS = [
  "#ef4444", // red
  "#3b82f6", // blue
  "#10b981", // green
  "#f59e0b", // amber
  "#8b5cf6", // violet
  "#ec4899", // pink
  "#14b8a6", // teal
  "#f97316", // orange
  "#6366f1", // indigo
  "#84cc16", // lime
];

/**
 * Custom tooltip component for the donut chart
 */
const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-lg">
        <p className="font-semibold text-gray-900 mb-2">{data.activity_name}</p>
        <p className="text-sm text-gray-700">
          <span className="font-medium">Emissions:</span>{" "}
          {data.total_emissions.toLocaleString()} kgCO2e
        </p>
        <p className="text-sm text-gray-700">
          <span className="font-medium">Percentage:</span>{" "}
          {data.percentage.toFixed(1)}%
        </p>
        <p className="text-sm text-gray-500 mt-1">
          {data.record_count} record{data.record_count !== 1 ? "s" : ""}
        </p>
      </div>
    );
  }
  return null;
};

/**
 * Custom label component to display percentage on chart
 */
const renderCustomLabel = ({
  cx,
  cy,
  midAngle,
  innerRadius,
  outerRadius,
  percent,
}: any) => {
  const RADIAN = Math.PI / 180;
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);

  // Only show label if percentage is significant enough
  if (percent < 0.05) return null;

  return (
    <text
      x={x}
      y={y}
      fill="white"
      textAnchor={x > cx ? "start" : "end"}
      dominantBaseline="central"
      className="text-xs font-semibold"
    >
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  );
};

/**
 * Emission Hotspot Donut Chart Component
 * Displays a donut chart showing percentage breakdown of emissions by source
 */
const HotspotDonutChart: React.FC<HotspotDonutChartProps> = ({
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
          Emission Hotspots
        </h3>
        <ErrorMessage message={error.message} onRetry={onRefresh} />
      </div>
    );
  }

  // Handle empty data state
  if (!data || !data.hotspots || data.hotspots.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-4 sm:p-6 border border-gray-200 min-h-[16rem] sm:min-h-[20rem] lg:min-h-[24rem]">
        <h3 className="text-lg sm:text-xl font-semibold mb-3 sm:mb-4 text-gray-800">
          Emission Hotspots
        </h3>
        <EmptyState
          message="No emission data available"
          description="There are no emission hotspots to display for the selected period."
        />
      </div>
    );
  }

  // Transform API data for Recharts PieChart format
  const chartData = data.hotspots.map((hotspot) => ({
    activity_name: hotspot.activity_name,
    total_emissions: hotspot.total_emissions,
    percentage: hotspot.percentage,
    record_count: hotspot.record_count,
    scope: hotspot.scope,
  }));

  // Generate screen reader description
  const screenReaderDescription = `Emission hotspots donut chart showing ${
    data.hotspots.length
  } emission sources. Total emissions: ${data.total_emissions.toLocaleString()} kilograms CO2 equivalent. ${data.hotspots
    .slice(0, 3)
    .map(
      (h) =>
        `${
          h.activity_name
        }: ${h.total_emissions.toLocaleString()} kilograms CO2 equivalent, ${h.percentage.toFixed(
          1
        )} percent`
    )
    .join(". ")}${data.hotspots.length > 3 ? ". And more sources." : "."}`;

  return (
    <div
      className="bg-white rounded-lg shadow-md p-4 sm:p-6 border border-gray-200"
      role="region"
      aria-labelledby="hotspot-chart-title"
    >
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-2 sm:gap-4 mb-3 sm:mb-4">
        <div className="flex-1 min-w-0">
          <h3
            id="hotspot-chart-title"
            className="text-lg sm:text-xl font-semibold text-gray-800 truncate"
          >
            Emission Hotspots
          </h3>
          <p className="text-xs sm:text-sm text-gray-600 mt-1">
            Top emission sources by activity
          </p>
        </div>
        <div className="text-left sm:text-right flex-shrink-0">
          <div
            className="text-sm font-medium text-gray-700"
            aria-label={`${data.hotspots.length} emission source${
              data.hotspots.length !== 1 ? "s" : ""
            }`}
          >
            {data.hotspots.length} source{data.hotspots.length !== 1 ? "s" : ""}
          </div>
          <div className="text-xs text-gray-500">
            {data.period.start_date && data.period.end_date
              ? `${data.period.start_date} to ${data.period.end_date}`
              : "All time"}
          </div>
        </div>
      </div>

      {/* Screen reader description */}
      <div className="sr-only" role="status" aria-live="polite">
        {screenReaderDescription}
      </div>

      <div
        role="img"
        aria-label="Donut chart showing emission hotspots by activity"
      >
        <ResponsiveContainer
          width="100%"
          height={280}
          className="sm:!h-[320px] lg:!h-[350px]"
        >
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={renderCustomLabel}
              outerRadius={
                window.innerWidth < 640
                  ? 80
                  : window.innerWidth < 1024
                  ? 100
                  : 120
              }
              innerRadius={
                window.innerWidth < 640
                  ? 50
                  : window.innerWidth < 1024
                  ? 60
                  : 70
              }
              fill="#8884d8"
              dataKey="total_emissions"
              paddingAngle={2}
            >
              {chartData.map((_entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={COLORS[index % COLORS.length]}
                />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend
              verticalAlign="bottom"
              height={36}
              iconType="circle"
              formatter={(value) => (
                <span className="text-sm text-gray-700">{value}</span>
              )}
              wrapperStyle={{ paddingTop: "20px" }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Center label overlay - Responsive */}
      <div className="relative -mt-[280px] sm:-mt-[320px] lg:-mt-[350px] h-[280px] sm:h-[320px] lg:h-[350px] pointer-events-none flex items-center justify-center">
        <div className="text-center">
          <div className="text-xl sm:text-2xl lg:text-3xl font-bold text-gray-900">
            {data.total_emissions.toLocaleString()}
          </div>
          <div className="text-xs sm:text-sm text-gray-600 mt-1">kgCO2e</div>
          <div className="text-xs text-gray-500 mt-1">Total</div>
        </div>
      </div>

      <div className="mt-3 sm:mt-4 pt-3 sm:pt-4 border-t border-gray-200">
        <div className="text-xs sm:text-sm text-gray-600">
          <span className="font-medium">Top contributor:</span>{" "}
          <span className="break-words">
            {data.hotspots[0].activity_name} (
            {data.hotspots[0].percentage.toFixed(1)}%)
          </span>
        </div>
      </div>
    </div>
  );
};

export default HotspotDonutChart;
