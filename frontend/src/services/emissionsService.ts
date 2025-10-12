import ApiClient from "./apiClient";
import type { EmissionFormData } from "../types/api.types";

/**
 * Emissions Service for submitting emission records
 */
class EmissionsService extends ApiClient {
  /**
   * Create a new emission record
   * @param data - Emission form data
   * @returns Created emission record
   */
  async createEmission(data: EmissionFormData): Promise<any> {
    // Format the date if it's a Date object
    const activityDate =
      data.activity_date instanceof Date
        ? data.activity_date.toISOString().split("T")[0]
        : data.activity_date;

    const payload = {
      activity_name: data.activity_name,
      activity_value: data.activity_value,
      activity_unit: data.activity_unit,
      activity_date: activityDate,
      scope: data.scope,
      location: data.location || null,
      department: data.department || null,
    };

    const response = await this.axiosInstance.post("/api/emissions/", payload);
    return response.data;
  }

  /**
   * Get all emission records (optional - for future use)
   * @param filters - Optional filters for querying emissions
   */
  async getEmissions(filters?: {
    startDate?: string;
    endDate?: string;
    scope?: number;
    limit?: number;
    offset?: number;
  }): Promise<any> {
    const params = new URLSearchParams();

    if (filters?.startDate) params.append("start_date", filters.startDate);
    if (filters?.endDate) params.append("end_date", filters.endDate);
    if (filters?.scope) params.append("scope", filters.scope.toString());
    if (filters?.limit) params.append("limit", filters.limit.toString());
    if (filters?.offset) params.append("offset", filters.offset.toString());

    const queryString = params.toString();
    const url = queryString
      ? `/api/emissions/?${queryString}`
      : "/api/emissions/";

    const response = await this.axiosInstance.get(url);
    return response.data;
  }
}

// Create and export a singleton instance
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";
const emissionsService = new EmissionsService(API_BASE_URL);

export default emissionsService;
