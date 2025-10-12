import React from "react";
import { HotspotDonutChart } from "./components/charts";
import { useAnalytics } from "./hooks";

/**
 * Test component for HotspotDonutChart
 * This demonstrates the component with real data from the useAnalytics hook
 */
const TestHotspotChart: React.FC = () => {
  const { hotspotsData, loading, error, refresh } = useAnalytics();

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Hotspot Donut Chart Test
        </h1>

        <div className="mb-8">
          <HotspotDonutChart
            data={hotspotsData}
            loading={loading}
            error={error}
            onRefresh={refresh}
          />
        </div>

        {/* Debug info */}
        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
          <h2 className="text-xl font-semibold mb-4">Debug Information</h2>
          <div className="space-y-2 text-sm">
            <div>
              <span className="font-medium">Loading:</span>{" "}
              {loading ? "Yes" : "No"}
            </div>
            <div>
              <span className="font-medium">Error:</span>{" "}
              {error ? error.message : "None"}
            </div>
            <div>
              <span className="font-medium">Data Available:</span>{" "}
              {hotspotsData ? "Yes" : "No"}
            </div>
            {hotspotsData && (
              <>
                <div>
                  <span className="font-medium">Total Emissions:</span>{" "}
                  {hotspotsData.total_emissions.toLocaleString()} kgCO2e
                </div>
                <div>
                  <span className="font-medium">Number of Hotspots:</span>{" "}
                  {hotspotsData.hotspots.length}
                </div>
                <div className="mt-4">
                  <span className="font-medium">Hotspots:</span>
                  <pre className="mt-2 p-4 bg-gray-50 rounded overflow-auto text-xs">
                    {JSON.stringify(hotspotsData.hotspots, null, 2)}
                  </pre>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TestHotspotChart;
