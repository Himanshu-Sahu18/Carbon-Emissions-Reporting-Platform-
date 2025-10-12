import ApiClient from "./apiClient";
import type { MetricsFormData } from "../types/api.types";

/**
 * Metrics Service for submitting business metrics
 */
class MetricsService extends ApiClient {
  /**
   * Create a new business metric record
   * @param data - Metrics form data
   * @returns Created metric record
   */
  async createMetric(data: MetricsFormData): Promise<any> {
    // Format the date if it's a Date object
    const metricDate =
      data.metric_date instanceof Date
        ? data.metric_date.toISOString().split("T")[0]
        : data.metric_date;

    const payload = {
      metric_name: data.metric_name,
      value: data.value,
      unit: data.unit,
      metric_date: metricDate,
    };

    const response = await this.axiosInstance.post("/api/metrics/", payload);
    return response.data;
  }

  /**
   * Get all business metrics (optional - for future use)
   * @param filters - Optional filters for querying metrics
   */
  async getMetrics(filters?: {
    startDate?: string;
    endDate?: string;
    metricName?: string;
    limit?: number;
    offset?: number;
  }): Promise<any> {
    const params = new URLSearchParams();

    if (filters?.startDate) params.append("start_date", filters.startDate);
    if (filters?.endDate) params.append("end_date", filters.endDate);
    if (filters?.metricName) params.append("metric_name", filters.metricName);
    if (filters?.limit) params.append("limit", filters.limit.toString());
    if (filters?.offset) params.append("offset", filters.offset.toString());

    const queryString = params.toString();
    const url = queryString ? `/api/metrics/?${queryString}` : "/api/metrics/";

    const response = await this.axiosInstance.get(url);
    return response.data;
  }
}

// Create and export a singleton instance
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";
const metricsService = new MetricsService(API_BASE_URL);

export default metricsService;
