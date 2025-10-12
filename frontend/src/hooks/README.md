# Custom Hooks

This directory contains custom React hooks for managing data fetching and form submissions in the Carbon Emissions Dashboard.

## Available Hooks

### `useAnalytics`

Fetches and manages all analytics data from the backend API.

**Usage:**

```typescript
import { useAnalytics } from "./hooks";

function Dashboard() {
  const {
    yoyData,
    intensityData,
    hotspotsData,
    monthlyData,
    loading,
    error,
    refresh,
  } = useAnalytics();

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} onRetry={refresh} />;

  return (
    <div>
      <YoYChart data={yoyData} />
      <IntensityKPI data={intensityData} />
      <HotspotsChart data={hotspotsData} />
      <MonthlyTrendChart data={monthlyData} />
      <button onClick={refresh}>Refresh Data</button>
    </div>
  );
}
```

**Return Values:**

- `yoyData`: Year-over-year emissions comparison data
- `intensityData`: Emission intensity metrics
- `hotspotsData`: Top emission sources
- `monthlyData`: Monthly emissions trend data
- `loading`: Boolean indicating if data is being fetched
- `error`: Error object if fetch failed, null otherwise
- `refresh`: Function to manually refresh all data

**Features:**

- Fetches all analytics data in parallel on mount
- Automatic error handling
- Manual refresh capability
- Loading state management

---

### `useEmissionForm`

Manages emission form submission with loading, error, and success states.

**Usage:**

```typescript
import { useEmissionForm } from "./hooks";

function EmissionForm() {
  const { submitEmission, loading, error, success, reset } = useEmissionForm(
    () => {
      console.log("Emission submitted successfully!");
      // Optionally refresh dashboard data
    }
  );

  const handleSubmit = async (formData: EmissionFormData) => {
    await submitEmission(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      {loading && <LoadingSpinner />}
      {error && <ErrorMessage error={error} />}
      {success && <SuccessMessage message="Emission submitted!" />}
      <button type="submit" disabled={loading}>
        Submit
      </button>
    </form>
  );
}
```

**Parameters:**

- `onSuccess` (optional): Callback function executed after successful submission

**Return Values:**

- `submitEmission`: Async function to submit emission data
- `loading`: Boolean indicating if submission is in progress
- `error`: Error object if submission failed, null otherwise
- `success`: Boolean indicating if submission was successful
- `reset`: Function to reset error and success states

**Features:**

- Automatic date formatting
- Error handling with detailed messages
- Success state management
- Optional success callback
- State reset functionality

---

### `useMetricsForm`

Manages business metrics form submission with loading, error, and success states.

**Usage:**

```typescript
import { useMetricsForm } from "./hooks";

function MetricsForm() {
  const { submitMetric, loading, error, success, reset } = useMetricsForm(
    () => {
      console.log("Metric submitted successfully!");
      // Optionally refresh dashboard data
    }
  );

  const handleSubmit = async (formData: MetricsFormData) => {
    await submitMetric(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      {loading && <LoadingSpinner />}
      {error && <ErrorMessage error={error} />}
      {success && <SuccessMessage message="Metric submitted!" />}
      <button type="submit" disabled={loading}>
        Submit
      </button>
    </form>
  );
}
```

**Parameters:**

- `onSuccess` (optional): Callback function executed after successful submission

**Return Values:**

- `submitMetric`: Async function to submit metrics data
- `loading`: Boolean indicating if submission is in progress
- `error`: Error object if submission failed, null otherwise
- `success`: Boolean indicating if submission was successful
- `reset`: Function to reset error and success states

**Features:**

- Automatic date formatting
- Error handling with detailed messages
- Success state management
- Optional success callback
- State reset functionality

---

## Common Patterns

### Combining Hooks

You can combine multiple hooks in a single component:

```typescript
function DashboardWithForms() {
  // Analytics data
  const { yoyData, loading, error, refresh } = useAnalytics();

  // Form submissions with auto-refresh
  const { submitEmission } = useEmissionForm(refresh);
  const { submitMetric } = useMetricsForm(refresh);

  return (
    <div>
      <EmissionForm onSubmit={submitEmission} />
      <MetricsForm onSubmit={submitMetric} />
      <AnalyticsCharts data={{ yoyData }} loading={loading} error={error} />
    </div>
  );
}
```

### Error Handling

All hooks provide consistent error handling:

```typescript
const { error } = useAnalytics();

if (error) {
  return (
    <div className="error-container">
      <p>Error: {error.message}</p>
      <button onClick={refresh}>Retry</button>
    </div>
  );
}
```

### Loading States

All hooks provide loading states for better UX:

```typescript
const { loading } = useAnalytics();

if (loading) {
  return <LoadingSpinner />;
}
```

## Requirements Satisfied

These hooks satisfy the following requirements from the spec:

- **Requirement 8.1**: Dashboard data fetching on load
- **Requirement 8.2**: Manual refresh functionality
- **Requirement 8.3**: Auto-refresh on form submission (via callbacks)
- **Requirement 8.6**: Error handling and retry options
- **Requirement 10.10**: State management patterns with React hooks

## Implementation Details

### State Management

All hooks use React's `useState` for local state management:

- Loading states
- Error states
- Success states
- Data states

### Performance Optimization

- `useCallback` is used to memoize functions and prevent unnecessary re-renders
- Parallel API calls in `useAnalytics` for faster data loading
- Proper cleanup and error handling

### Type Safety

All hooks are fully typed with TypeScript:

- Input parameters are typed
- Return values match defined interfaces
- Service layer integration is type-safe

## Testing

Unit tests for these hooks can be found in the `__tests__` directory (when implemented in task 19).

Example test structure:

```typescript
describe("useAnalytics", () => {
  it("should fetch analytics data on mount", async () => {
    const { result } = renderHook(() => useAnalytics());

    expect(result.current.loading).toBe(true);

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
      expect(result.current.yoyData).toBeDefined();
    });
  });
});
```
