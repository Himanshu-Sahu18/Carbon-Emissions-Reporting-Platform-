import React, { useState } from "react";
import Button from "./Button";
import Card from "./Card";
import EmptyState from "./EmptyState";
import ErrorMessage from "./ErrorMessage";
import LoadingSpinner from "./LoadingSpinner";

/**
 * Demo component showcasing all common UI components
 * This file is for development/testing purposes only
 */
const ComponentDemo: React.FC = () => {
  const [loading, setLoading] = useState(false);

  const handleLoadingDemo = () => {
    setLoading(true);
    setTimeout(() => setLoading(false), 2000);
  };

  return (
    <div className="p-8 space-y-8 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold text-gray-900">
        Common Components Demo
      </h1>

      {/* Button Variants */}
      <Card title="Button Component" subtitle="Different variants and sizes">
        <div className="space-y-4">
          <div className="flex gap-4 items-center">
            <Button variant="primary">Primary Button</Button>
            <Button variant="secondary">Secondary Button</Button>
            <Button variant="danger">Danger Button</Button>
          </div>
          <div className="flex gap-4 items-center">
            <Button size="sm">Small</Button>
            <Button size="md">Medium</Button>
            <Button size="lg">Large</Button>
          </div>
          <div className="flex gap-4 items-center">
            <Button loading={loading} onClick={handleLoadingDemo}>
              {loading ? "Loading..." : "Click to Load"}
            </Button>
            <Button disabled>Disabled Button</Button>
          </div>
          <Button fullWidth>Full Width Button</Button>
        </div>
      </Card>

      {/* Loading Spinner */}
      <Card title="Loading Spinner" subtitle="Different sizes">
        <div className="flex gap-8 items-center">
          <div className="text-center">
            <LoadingSpinner size="sm" />
            <p className="mt-2 text-sm text-gray-600">Small</p>
          </div>
          <div className="text-center">
            <LoadingSpinner size="md" />
            <p className="mt-2 text-sm text-gray-600">Medium</p>
          </div>
          <div className="text-center">
            <LoadingSpinner size="lg" />
            <p className="mt-2 text-sm text-gray-600">Large</p>
          </div>
        </div>
      </Card>

      {/* Error Message */}
      <Card title="Error Message" subtitle="With and without retry">
        <div className="space-y-4">
          <ErrorMessage
            message="Something went wrong. Please try again."
            onRetry={() => alert("Retry clicked!")}
          />
          <ErrorMessage message="This is an error without retry functionality." />
        </div>
      </Card>

      {/* Empty State */}
      <Card title="Empty State" subtitle="Different configurations">
        <div className="space-y-8">
          <EmptyState
            message="No data available"
            description="Start by adding some emission records to see your dashboard"
            action={{
              label: "Add Record",
              onClick: () => alert("Add record clicked!"),
            }}
          />
          <EmptyState
            message="No results found"
            description="Try adjusting your filters"
          />
        </div>
      </Card>

      {/* Card Variations */}
      <Card
        title="Card with Header Action"
        subtitle="This card has an action button in the header"
        headerAction={
          <Button size="sm" variant="secondary">
            Refresh
          </Button>
        }
      >
        <p className="text-gray-700">
          This demonstrates a card with a header action button. Useful for
          refresh, settings, or other contextual actions.
        </p>
      </Card>

      <Card title="Card with Different Padding" padding="lg">
        <p className="text-gray-700">This card uses large padding.</p>
      </Card>
    </div>
  );
};

export default ComponentDemo;
