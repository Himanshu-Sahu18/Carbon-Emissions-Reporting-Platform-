import React from "react";
import Header from "./Header";
import ErrorBoundary from "../common/ErrorBoundary";
import LoadingSpinner from "../common/LoadingSpinner";
import ErrorMessage from "../common/ErrorMessage";
import SkipToMain from "../common/SkipToMain";
import EmissionForm from "../forms/EmissionForm";
import MetricsForm from "../forms/MetricsForm";
import YoYChart from "../charts/YoYChart";
import HotspotDonutChart from "../charts/HotspotDonutChart";
import IntensityKPICard from "../charts/IntensityKPICard";
import MonthlyTrendChart from "../charts/MonthlyTrendChart";
import { useAnalytics } from "../../hooks";

const DashboardLayout: React.FC = () => {
  const {
    yoyData,
    intensityData,
    hotspotsData,
    monthlyData,
    loading,
    refreshing,
    error,
    refresh,
  } = useAnalytics();

  const handleFormSuccess = () => {
    // Auto-refresh dashboard after successful form submission
    refresh();
  };

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gray-50">
        {/* Skip to main content link for keyboard navigation */}
        <SkipToMain />

        {/* Header */}
        <Header onRefresh={refresh} isRefreshing={refreshing} />

        {/* Main Content */}
        <main
          id="main-content"
          className="container mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6 lg:py-8"
          role="main"
          tabIndex={-1}
        >
          {/* Global Error State */}
          {error && (
            <div className="mb-4 sm:mb-6">
              <ErrorMessage
                message={error.message || "Failed to load dashboard data"}
                onRetry={refresh}
              />
            </div>
          )}

          {/* Dashboard Grid Layout - Responsive */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 sm:gap-6 lg:gap-8">
            {/* Data Entry Section - Stacked on mobile, sidebar on desktop */}
            <aside
              className="lg:col-span-4 xl:col-span-3 space-y-4 sm:space-y-6"
              aria-label="Data entry forms"
            >
              <section aria-labelledby="emission-form-title">
                <h2
                  id="emission-form-title"
                  className="text-base sm:text-lg font-semibold text-gray-900 mb-3 sm:mb-4"
                >
                  Submit Emissions Data
                </h2>
                <EmissionForm onSuccess={handleFormSuccess} />
              </section>

              <section aria-labelledby="metrics-form-title">
                <h2
                  id="metrics-form-title"
                  className="text-base sm:text-lg font-semibold text-gray-900 mb-3 sm:mb-4"
                >
                  Submit Business Metrics
                </h2>
                <MetricsForm onSuccess={handleFormSuccess} />
              </section>
            </aside>

            {/* Visualization Section - Main Content Area */}
            <section
              className="lg:col-span-8 xl:col-span-9 space-y-4 sm:space-y-6"
              aria-labelledby="visualizations-title"
            >
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 sm:gap-4 mb-3 sm:mb-4">
                <h2
                  id="visualizations-title"
                  className="text-base sm:text-lg font-semibold text-gray-900"
                >
                  Analytics & Insights
                </h2>
                {/* Refreshing indicator */}
                {refreshing && (
                  <div className="flex items-center text-xs sm:text-sm text-gray-600">
                    <LoadingSpinner size="sm" />
                    <span className="ml-2">Updating data...</span>
                  </div>
                )}
              </div>

              {/* Visualizations Grid - Responsive layout */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
                {/* Year-over-Year Chart - Full width on mobile and tablet */}
                <div className="col-span-1 md:col-span-2">
                  <YoYChart
                    data={yoyData}
                    loading={loading && !refreshing}
                    error={error}
                    onRefresh={refresh}
                  />
                </div>

                {/* Hotspot Donut Chart - Full width on mobile, half on tablet+ */}
                <div className="col-span-1">
                  <HotspotDonutChart
                    data={hotspotsData}
                    loading={loading && !refreshing}
                    error={error}
                    onRefresh={refresh}
                  />
                </div>

                {/* Intensity KPI Card - Full width on mobile, half on tablet+ */}
                <div className="col-span-1">
                  <IntensityKPICard
                    data={intensityData}
                    loading={loading && !refreshing}
                    error={error}
                    onRefresh={refresh}
                    startDate={new Date(new Date().getFullYear(), 0, 1)}
                    endDate={new Date()}
                    metricName="Tons of Steel Produced"
                  />
                </div>

                {/* Monthly Trend Chart - Full width on mobile and tablet */}
                <div className="col-span-1 md:col-span-2">
                  <MonthlyTrendChart
                    data={monthlyData}
                    loading={loading && !refreshing}
                    error={error}
                    onRefresh={refresh}
                  />
                </div>
              </div>
            </section>
          </div>
        </main>

        {/* Footer */}
        <footer className="bg-white border-t border-gray-200 mt-12">
          <div className="container mx-auto px-4 py-6">
            <p className="text-center text-sm text-gray-600">
              Carbon Emissions Tracking Platform &copy;{" "}
              {new Date().getFullYear()}
            </p>
          </div>
        </footer>
      </div>
    </ErrorBoundary>
  );
};

export default DashboardLayout;
