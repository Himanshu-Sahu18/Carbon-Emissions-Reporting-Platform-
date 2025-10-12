import MonthlyTrendChart from "./MonthlyTrendChart";
import type { MonthlyEmissionsResponse } from "../../types/api.types";

/**
 * Example usage of MonthlyTrendChart component
 * This file demonstrates various use cases and states
 */

// Example 1: With full year data
export function MonthlyTrendChartFullYear() {
  const fullYearData: MonthlyEmissionsResponse = {
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
      { month: 5, month_name: "May", total_emissions: 51000, record_count: 13 },
      {
        month: 6,
        month_name: "June",
        total_emissions: 58000,
        record_count: 18,
      },
      {
        month: 7,
        month_name: "July",
        total_emissions: 62000,
        record_count: 19,
      },
      {
        month: 8,
        month_name: "August",
        total_emissions: 59000,
        record_count: 17,
      },
      {
        month: 9,
        month_name: "September",
        total_emissions: 54000,
        record_count: 15,
      },
      {
        month: 10,
        month_name: "October",
        total_emissions: 50000,
        record_count: 14,
      },
      {
        month: 11,
        month_name: "November",
        total_emissions: 47000,
        record_count: 13,
      },
      {
        month: 12,
        month_name: "December",
        total_emissions: 44000,
        record_count: 12,
      },
    ],
  };

  return <MonthlyTrendChart data={fullYearData} loading={false} error={null} />;
}

// Example 2: With partial year data (Q1 only)
export function MonthlyTrendChartPartialYear() {
  const partialYearData: MonthlyEmissionsResponse = {
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
    ],
  };

  return (
    <MonthlyTrendChart data={partialYearData} loading={false} error={null} />
  );
}

// Example 3: With gaps in data
export function MonthlyTrendChartWithGaps() {
  const dataWithGaps: MonthlyEmissionsResponse = {
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
      { month: 5, month_name: "May", total_emissions: 51000, record_count: 13 },
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
  };

  return <MonthlyTrendChart data={dataWithGaps} loading={false} error={null} />;
}

// Example 4: Loading state
export function MonthlyTrendChartLoading() {
  return <MonthlyTrendChart data={null} loading={true} error={null} />;
}

// Example 5: Error state
export function MonthlyTrendChartError() {
  const handleRetry = () => {
    console.log("Retry clicked");
    // Implement retry logic
  };

  return (
    <MonthlyTrendChart
      data={null}
      loading={false}
      error={new Error("Failed to fetch monthly emissions data")}
      onRefresh={handleRetry}
    />
  );
}

// Example 6: Empty state
export function MonthlyTrendChartEmpty() {
  const emptyData: MonthlyEmissionsResponse = {
    year: 2024,
    months: [],
  };

  return <MonthlyTrendChart data={emptyData} loading={false} error={null} />;
}

// Example 7: With useAnalytics hook (recommended)
export function MonthlyTrendChartWithHook() {
  // This example shows how to use the component with the useAnalytics hook
  // Uncomment the following lines to use in a real application:

  // import { useAnalytics } from "../../hooks/useAnalytics";
  //
  // const { monthlyData, loading, error, refresh } = useAnalytics();
  //
  // return (
  //   <MonthlyTrendChart
  //     data={monthlyData}
  //     loading={loading}
  //     error={error}
  //     onRefresh={refresh}
  //   />
  // );

  // For this example, we'll use mock data
  const mockData: MonthlyEmissionsResponse = {
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
    ],
  };

  return <MonthlyTrendChart data={mockData} loading={false} error={null} />;
}

// Example 8: Increasing trend
export function MonthlyTrendChartIncreasing() {
  const increasingData: MonthlyEmissionsResponse = {
    year: 2024,
    months: [
      {
        month: 1,
        month_name: "January",
        total_emissions: 30000,
        record_count: 10,
      },
      {
        month: 2,
        month_name: "February",
        total_emissions: 35000,
        record_count: 11,
      },
      {
        month: 3,
        month_name: "March",
        total_emissions: 40000,
        record_count: 12,
      },
      {
        month: 4,
        month_name: "April",
        total_emissions: 45000,
        record_count: 13,
      },
      { month: 5, month_name: "May", total_emissions: 50000, record_count: 14 },
      {
        month: 6,
        month_name: "June",
        total_emissions: 55000,
        record_count: 15,
      },
    ],
  };

  return (
    <MonthlyTrendChart data={increasingData} loading={false} error={null} />
  );
}

// Example 9: Decreasing trend
export function MonthlyTrendChartDecreasing() {
  const decreasingData: MonthlyEmissionsResponse = {
    year: 2024,
    months: [
      {
        month: 1,
        month_name: "January",
        total_emissions: 60000,
        record_count: 18,
      },
      {
        month: 2,
        month_name: "February",
        total_emissions: 55000,
        record_count: 16,
      },
      {
        month: 3,
        month_name: "March",
        total_emissions: 50000,
        record_count: 14,
      },
      {
        month: 4,
        month_name: "April",
        total_emissions: 45000,
        record_count: 13,
      },
      { month: 5, month_name: "May", total_emissions: 40000, record_count: 12 },
      {
        month: 6,
        month_name: "June",
        total_emissions: 35000,
        record_count: 10,
      },
    ],
  };

  return (
    <MonthlyTrendChart data={decreasingData} loading={false} error={null} />
  );
}

// Example 10: All examples in a grid
export function MonthlyTrendChartExamples() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          MonthlyTrendChart Examples
        </h1>

        <div className="space-y-8">
          <div>
            <h2 className="text-xl font-semibold mb-4">Full Year Data</h2>
            <MonthlyTrendChartFullYear />
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-4">Partial Year (Q1)</h2>
            <MonthlyTrendChartPartialYear />
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-4">Data with Gaps</h2>
            <MonthlyTrendChartWithGaps />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h2 className="text-xl font-semibold mb-4">Increasing Trend</h2>
              <MonthlyTrendChartIncreasing />
            </div>

            <div>
              <h2 className="text-xl font-semibold mb-4">Decreasing Trend</h2>
              <MonthlyTrendChartDecreasing />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h2 className="text-xl font-semibold mb-4">Loading State</h2>
              <MonthlyTrendChartLoading />
            </div>

            <div>
              <h2 className="text-xl font-semibold mb-4">Error State</h2>
              <MonthlyTrendChartError />
            </div>

            <div>
              <h2 className="text-xl font-semibold mb-4">Empty State</h2>
              <MonthlyTrendChartEmpty />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default MonthlyTrendChartExamples;
