import React from "react";
import { YoYChart } from "./components/charts";
import { useAnalytics } from "./hooks/useAnalytics";

/**
 * Test component to verify YoYChart integration with useAnalytics hook
 */
const TestYoYChart: React.FC = () => {
  const { yoyData, loading, error, refresh } = useAnalytics();

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Year-over-Year Chart Test
        </h1>
        <YoYChart
          data={yoyData}
          loading={loading}
          error={error}
          onRefresh={refresh}
        />
      </div>
    </div>
  );
};

export default TestYoYChart;
