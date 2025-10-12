import ApiClient from "./apiClient";
import type {
  YoYResponse,
  IntensityResponse,
  HotspotsResponse,
  MonthlyEmissionsResponse,
} from "../types/api.types";

/**
 * Analytics Service for fetching emission analytics data
 */
class AnalyticsService extends ApiClient {
  /**
   * Get Year-over-Year emissions comparison
   * @param currentYear - Current year (optional, defaults to current year)
   * @param previousYear - Previous year (optional, defaults to current year - 1)
   */
  async getYoYEmissions(
    currentYear?: number,
    previousYear?: number
  ): Promise<YoYResponse> {
    const params = new URLSearchParams();
    if (currentYear) params.append("current_year", currentYear.toString());
    if (previousYear) params.append("previous_year", previousYear.toString());

    const queryString = params.toString();
    const url = queryString
      ? `/api/analytics/yoy?${queryString}`
      : "/api/analytics/yoy";

    const response = await this.axiosInstance.get<YoYResponse>(url);
    return response.data;
  }

  /**
   * Get emission intensity metrics
   * @param startDate - Start date in YYYY-MM-DD format
   * @param endDate - End date in YYYY-MM-DD format
   * @param metricName - Name of the business metric (e.g., "Tons of Steel Produced")
   */
  async getEmissionIntensity(
    startDate: string,
    endDate: string,
    metricName: string
  ): Promise<IntensityResponse> {
    const params = new URLSearchParams({
      start_date: startDate,
      end_date: endDate,
      metric_name: metricName,
    });

    const response = await this.axiosInstance.get<IntensityResponse>(
      `/api/analytics/intensity?${params.toString()}`
    );
    return response.data;
  }

  /**
   * Get emission hotspots (top emission sources)
   * @param filters - Optional filters for date range, scope, and limit
   */
  async getEmissionHotspots(filters?: {
    startDate?: string;
    endDate?: string;
    scope?: number;
    limit?: number;
  }): Promise<HotspotsResponse> {
    const params = new URLSearchParams();

    if (filters?.startDate) params.append("start_date", filters.startDate);
    if (filters?.endDate) params.append("end_date", filters.endDate);
    if (filters?.scope) params.append("scope", filters.scope.toString());
    if (filters?.limit) params.append("limit", filters.limit.toString());

    const queryString = params.toString();
    const url = queryString
      ? `/api/analytics/hotspots?${queryString}`
      : "/api/analytics/hotspots";

    const response = await this.axiosInstance.get<HotspotsResponse>(url);
    return response.data;
  }

  /**
   * Get monthly emissions data for a specific year
   * Note: This endpoint may need to be implemented on the backend
   * or aggregated from existing data on the frontend
   * @param year - Year to fetch monthly data for
   */
  async getMonthlyEmissions(year: number): Promise<MonthlyEmissionsResponse> {
    const response = await this.axiosInstance.get<MonthlyEmissionsResponse>(
      `/api/analytics/monthly?year=${year}`
    );
    return response.data;
  }
}

// Create and export a singleton instance
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";
const analyticsService = new AnalyticsService(API_BASE_URL);

export default analyticsService;
