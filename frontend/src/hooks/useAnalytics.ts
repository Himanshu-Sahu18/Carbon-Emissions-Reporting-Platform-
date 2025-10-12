import { useState, useEffect, useCallback } from "react";
import analyticsService from "../services/analyticsService";
import type { UseAnalyticsReturn } from "../types/hook.types";

/**
 * Custom hook for fetching and managing analytics data
 * Fetches YoY, intensity, hotspots, and monthly emissions data
 *
 * @returns Analytics data, loading state, error state, and refresh function
 */
export function useAnalytics(): UseAnalyticsReturn {
  const [yoyData, setYoyData] = useState<UseAnalyticsReturn["yoyData"]>(null);
  const [intensityData, setIntensityData] =
    useState<UseAnalyticsReturn["intensityData"]>(null);
  const [hotspotsData, setHotspotsData] =
    useState<UseAnalyticsReturn["hotspotsData"]>(null);
  const [monthlyData, setMonthlyData] =
    useState<UseAnalyticsReturn["monthlyData"]>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  /**
   * Fetch all analytics data from the API
   * @param isRefresh - Whether this is a refresh operation (vs initial load)
   */
  const fetchData = useCallback(async (isRefresh = false) => {
    if (isRefresh) {
      setRefreshing(true);
    } else {
      setLoading(true);
    }
    setError(null);

    try {
      // Get current year for default parameters
      // Use 2024 as we have sample data for 2024
      const currentYear = 2024;
      const previousYear = 2023;
      const startOfYear = `${currentYear}-01-01`;
      const endOfYear = `${currentYear}-12-31`;

      // Fetch all data in parallel for better performance
      console.log(`Fetching YoY data for ${currentYear} vs ${previousYear}`);
      const [yoy, intensity, hotspots, monthly] = await Promise.all([
        analyticsService.getYoYEmissions(currentYear, previousYear),
        analyticsService.getEmissionIntensity(
          startOfYear,
          endOfYear,
          "Tons of Steel Produced"
        ),
        analyticsService.getEmissionHotspots({ limit: 10 }),
        analyticsService.getMonthlyEmissions(currentYear),
      ]);

      console.log("YoY data received:", yoy);
      setYoyData(yoy);
      setIntensityData(intensity);
      setHotspotsData(hotspots);
      setMonthlyData(monthly);
    } catch (err) {
      const error =
        err instanceof Error
          ? err
          : new Error("Failed to fetch analytics data");
      setError(error);
      console.error("Error fetching analytics data:", error);
    } finally {
      if (isRefresh) {
        setRefreshing(false);
      } else {
        setLoading(false);
      }
    }
  }, []);

  /**
   * Refresh all analytics data without removing existing visualizations
   */
  const refresh = useCallback(async () => {
    await fetchData(true);
  }, [fetchData]);

  // Fetch data on mount
  useEffect(() => {
    fetchData(false);
  }, [fetchData]);

  return {
    yoyData,
    intensityData,
    hotspotsData,
    monthlyData,
    loading,
    refreshing,
    error,
    refresh,
  };
}
