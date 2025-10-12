import { useState, useCallback } from "react";
import metricsService from "../services/metricsService";
import type { MetricsFormData } from "../types/api.types";
import type { UseMetricsFormReturn } from "../types/hook.types";

/**
 * Custom hook for managing business metrics form submission
 * Handles form submission, loading states, errors, and success states
 *
 * @param onSuccess - Optional callback to execute on successful submission
 * @returns Submission function, loading state, error state, success state, and reset function
 */
export function useMetricsForm(onSuccess?: () => void): UseMetricsFormReturn {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [success, setSuccess] = useState(false);

  /**
   * Submit metrics data to the API
   */
  const submitMetric = useCallback(
    async (data: MetricsFormData) => {
      setLoading(true);
      setError(null);
      setSuccess(false);

      try {
        await metricsService.createMetric(data);
        setSuccess(true);

        // Call the optional success callback
        if (onSuccess) {
          onSuccess();
        }
      } catch (err) {
        const error =
          err instanceof Error
            ? err
            : new Error("Failed to submit metrics data");
        setError(error);
        console.error("Error submitting metric:", error);
      } finally {
        setLoading(false);
      }
    },
    [onSuccess]
  );

  /**
   * Reset the form state (error and success flags)
   */
  const reset = useCallback(() => {
    setError(null);
    setSuccess(false);
  }, []);

  return {
    submitMetric,
    loading,
    error,
    success,
    reset,
  };
}
