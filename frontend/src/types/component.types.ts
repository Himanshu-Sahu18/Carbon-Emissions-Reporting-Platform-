// Component Prop Types

import type {
  YoYResponse,
  IntensityResponse,
  HotspotsResponse,
  MonthlyEmissionsResponse,
} from "./api.types";

// Layout Components
export interface DashboardLayoutProps {
  children: React.ReactNode;
}

export interface HeaderProps {
  onRefresh?: () => void;
  isRefreshing?: boolean;
}

// Form Components
export interface EmissionFormProps {
  onSuccess?: () => void;
  onError?: (error: Error) => void;
}

export interface MetricsFormProps {
  onSuccess?: () => void;
  onError?: (error: Error) => void;
}

// Chart Components
export interface YoYChartProps {
  data?: YoYResponse | null;
  loading?: boolean;
  error?: Error | null;
  currentYear?: number;
  previousYear?: number;
  onRefresh?: () => void;
}

export interface HotspotDonutChartProps {
  data?: HotspotsResponse | null;
  loading?: boolean;
  error?: Error | null;
  startDate?: Date;
  endDate?: Date;
  scope?: number;
  limit?: number;
  onRefresh?: () => void;
}

export interface IntensityKPICardProps {
  data?: IntensityResponse | null;
  loading?: boolean;
  error?: Error | null;
  startDate: Date;
  endDate: Date;
  metricName: string;
  onRefresh?: () => void;
}

export interface MonthlyTrendChartProps {
  data?: MonthlyEmissionsResponse | null;
  loading?: boolean;
  error?: Error | null;
  year?: number;
  onRefresh?: () => void;
}

// Common UI Components
export interface LoadingSpinnerProps {
  size?: "small" | "medium" | "large";
  message?: string;
}

export interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
  showRetry?: boolean;
}

export interface EmptyStateProps {
  message: string;
  icon?: React.ReactNode;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger" | "success";
  size?: "small" | "medium" | "large";
  loading?: boolean;
  icon?: React.ReactNode;
}

export interface CardProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  className?: string;
  headerAction?: React.ReactNode;
}
