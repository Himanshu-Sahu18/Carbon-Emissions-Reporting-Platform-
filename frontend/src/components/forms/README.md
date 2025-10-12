# Form Components

This directory contains form components for data entry in the Carbon Emissions Dashboard.

## EmissionForm

A comprehensive form component for submitting Scope 1 emission data.

### Features

- **React Hook Form Integration**: Uses react-hook-form for efficient form state management and validation
- **Comprehensive Validation**:
  - Required field validation
  - Positive number validation for activity values
  - Date validation (prevents future dates)
  - Character length limits for optional fields
- **User Feedback**:
  - Success messages with auto-dismiss
  - Error messages with retry functionality
  - Field-level validation errors
  - Loading states during submission
- **Accessibility**:
  - ARIA labels and descriptions
  - Semantic HTML
  - Keyboard navigation support
  - Screen reader friendly error messages
- **Auto-clear**: Form automatically clears on successful submission

### Usage

```tsx
import { EmissionForm } from "./components";

function App() {
  const handleSuccess = () => {
    console.log("Emission submitted successfully!");
    // Optionally refresh dashboard data
  };

  const handleError = (error: Error) => {
    console.error("Error submitting emission:", error);
  };

  return <EmissionForm onSuccess={handleSuccess} onError={handleError} />;
}
```

### Props

| Prop        | Type                     | Required | Description                                          |
| ----------- | ------------------------ | -------- | ---------------------------------------------------- |
| `onSuccess` | `() => void`             | No       | Callback function called after successful submission |
| `onError`   | `(error: Error) => void` | No       | Callback function called when submission fails       |

### Form Fields

| Field            | Type   | Required | Validation         |
| ---------------- | ------ | -------- | ------------------ |
| `activity_name`  | text   | Yes      | Min 2 characters   |
| `activity_value` | number | Yes      | Positive number    |
| `activity_unit`  | text   | Yes      | Required           |
| `activity_date`  | date   | Yes      | Not in future      |
| `location`       | text   | No       | Max 100 characters |
| `department`     | text   | No       | Max 100 characters |

### API Integration

The form integrates with the `useEmissionForm` hook which calls the emissions service to submit data to:

```
POST /api/emissions/
```

### Styling

The component uses Tailwind CSS for styling and follows the design system established in the common components. It includes:

- Responsive layout
- Focus states for accessibility
- Error state styling
- Loading indicators
- Success/error message styling

### Example Data

```json
{
  "activity_name": "Diesel",
  "activity_value": 1000,
  "activity_unit": "litres",
  "activity_date": "2024-10-01",
  "scope": 1,
  "location": "Plant A",
  "department": "Production"
}
```

### Requirements Covered

This component satisfies the following requirements from the spec:

- 1.1: Display form with fields for Scope 1 emission data entry
- 1.2: Include all required input fields
- 1.3: Optional autocomplete suggestions (prepared for future enhancement)
- 1.4: Validate positive numbers
- 1.5: Ensure date is not in future
- 1.6: Send POST request to backend API
- 1.7: Display success message and clear form
- 1.8: Display error messages from API
- 1.9: Highlight invalid fields with error messages

---

## MetricsForm

A comprehensive form component for submitting business metrics (production data).

### Features

- **React Hook Form Integration**: Uses react-hook-form for efficient form state management and validation
- **Dropdown Selection**: Provides common metric names in a dropdown with custom option
- **Dynamic Custom Input**: Shows custom metric name input when "Custom" is selected
- **Comprehensive Validation**:
  - Required field validation
  - Positive number validation for metric values
  - Date validation (prevents future dates)
- **User Feedback**:
  - Success messages with auto-dismiss
  - Error messages with retry functionality
  - Field-level validation errors
  - Loading states during submission
- **Accessibility**:
  - ARIA labels and descriptions
  - Semantic HTML
  - Keyboard navigation support
  - Screen reader friendly error messages
- **Auto-clear**: Form automatically clears on successful submission

### Usage

```tsx
import { MetricsForm } from "./components";

function App() {
  const handleSuccess = () => {
    console.log("Metric submitted successfully!");
    // Optionally refresh dashboard data
  };

  const handleError = (error: Error) => {
    console.error("Error submitting metric:", error);
  };

  return <MetricsForm onSuccess={handleSuccess} onError={handleError} />;
}
```

### Props

| Prop        | Type                     | Required | Description                                          |
| ----------- | ------------------------ | -------- | ---------------------------------------------------- |
| `onSuccess` | `() => void`             | No       | Callback function called after successful submission |
| `onError`   | `(error: Error) => void` | No       | Callback function called when submission fails       |

### Form Fields

| Field         | Type     | Required | Validation      |
| ------------- | -------- | -------- | --------------- |
| `metric_name` | dropdown | Yes      | Required        |
| `value`       | number   | Yes      | Positive number |
| `unit`        | text     | Yes      | Required        |
| `metric_date` | date     | Yes      | Not in future   |

### Common Metrics

The dropdown includes the following common metric names:

- Tons of Steel Produced
- Units Manufactured
- Square Meters Produced
- Revenue (USD)
- Custom (allows user to enter custom metric name)

### API Integration

The form integrates with the `useMetricsForm` hook which calls the metrics service to submit data to:

```
POST /api/metrics/
```

### Styling

The component uses Tailwind CSS for styling and follows the design system established in the common components. It includes:

- Responsive layout
- Focus states for accessibility
- Error state styling
- Loading indicators
- Success/error message styling

### Example Data

```json
{
  "metric_name": "Tons of Steel Produced",
  "value": 150000,
  "unit": "tons",
  "metric_date": "2024-10-01"
}
```

### Requirements Covered

This component satisfies the following requirements from the spec:

- 2.1: Display form for submitting business metric data
- 2.2: Include all required input fields (metric_name, value, unit, metric_date)
- 2.3: Validate positive numbers for value field
- 2.4: Ensure date is not in future
- 2.5: Send POST request to backend API endpoint
- 2.6: Display success message and clear form
- 2.7: Display error messages from API
- 2.8: Highlight invalid fields with error messages
