// Hook Return Types

import type {
  YoYResponse,
  IntensityResponse,
  HotspotsResponse,
  MonthlyEmissionsResponse,
  EmissionFormData,
  MetricsFormData,
} from "./api.types";

// Analytics Hook
export interface UseAnalyticsReturn {
  yoyData: YoYResponse | null;
  intensityData: IntensityResponse | null;
  hotspotsData: HotspotsResponse | null;
  monthlyData: MonthlyEmissionsResponse | null;
  loading: boolean;
  refreshing: boolean;
  error: Error | null;
  refresh: () => Promise<void>;
}

// Emission Form Hook
export interface UseEmissionFormReturn {
  submitEmission: (data: EmissionFormData) => Promise<void>;
  loading: boolean;
  error: Error | null;
  success: boolean;
  reset: () => void;
}

// Metrics Form Hook
export interface UseMetricsFormReturn {
  submitMetric: (data: MetricsFormData) => Promise<void>;
  loading: boolean;
  error: Error | null;
  success: boolean;
  reset: () => void;
}

// Generic API Hook State
export interface ApiState<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
}

// Generic API Hook Return
export interface UseApiReturn<T> extends ApiState<T> {
  refetch: () => Promise<void>;
}
