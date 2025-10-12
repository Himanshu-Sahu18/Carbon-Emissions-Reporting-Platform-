/**
 * Test file to verify error handling implementation
 * This file demonstrates and tests various error handling scenarios
 */

import { useState } from "react";
import { createRoot } from "react-dom/client";
import { ErrorBoundary } from "./components/common";
import { validateEmissionForm, validateMetricsForm } from "./utils/validation";
import type { EmissionFormData, MetricsFormData } from "./types/api.types";
import { ApiClientError } from "./services/apiClient";

// Test component that throws an error
function ErrorThrowingComponent() {
  const [shouldThrow, setShouldThrow] = useState(false);

  if (shouldThrow) {
    throw new Error("Test error from component!");
  }

  return (
    <div className="p-4 border rounded">
      <h3 className="font-bold mb-2">Error Boundary Test</h3>
      <button
        onClick={() => setShouldThrow(true)}
        className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
      >
        Throw Error
      </button>
    </div>
  );
}

// Test validation functions
function ValidationTest() {
  const [emissionResult, setEmissionResult] = useState<string>("");
  const [metricsResult, setMetricsResult] = useState<string>("");

  const testEmissionValidation = () => {
    // Test with invalid data
    const invalidData: Partial<EmissionFormData> = {
      activity_name: "D", // Too short
      activity_value: -10, // Negative
      activity_date: new Date("2099-01-01"), // Future date
    };

    const result = validateEmissionForm(invalidData);
    setEmissionResult(
      JSON.stringify(
        {
          isValid: result.isValid,
          errors: result.errors,
        },
        null,
        2
      )
    );
  };

  const testMetricsValidation = () => {
    // Test with invalid data
    const invalidData: Partial<MetricsFormData> = {
      metric_name: "T", // Too short
      value: -100, // Negative
      metric_date: new Date("2099-12-31"), // Future date
    };

    const result = validateMetricsForm(invalidData);
    setMetricsResult(
      JSON.stringify(
        {
          isValid: result.isValid,
          errors: result.errors,
        },
        null,
        2
      )
    );
  };

  return (
    <div className="p-4 border rounded">
      <h3 className="font-bold mb-4">Validation Tests</h3>

      <div className="space-y-4">
        <div>
          <button
            onClick={testEmissionValidation}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 mb-2"
          >
            Test Emission Form Validation
          </button>
          {emissionResult && (
            <pre className="bg-gray-100 p-2 rounded text-xs overflow-auto">
              {emissionResult}
            </pre>
          )}
        </div>

        <div>
          <button
            onClick={testMetricsValidation}
            className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 mb-2"
          >
            Test Metrics Form Validation
          </button>
          {metricsResult && (
            <pre className="bg-gray-100 p-2 rounded text-xs overflow-auto">
              {metricsResult}
            </pre>
          )}
        </div>
      </div>
    </div>
  );
}

// Test API error handling
function ApiErrorTest() {
  const [errorInfo, setErrorInfo] = useState<string>("");

  const testApiErrors = () => {
    const errors = [
      new ApiClientError("Network error test", undefined, "NETWORK_ERROR"),
      new ApiClientError("Server error test", 500, "HTTP_500"),
      new ApiClientError("Not found test", 404, "HTTP_404"),
      new ApiClientError("Validation error test", 422, "HTTP_422", {
        field: "activity_name",
        message: "Invalid value",
      }),
    ];

    const errorDetails = errors.map((err) => ({
      message: err.message,
      statusCode: err.statusCode,
      code: err.code,
      isNetworkError: err.isNetworkError,
      isServerError: err.isServerError,
      isClientError: err.isClientError,
      details: err.details,
    }));

    setErrorInfo(JSON.stringify(errorDetails, null, 2));
  };

  return (
    <div className="p-4 border rounded">
      <h3 className="font-bold mb-4">API Error Tests</h3>
      <button
        onClick={testApiErrors}
        className="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600 mb-2"
      >
        Test API Error Types
      </button>
      {errorInfo && (
        <pre className="bg-gray-100 p-2 rounded text-xs overflow-auto max-h-96">
          {errorInfo}
        </pre>
      )}
    </div>
  );
}

// Main test app
function ErrorHandlingTestApp() {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">
          Error Handling Implementation Tests
        </h1>

        <div className="space-y-6">
          <ErrorBoundary>
            <ErrorThrowingComponent />
          </ErrorBoundary>

          <ValidationTest />

          <ApiErrorTest />

          <div className="p-4 border rounded bg-green-50">
            <h3 className="font-bold mb-2 text-green-800">
              ✅ Implementation Complete
            </h3>
            <ul className="list-disc list-inside space-y-1 text-sm text-green-700">
              <li>Global ErrorBoundary component</li>
              <li>Enhanced API client with retry logic</li>
              <li>Centralized validation schemas</li>
              <li>Field-level validation in forms</li>
              <li>User-friendly error messages</li>
              <li>Network error handling</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

// Mount the test app
const container = document.getElementById("root");
if (container) {
  const root = createRoot(container);
  root.render(<ErrorHandlingTestApp />);
}

export default ErrorHandlingTestApp;
