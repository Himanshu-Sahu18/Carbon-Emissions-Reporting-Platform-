import { useState, useCallback } from "react";
import emissionsService from "../services/emissionsService";
import type { EmissionFormData } from "../types/api.types";
import type { UseEmissionFormReturn } from "../types/hook.types";

/**
 * Custom hook for managing emission form submission
 * Handles form submission, loading states, errors, and success states
 *
 * @param onSuccess - Optional callback to execute on successful submission
 * @returns Submission function, loading state, error state, success state, and reset function
 */
export function useEmissionForm(onSuccess?: () => void): UseEmissionFormReturn {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [success, setSuccess] = useState(false);

  /**
   * Submit emission data to the API
   */
  const submitEmission = useCallback(
    async (data: EmissionFormData) => {
      setLoading(true);
      setError(null);
      setSuccess(false);

      try {
        await emissionsService.createEmission(data);
        setSuccess(true);

        // Call the optional success callback
        if (onSuccess) {
          onSuccess();
        }
      } catch (err) {
        const error =
          err instanceof Error
            ? err
            : new Error("Failed to submit emission data");
        setError(error);
        console.error("Error submitting emission:", error);
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
    submitEmission,
    loading,
    error,
    success,
    reset,
  };
}
