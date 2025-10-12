import axios from "axios";
import type {
  AxiosInstance,
  AxiosError,
  InternalAxiosRequestConfig,
} from "axios";
import type { APIError } from "../types/api.types";

/**
 * Custom error class for API errors
 */
export class ApiClientError extends Error {
  public statusCode?: number;
  public code?: string;
  public details?: Record<string, any>;
  public isNetworkError: boolean;
  public isServerError: boolean;
  public isClientError: boolean;

  constructor(
    message: string,
    statusCode?: number,
    code?: string,
    details?: Record<string, any>
  ) {
    super(message);
    this.name = "ApiClientError";
    this.statusCode = statusCode;
    this.code = code;
    this.details = details;
    this.isNetworkError = !statusCode;
    this.isServerError = statusCode ? statusCode >= 500 : false;
    this.isClientError = statusCode
      ? statusCode >= 400 && statusCode < 500
      : false;

    // Maintains proper stack trace for where our error was thrown
    if (typeof (Error as any).captureStackTrace === "function") {
      (Error as any).captureStackTrace(this, ApiClientError);
    }
  }
}

/**
 * Retry configuration
 */
interface RetryConfig {
  maxRetries: number;
  retryDelay: number;
  retryableStatuses: number[];
}

/**
 * Base API Client with axios instance and error handling interceptors
 */
class ApiClient {
  protected axiosInstance: AxiosInstance;
  private retryConfig: RetryConfig;

  constructor(baseURL: string, retryConfig?: Partial<RetryConfig>) {
    this.axiosInstance = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        "Content-Type": "application/json",
      },
    });

    // Default retry configuration
    this.retryConfig = {
      maxRetries: retryConfig?.maxRetries ?? 3,
      retryDelay: retryConfig?.retryDelay ?? 1000,
      retryableStatuses: retryConfig?.retryableStatuses ?? [
        408, 429, 500, 502, 503, 504,
      ],
    };

    this.setupInterceptors();
  }

  /**
   * Setup request and response interceptors for error handling
   */
  private setupInterceptors(): void {
    // Request interceptor
    this.axiosInstance.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        // Initialize retry count
        if (!config.headers) {
          config.headers = {} as any;
        }

        // You can add auth tokens here if needed in the future
        // config.headers.Authorization = `Bearer ${token}`;

        return config;
      },
      (error) => {
        console.error("Request interceptor error:", error);
        return Promise.reject(error);
      }
    );

    // Response interceptor for error handling
    this.axiosInstance.interceptors.response.use(
      (response) => response,
      async (error: AxiosError<APIError>) => {
        const originalRequest = error.config as InternalAxiosRequestConfig & {
          _retry?: boolean;
          _retryCount?: number;
        };

        // Handle retry logic for specific errors
        if (originalRequest && this.shouldRetry(error, originalRequest)) {
          originalRequest._retryCount = originalRequest._retryCount || 0;
          originalRequest._retryCount += 1;

          if (originalRequest._retryCount <= this.retryConfig.maxRetries) {
            originalRequest._retry = true;

            // Wait before retrying with exponential backoff
            const delay =
              this.retryConfig.retryDelay *
              Math.pow(2, originalRequest._retryCount - 1);
            await this.sleep(delay);

            console.log(
              `Retrying request (attempt ${originalRequest._retryCount}/${this.retryConfig.maxRetries})`
            );

            return this.axiosInstance(originalRequest);
          }
        }

        // Transform error into ApiClientError
        return Promise.reject(this.handleError(error));
      }
    );
  }

  /**
   * Determine if a request should be retried
   */
  private shouldRetry(
    error: AxiosError,
    config: InternalAxiosRequestConfig & {
      _retry?: boolean;
      _retryCount?: number;
    }
  ): boolean {
    // Don't retry if already retrying or max retries reached
    if (
      config._retry ||
      (config._retryCount || 0) >= this.retryConfig.maxRetries
    ) {
      return false;
    }

    // Retry on network errors
    if (!error.response) {
      return true;
    }

    // Retry on specific status codes
    if (
      error.response.status &&
      this.retryConfig.retryableStatuses.includes(error.response.status)
    ) {
      return true;
    }

    return false;
  }

  /**
   * Sleep utility for retry delays
   */
  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  /**
   * Handle and transform axios errors into ApiClientError
   */
  private handleError(error: AxiosError<APIError>): ApiClientError {
    if (error.response) {
      // Server responded with error status
      const statusCode = error.response.status;
      const apiError = error.response.data;

      // Extract error details from API response
      const message =
        apiError?.error?.message || this.getDefaultErrorMessage(statusCode);
      const code = apiError?.error?.code || `HTTP_${statusCode}`;
      const details = apiError?.error?.details;

      return new ApiClientError(message, statusCode, code, details);
    } else if (error.request) {
      // Request made but no response received (network error)
      return new ApiClientError(
        "Unable to connect to the server. Please check your internet connection and try again.",
        undefined,
        "NETWORK_ERROR"
      );
    } else {
      // Error in request setup
      return new ApiClientError(
        error.message || "An unexpected error occurred. Please try again.",
        undefined,
        "REQUEST_SETUP_ERROR"
      );
    }
  }

  /**
   * Get default error message based on status code
   */
  private getDefaultErrorMessage(statusCode: number): string {
    switch (statusCode) {
      case 400:
        return "Invalid request. Please check your input and try again.";
      case 401:
        return "Authentication required. Please log in and try again.";
      case 403:
        return "You don't have permission to perform this action.";
      case 404:
        return "The requested resource was not found.";
      case 408:
        return "Request timeout. Please try again.";
      case 409:
        return "A conflict occurred. The resource may already exist.";
      case 422:
        return "Validation error. Please check your input.";
      case 429:
        return "Too many requests. Please wait a moment and try again.";
      case 500:
        return "Internal server error. Please try again later.";
      case 502:
        return "Bad gateway. The server is temporarily unavailable.";
      case 503:
        return "Service unavailable. Please try again later.";
      case 504:
        return "Gateway timeout. The server took too long to respond.";
      default:
        return `Server error (${statusCode}). Please try again later.`;
    }
  }

  /**
   * Get the axios instance for making requests
   */
  protected getClient(): AxiosInstance {
    return this.axiosInstance;
  }

  /**
   * Manual retry method for failed requests
   * Can be used by components to retry a specific request
   */
  public async retryRequest<T>(
    requestFn: () => Promise<T>,
    maxRetries: number = this.retryConfig.maxRetries
  ): Promise<T> {
    let lastError: Error;

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        return await requestFn();
      } catch (error) {
        lastError = error as Error;

        if (attempt < maxRetries) {
          const delay = this.retryConfig.retryDelay * Math.pow(2, attempt - 1);
          console.log(
            `Retry attempt ${attempt}/${maxRetries} after ${delay}ms`
          );
          await this.sleep(delay);
        }
      }
    }

    throw lastError!;
  }
}

export default ApiClient;
