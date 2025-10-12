import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import { useEmissionForm } from "../../hooks/useEmissionForm";
import { emissionFormValidation } from "../../utils/validation";
import type { EmissionFormProps } from "../../types/component.types";
import type { EmissionFormData } from "../../types/api.types";
import Button from "../common/Button";
import Card from "../common/Card";
import ErrorMessage from "../common/ErrorMessage";

/**
 * EmissionForm Component
 * Form for submitting Scope 1 emission data
 */
const EmissionForm: React.FC<EmissionFormProps> = ({ onSuccess, onError }) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset: resetForm,
  } = useForm<EmissionFormData>({
    defaultValues: {
      scope: 1,
    },
  });

  const {
    submitEmission,
    loading,
    error,
    success,
    reset: resetHook,
  } = useEmissionForm(onSuccess);

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

  const onSubmit = async (data: EmissionFormData) => {
    await submitEmission(data);
  };

  // Get today's date in YYYY-MM-DD format for max date validation
  const today = new Date().toISOString().split("T")[0];

  return (
    <Card
      title="Submit Emission Data"
      subtitle="Record Scope 1 emission activities"
    >
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="space-y-3 sm:space-y-4"
      >
        {/* Activity Name */}
        <div>
          <label
            htmlFor="activity_name"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Activity Name <span className="text-red-500">*</span>
          </label>
          <input
            id="activity_name"
            type="text"
            {...register("activity_name", emissionFormValidation.activity_name)}
            className={`w-full px-3 py-2 sm:py-2.5 text-base border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 touch-manipulation ${
              errors.activity_name ? "border-red-500" : "border-gray-300"
            }`}
            placeholder="e.g., Diesel, Natural Gas, Company Vehicles"
            aria-invalid={errors.activity_name ? "true" : "false"}
            aria-describedby={
              errors.activity_name ? "activity_name-error" : undefined
            }
          />
          {errors.activity_name && (
            <p
              id="activity_name-error"
              className="mt-1 text-sm text-red-600"
              role="alert"
            >
              {errors.activity_name.message}
            </p>
          )}
        </div>

        {/* Activity Value */}
        <div>
          <label
            htmlFor="activity_value"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Activity Value <span className="text-red-500">*</span>
          </label>
          <input
            id="activity_value"
            type="number"
            step="0.01"
            {...register(
              "activity_value",
              emissionFormValidation.activity_value
            )}
            className={`w-full px-3 py-2 sm:py-2.5 text-base border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 touch-manipulation ${
              errors.activity_value ? "border-red-500" : "border-gray-300"
            }`}
            placeholder="e.g., 1000"
            aria-invalid={errors.activity_value ? "true" : "false"}
            aria-describedby={
              errors.activity_value
                ? "activity_value-error activity_value-help"
                : "activity_value-help"
            }
          />
          <p id="activity_value-help" className="mt-1 text-xs text-gray-500">
            Enter the quantity of the activity
          </p>
          {errors.activity_value && (
            <p
              id="activity_value-error"
              className="mt-1 text-sm text-red-600"
              role="alert"
            >
              {errors.activity_value.message}
            </p>
          )}
        </div>

        {/* Activity Unit */}
        <div>
          <label
            htmlFor="activity_unit"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Activity Unit <span className="text-red-500">*</span>
          </label>
          <input
            id="activity_unit"
            type="text"
            {...register("activity_unit", emissionFormValidation.activity_unit)}
            className={`w-full px-3 py-2 sm:py-2.5 text-base border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 touch-manipulation ${
              errors.activity_unit ? "border-red-500" : "border-gray-300"
            }`}
            placeholder="e.g., litres, kWh, km"
            aria-invalid={errors.activity_unit ? "true" : "false"}
            aria-describedby={
              errors.activity_unit ? "activity_unit-error" : undefined
            }
          />
          {errors.activity_unit && (
            <p
              id="activity_unit-error"
              className="mt-1 text-sm text-red-600"
              role="alert"
            >
              {errors.activity_unit.message}
            </p>
          )}
        </div>

        {/* Activity Date */}
        <div>
          <label
            htmlFor="activity_date"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Activity Date <span className="text-red-500">*</span>
          </label>
          <input
            id="activity_date"
            type="date"
            max={today}
            {...register("activity_date", emissionFormValidation.activity_date)}
            className={`w-full px-3 py-2 sm:py-2.5 text-base border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 touch-manipulation ${
              errors.activity_date ? "border-red-500" : "border-gray-300"
            }`}
            aria-invalid={errors.activity_date ? "true" : "false"}
            aria-describedby={
              errors.activity_date ? "activity_date-error" : undefined
            }
          />
          {errors.activity_date && (
            <p
              id="activity_date-error"
              className="mt-1 text-sm text-red-600"
              role="alert"
            >
              {errors.activity_date.message}
            </p>
          )}
        </div>

        {/* Location (Optional) */}
        <div>
          <label
            htmlFor="location"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Location <span className="text-gray-400 text-xs">(Optional)</span>
          </label>
          <input
            id="location"
            type="text"
            {...register("location", emissionFormValidation.location)}
            className={`w-full px-3 py-2 sm:py-2.5 text-base border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 touch-manipulation ${
              errors.location ? "border-red-500" : "border-gray-300"
            }`}
            placeholder="e.g., Plant A, Building 3"
            aria-invalid={errors.location ? "true" : "false"}
            aria-describedby={errors.location ? "location-error" : undefined}
          />
          {errors.location && (
            <p
              id="location-error"
              className="mt-1 text-sm text-red-600"
              role="alert"
            >
              {errors.location.message}
            </p>
          )}
        </div>

        {/* Department (Optional) */}
        <div>
          <label
            htmlFor="department"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Department <span className="text-gray-400 text-xs">(Optional)</span>
          </label>
          <input
            id="department"
            type="text"
            {...register("department", emissionFormValidation.department)}
            className={`w-full px-3 py-2 sm:py-2.5 text-base border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 touch-manipulation ${
              errors.department ? "border-red-500" : "border-gray-300"
            }`}
            placeholder="e.g., Production, Operations"
            aria-invalid={errors.department ? "true" : "false"}
            aria-describedby={
              errors.department ? "department-error" : undefined
            }
          />
          {errors.department && (
            <p
              id="department-error"
              className="mt-1 text-sm text-red-600"
              role="alert"
            >
              {errors.department.message}
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
                  Emission data submitted successfully!
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
            {loading ? "Submitting..." : "Submit Emission Data"}
          </Button>
        </div>
      </form>
    </Card>
  );
};

export default EmissionForm;
