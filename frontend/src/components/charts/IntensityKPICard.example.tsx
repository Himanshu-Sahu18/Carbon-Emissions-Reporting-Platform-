/**
 * Example usage of IntensityKPICard component
 * This file demonstrates how to integrate the component with the useAnalytics hook
 */

import React from "react";
import IntensityKPICard from "./IntensityKPICard";
import { useAnalytics } from "../../hooks/useAnalytics";

/**
 * Example: Using IntensityKPICard with useAnalytics hook
 */
export const IntensityKPICardExample: React.FC = () => {
  const { intensityData, loading, error, refresh } = useAnalytics();

  return (
    <div className="p-4">
      <IntensityKPICard
        data={intensityData}
        loading={loading}
        error={error}
        startDate={new Date("2024-01-01")}
        endDate={new Date("2024-03-31")}
        metricName="Tons of Steel Produced"
        onRefresh={refresh}
      />
    </div>
  );
};

/**
 * Example: Using IntensityKPICard with custom data
 */
export const IntensityKPICardWithCustomData: React.FC = () => {
  const customData = {
    period: {
      start_date: "2024-01-01",
      end_date: "2024-03-31",
    },
    metric_name: "Tons of Steel Produced",
    total_emissions: 125000,
    total_production: 150000,
    production_unit: "tons",
    intensity: 0.833,
    intensity_unit: "kgCO2e per ton",
    record_count: 52,
  };

  return (
    <div className="p-4">
      <IntensityKPICard
        data={customData}
        loading={false}
        error={null}
        startDate={new Date("2024-01-01")}
        endDate={new Date("2024-03-31")}
        metricName="Tons of Steel Produced"
      />
    </div>
  );
};

/**
 * Example: Grid layout with multiple KPI cards
 */
export const IntensityKPICardGrid: React.FC = () => {
  const { intensityData, loading, error, refresh } = useAnalytics();

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-4">
      <IntensityKPICard
        data={intensityData}
        loading={loading}
        error={error}
        startDate={new Date("2024-01-01")}
        endDate={new Date("2024-03-31")}
        metricName="Tons of Steel Produced"
        onRefresh={refresh}
      />
      {/* Add more KPI cards here for different metrics */}
    </div>
  );
};
