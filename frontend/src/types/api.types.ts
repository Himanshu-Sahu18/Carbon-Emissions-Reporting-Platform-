// API Response Types

export interface ScopeEmission {
  scope: number;
  total_emissions: number;
  unit: string;
}

export interface YoYResponse {
  current_year: number;
  previous_year: number;
  current_year_data: ScopeEmission[];
  previous_year_data: ScopeEmission[];
  comparison: {
    total_current: number;
    total_previous: number;
    change_percentage: number;
    change_absolute: number;
  };
}

export interface IntensityResponse {
  period: {
    start_date: string;
    end_date: string;
  };
  metric_name: string;
  total_emissions: number;
  total_production: number;
  production_unit: string;
  intensity: number;
  intensity_unit: string;
  record_count: number;
}

export interface HotspotItem {
  activity_name: string;
  scope: number;
  total_emissions: number;
  percentage: number;
  record_count: number;
  average_per_record: number;
}

export interface HotspotsResponse {
  period: {
    start_date?: string;
    end_date?: string;
    limit: number;
  };
  total_emissions: number;
  hotspots: HotspotItem[];
}

export interface MonthlyEmission {
  month: number;
  month_name: string;
  total_emissions: number;
  record_count: number;
}

export interface MonthlyEmissionsResponse {
  year: number;
  months: MonthlyEmission[];
}

// Form Data Types

export interface EmissionFormData {
  activity_name: string;
  activity_value: number;
  activity_unit: string;
  activity_date: Date | string;
  scope: 1;
  location?: string;
  department?: string;
}

export interface MetricsFormData {
  metric_name: string;
  value: number;
  unit: string;
  metric_date: Date | string;
}

// Error Types

export interface APIError {
  error: {
    code: string;
    message: string;
    details?: Record<string, any>;
  };
}
