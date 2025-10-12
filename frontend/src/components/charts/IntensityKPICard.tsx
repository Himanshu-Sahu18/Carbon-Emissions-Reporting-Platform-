import React from "react";
import type { IntensityKPICardProps } from "../../types/component.types";
import LoadingSpinner from "../common/LoadingSpinner";
import ErrorMessage from "../common/ErrorMessage";
import EmptyState from "../common/EmptyState";

/**
 * Determine color coding based on intensity value
 * This is a simple heuristic - adjust thresholds based on industry standards
 */
const getIntensityColor = (intensity: number): string => {
  if (intensity < 0.5) return "text-green-600";
  if (intensity < 1.0) return "text-yellow-600";
  return "text-red-600";
};

const getIntensityBgColor = (intensity: number): string => {
  if (intensity < 0.5) return "bg-green-50 border-green-200";
  if (intensity < 1.0) return "bg-yellow-50 border-yellow-200";
  return "bg-red-50 border-red-200";
};

/**
 * Format date range for display
 */
const formatDateRange = (startDate: string, endDate: string): string => {
  const start = new Date(startDate);
  const end = new Date(endDate);

  const options: Intl.DateTimeFormatOptions = {
    month: "short",
    day: "numeric",
    year: "numeric",
  };

  return `${start.toLocaleDateString(
    "en-US",
    options
  )} - ${end.toLocaleDateString("en-US", options)}`;
};

/**
 * Emission Intensity KPI Card Component
 * Displays emission intensity metric prominently with supporting data
 */
const IntensityKPICard: React.FC<IntensityKPICardProps> = ({
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
          Emission Intensity
        </h3>
        <ErrorMessage message={error.message} onRetry={onRefresh} />
      </div>
    );
  }

  // Handle empty data state
  if (!data) {
    return (
      <div className="bg-white rounded-lg shadow-md p-4 sm:p-6 border border-gray-200 min-h-[16rem] sm:min-h-[20rem] lg:min-h-[24rem]">
        <h3 className="text-lg sm:text-xl font-semibold mb-3 sm:mb-4 text-gray-800">
          Emission Intensity
        </h3>
        <EmptyState
          message="No data available"
          description="There is no intensity data available for the selected period."
        />
      </div>
    );
  }

  // Handle case when production data is unavailable
  if (data.total_production === 0 || !data.total_production) {
    return (
      <div className="bg-white rounded-lg shadow-md p-4 sm:p-6 border border-gray-200 min-h-[16rem] sm:min-h-[20rem] lg:min-h-[24rem]">
        <h3 className="text-lg sm:text-xl font-semibold mb-3 sm:mb-4 text-gray-800">
          Emission Intensity
        </h3>
        <EmptyState
          message="Production data unavailable"
          description="Emission intensity cannot be calculated without production data. Please submit business metrics to enable this calculation."
        />
      </div>
    );
  }

  const intensityColor = getIntensityColor(data.intensity);
  const intensityBgColor = getIntensityBgColor(data.intensity);
  const dateRange = formatDateRange(
    data.period.start_date,
    data.period.end_date
  );

  // Determine intensity level for screen reader
  const intensityLevel =
    data.intensity < 0.5 ? "low" : data.intensity < 1.0 ? "medium" : "high";

  return (
    <div
      className="bg-white rounded-lg shadow-md p-4 sm:p-6 border border-gray-200"
      role="region"
      aria-labelledby="intensity-kpi-title"
    >
      <div className="mb-3 sm:mb-4">
        <h3
          id="intensity-kpi-title"
          className="text-lg sm:text-xl font-semibold text-gray-800 truncate"
        >
          Emission Intensity
        </h3>
        <p className="text-xs sm:text-sm text-gray-600 mt-1 truncate">
          {data.metric_name}
        </p>
      </div>

      {/* Screen reader description */}
      <div className="sr-only" role="status" aria-live="polite">
        Emission intensity KPI card. Current intensity is{" "}
        {data.intensity.toFixed(2)} {data.intensity_unit}, which is considered{" "}
        {intensityLevel} level. Period: {dateRange}. Total emissions:{" "}
        {data.total_emissions.toLocaleString()} kilograms CO2 equivalent. Total
        production: {data.total_production.toLocaleString()}{" "}
        {data.production_unit}.
      </div>

      {/* Main KPI Display - Responsive */}
      <div
        className={`${intensityBgColor} rounded-lg p-4 sm:p-6 mb-4 sm:mb-6 border-2 transition-colors`}
        role="status"
        aria-label={`Emission intensity: ${data.intensity.toFixed(2)} ${
          data.intensity_unit
        }, ${intensityLevel} level`}
      >
        <div className="text-center">
          <div
            className={`text-4xl sm:text-5xl lg:text-6xl font-bold ${intensityColor} mb-2`}
            aria-hidden="true"
          >
            {data.intensity.toFixed(2)}
          </div>
          <div
            className="text-sm sm:text-base lg:text-lg text-gray-700 font-medium break-words"
            aria-hidden="true"
          >
            {data.intensity_unit}
          </div>
        </div>
      </div>

      {/* Date Range - Responsive */}
      <div className="mb-4 sm:mb-6 pb-3 sm:pb-4 border-b border-gray-200">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-center gap-1 sm:gap-2 text-xs sm:text-sm text-gray-600">
          <div className="flex items-center justify-center sm:justify-start">
            <svg
              className="h-4 w-4 mr-2 flex-shrink-0"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
            <span className="font-medium">Period:</span>
          </div>
          <span className="text-center sm:text-left break-words">
            {dateRange}
          </span>
        </div>
      </div>

      {/* Supporting Metrics - Responsive */}
      <div className="space-y-3 sm:space-y-4">
        <div className="flex justify-between items-center gap-2">
          <span className="text-xs sm:text-sm text-gray-600">
            Total Emissions
          </span>
          <span className="text-xs sm:text-sm font-semibold text-gray-900 text-right">
            {data.total_emissions.toLocaleString()} kgCO2e
          </span>
        </div>

        <div className="flex justify-between items-center gap-2">
          <span className="text-xs sm:text-sm text-gray-600">
            Total Production
          </span>
          <span className="text-xs sm:text-sm font-semibold text-gray-900 text-right break-words">
            {data.total_production.toLocaleString()} {data.production_unit}
          </span>
        </div>

        <div className="flex justify-between items-center gap-2 pt-2 border-t border-gray-100">
          <span className="text-xs sm:text-sm text-gray-600">Data Points</span>
          <span className="text-xs sm:text-sm font-semibold text-gray-900">
            {data.record_count} records
          </span>
        </div>
      </div>

      {/* Intensity Level Indicator - Responsive */}
      <div className="mt-4 sm:mt-6 pt-3 sm:pt-4 border-t border-gray-200">
        <div className="flex items-center justify-center">
          <div className="flex flex-col sm:flex-row items-center gap-2 text-xs">
            <div className="flex items-center">
              <div className="w-3 h-3 rounded-full bg-green-500 mr-1 flex-shrink-0"></div>
              <span className="text-gray-600 whitespace-nowrap">
                Low (&lt;0.5)
              </span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 rounded-full bg-yellow-500 mr-1 flex-shrink-0"></div>
              <span className="text-gray-600 whitespace-nowrap">
                Medium (0.5-1.0)
              </span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 rounded-full bg-red-500 mr-1 flex-shrink-0"></div>
              <span className="text-gray-600 whitespace-nowrap">
                High (&gt;1.0)
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default IntensityKPICard;
