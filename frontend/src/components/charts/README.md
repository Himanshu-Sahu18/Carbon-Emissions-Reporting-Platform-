# Chart Components

This directory contains chart components for visualizing emission analytics data.

## YoYChart Component

The Year-over-Year Chart component displays a stacked bar chart comparing emissions by scope across two years.

### Features

- **Stacked Bar Chart**: Displays Scope 1, 2, and 3 emissions in stacked bars
- **Color Coding**: Uses distinct colors for each scope (Scope 1: red, Scope 2: blue, Scope 3: green)
- **Interactive Tooltips**: Shows scope name and emission value on hover
- **Percentage Change**: Displays year-over-year change percentage with visual indicator
- **Loading State**: Shows spinner while data is being fetched
- **Error Handling**: Displays error message with retry option
- **Empty State**: Shows message when no data is available
- **Responsive**: Adapts to different screen sizes

### Usage

```tsx
import { YoYChart } from "./components/charts";
import { useAnalytics } from "./hooks/useAnalytics";

function Dashboard() {
  const { yoyData, loading, error, refresh } = useAnalytics();

  return (
    <YoYChart
      data={yoyData}
      loading={loading}
      error={error}
      onRefresh={refresh}
    />
  );
}
```

### Props

| Prop           | Type                  | Required | Description                            |
| -------------- | --------------------- | -------- | -------------------------------------- |
| `data`         | `YoYResponse \| null` | No       | Year-over-year emissions data from API |
| `loading`      | `boolean`             | No       | Loading state indicator                |
| `error`        | `Error \| null`       | No       | Error object if data fetch failed      |
| `currentYear`  | `number`              | No       | Current year to display (optional)     |
| `previousYear` | `number`              | No       | Previous year to display (optional)    |
| `onRefresh`    | `() => void`          | No       | Callback function to refresh data      |

### Data Structure

The component expects data in the following format:

```typescript
interface YoYResponse {
  current_year: number;
  previous_year: number;
  current_year_data: ScopeEmission[];
  previous_year_data: ScopeEmission[];
  comparison: {
    total_current: number;
    total_previous: number;
    change_percentage: number;
    change_absolute: number;
  };
}

interface ScopeEmission {
  scope: number;
  total_emissions: number;
  unit: string;
}
```

### Styling

The component uses Tailwind CSS for styling and follows the design system:

- **Card**: White background with shadow and border
- **Colors**:
  - Scope 1: `#ef4444` (red)
  - Scope 2: `#3b82f6` (blue)
  - Scope 3: `#10b981` (green)
- **Typography**: Consistent font sizes and weights
- **Spacing**: Proper padding and margins

### Accessibility

- Semantic HTML structure
- ARIA labels for screen readers
- Keyboard navigation support
- Color contrast compliance
- Descriptive tooltips

### Requirements Satisfied

This component satisfies the following requirements:

- **3.1**: Fetches year-over-year data from the API
- **3.2**: Renders a stacked bar chart with two bars
- **3.3**: Displays separate stacks for Scope 1, 2, and 3
- **3.4**: Uses distinct colors for each scope
- **3.5**: Shows tooltips with scope name and emission value
- **3.6**: Includes axis labels
- **3.7**: Includes a legend identifying each scope
- **3.8**: Displays message when no data is available
- **10.2**: Uses Recharts charting library
