import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import { useMetricsForm } from "../../hooks/useMetricsForm";
import { metricsFormValidation } from "../../utils/validation";
import type { MetricsFormProps } from "../../types/component.types";
import type { MetricsFormData } from "../../types/api.types";
import Button from "../common/Button";
import Card from "../common/Card";
import ErrorMessage from "../common/ErrorMessage";

// Common metric names for the dropdown
const COMMON_METRICS = [
  "Tons of Steel Produced",
  "Units Manufactured",
  "Square Meters Produced",
  "Revenue (USD)",
  "Custom",
] as const;

/**
 * MetricsForm Component
 * Form for submitting business metrics (production data)
 */
const MetricsForm: React.FC<MetricsFormProps> = ({ onSuccess, onError }) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset: resetForm,
    watch,
    setValue,
  } = useForm<MetricsFormData>();

  const {
    submitMetric,
    loading,
    error,
    success,
    reset: resetHook,
  } = useMetricsForm(onSuccess);

  // Watch the metric_name field to handle custom input
  const selectedMetric = watch("metric_name");

  // Clear form on successful submission
  useEffect(() => {
    if (success) {
      resetForm();
      // Reset success state after 3 seconds
      const timer = setTimeout(() => {
        resetHook();
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [success, resetForm, resetHook]);

  // Call onError callback when error occurs
  useEffect(() => {
    if (error && onError) {
      onError(error);
    }
  }, [error, onError]);

  const onSubmit = async (data: MetricsFormData) => {
    await submitMetric(data);
  };

  // Get today's date in YYYY-MM-DD format for max date validation
  const today = new Date().toISOString().split("T")[0];

  return (
    <Card
      title="Submit Business Metrics"
      subtitle="Record production and business metrics"
    >
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="space-y-3 sm:space-y-4"
      >
        {/* Metric Name */}
        <div>
          <label
            htmlFor="metric_name"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Metric Name <span className="text-red-500">*</span>
          </label>
          <select
            id="metric_name"
            {...register("metric_name", metricsFormValidation.metric_name)}
            className={`w-full px-3 py-2 sm:py-2.5 text-base border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 touch-manipulation ${
              errors.metric_name ? "border-red-500" : "border-gray-300"
            }`}
            aria-invalid={errors.metric_name ? "true" : "false"}
            aria-describedby={
              errors.metric_name ? "metric_name-error" : undefined
            }
          >
            <option value="">Select a metric</option>
            {COMMON_METRICS.map((metric) => (
              <option key={metric} value={metric}>
                {metric}
              </option>
            ))}
          </select>
          {errors.metric_name && (
            <p
              id="metric_name-error"
              className="mt-1 text-sm text-red-600"
              role="alert"
            >
              {errors.metric_name.message}
            </p>
          )}
        </div>

        {/* Custom Metric Name Input (shown when "Custom" is selected) */}
        {selectedMetric === "Custom" && (
          <div>
            <label
              htmlFor="custom_metric_name"
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              Custom Metric Name <span className="text-red-500">*</span>
            </label>
            <input
              id="custom_metric_name"
              type="text"
              onChange={(e) => setValue("metric_name", e.target.value)}
              className="w-full px-3 py-2 sm:py-2.5 text-base border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 touch-manipulation"
              placeholder="Enter custom metric name"
              aria-describedby="custom_metric_name-help"
            />
            <p
              id="custom_metric_name-help"
              className="mt-1 text-xs text-gray-500"
            >
              Enter a descriptive name for your custom metric
            </p>
          </div>
        )}

        {/* Value */}
        <div>
          <label
            htmlFor="value"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Value <span className="text-red-500">*</span>
          </label>
          <input
            id="value"
            type="number"
            step="0.01"
            {...register("value", metricsFormValidation.value)}
            className={`w-full px-3 py-2 sm:py-2.5 text-base border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 touch-manipulation ${
              errors.value ? "border-red-500" : "border-gray-300"
            }`}
            placeholder="e.g., 150000"
            aria-invalid={errors.value ? "true" : "false"}
            aria-describedby={
              errors.value ? "value-error value-help" : "value-help"
            }
          />
          <p id="value-help" className="mt-1 text-xs text-gray-500">
            Enter the metric value
          </p>
          {errors.value && (
            <p
              id="value-error"
              className="mt-1 text-sm text-red-600"
              role="alert"
            >
              {errors.value.message}
            </p>
          )}
        </div>

        {/* Unit */}
        <div>
          <label
            htmlFor="unit"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Unit <span className="text-red-500">*</span>
          </label>
          <input
            id="unit"
            type="text"
            {...register("unit", metricsFormValidation.unit)}
            className={`w-full px-3 py-2 sm:py-2.5 text-base border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 touch-manipulation ${
              errors.unit ? "border-red-500" : "border-gray-300"
            }`}
            placeholder="e.g., tons, units, square meters, USD"
            aria-invalid={errors.unit ? "true" : "false"}
            aria-describedby={errors.unit ? "unit-error" : undefined}
          />
          {errors.unit && (
            <p
              id="unit-error"
              className="mt-1 text-sm text-red-600"
              role="alert"
            >
              {errors.unit.message}
            </p>
          )}
        </div>

        {/* Metric Date */}
        <div>
          <label
            htmlFor="metric_date"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Metric Date <span className="text-red-500">*</span>
          </label>
          <input
            id="metric_date"
            type="date"
            max={today}
            {...register("metric_date", metricsFormValidation.metric_date)}
            className={`w-full px-3 py-2 sm:py-2.5 text-base border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 touch-manipulation ${
              errors.metric_date ? "border-red-500" : "border-gray-300"
            }`}
            aria-invalid={errors.metric_date ? "true" : "false"}
            aria-describedby={
              errors.metric_date ? "metric_date-error" : undefined
            }
          />
          {errors.metric_date && (
            <p
              id="metric_date-error"
              className="mt-1 text-sm text-red-600"
              role="alert"
            >
              {errors.metric_date.message}
            </p>
          )}
        </div>

        {/* Success Message */}
        {success && (
          <div
            className="bg-green-50 border border-green-200 rounded-lg p-4"
            role="alert"
            aria-live="polite"
          >
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <svg
                  className="h-5 w-5 text-green-400"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-green-800">Success</h3>
                <p className="mt-1 text-sm text-green-700">
                  Business metric submitted successfully!
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <ErrorMessage message={error.message} onRetry={() => resetHook()} />
        )}

        {/* Submit Button */}
        <div className="pt-4">
          <Button
            type="submit"
            variant="primary"
            fullWidth
            loading={loading}
            disabled={loading}
          >
            {loading ? "Submitting..." : "Submit Business Metric"}
          </Button>
        </div>
      </form>
    </Card>
  );
};

export default MetricsForm;
