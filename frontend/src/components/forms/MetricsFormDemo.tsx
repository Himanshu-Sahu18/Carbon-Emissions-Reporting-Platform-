/**
 * MetricsForm Demo Component
 * Demonstrates the usage of the MetricsForm component
 */

import React from "react";
import MetricsForm from "./MetricsForm";

const MetricsFormDemo: React.FC = () => {
  const handleSuccess = () => {
    console.log("✓ Metric submitted successfully!");
    alert("Business metric submitted successfully!");
  };

  const handleError = (error: Error) => {
    console.error("✗ Error submitting metric:", error);
    alert(`Error: ${error.message}`);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-4xl">
        <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">
          Business Metrics Form Demo
        </h1>

        <div className="max-w-2xl mx-auto">
          <MetricsForm onSuccess={handleSuccess} onError={handleError} />
        </div>

        <div className="mt-8 max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Component Features</h2>
          <ul className="space-y-2 text-sm text-gray-700">
            <li>✓ Dropdown with common metric names</li>
            <li>✓ Custom metric name input option</li>
            <li>✓ Form validation (required fields, positive numbers)</li>
            <li>✓ Date picker with future date prevention</li>
            <li>✓ Integration with useMetricsForm hook</li>
            <li>✓ Success and error message display</li>
            <li>✓ Auto-clear form on successful submission</li>
            <li>✓ Tailwind CSS styling</li>
            <li>✓ Full accessibility support</li>
          </ul>

          <h2 className="text-xl font-semibold mt-6 mb-4">
            Example Metric Data
          </h2>
          <div className="bg-gray-50 rounded p-4">
            <pre className="text-xs overflow-x-auto">
              {JSON.stringify(
                {
                  metric_name: "Tons of Steel Produced",
                  value: 150000,
                  unit: "tons",
                  metric_date: "2024-10-01",
                },
                null,
                2
              )}
            </pre>
          </div>

          <h2 className="text-xl font-semibold mt-6 mb-4">
            Requirements Covered
          </h2>
          <ul className="space-y-1 text-sm text-gray-700">
            <li>• 2.1: Form with metric fields</li>
            <li>• 2.2: Dropdown for common metrics</li>
            <li>• 2.3: Positive number validation</li>
            <li>• 2.4: Date not in future validation</li>
            <li>• 2.5: POST request to backend</li>
            <li>• 2.6: Success message display</li>
            <li>• 2.7: Error message display</li>
            <li>• 2.8: Field validation and error highlighting</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default MetricsFormDemo;
