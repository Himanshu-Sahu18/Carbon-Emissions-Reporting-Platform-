# MonthlyTrendChart Component

## Overview

The `MonthlyTrendChart` component displays a line chart tracking total monthly emissions over a specified year. It provides visual insights into emission patterns, seasonal trends, and month-to-month changes.

## Features

- **Line Chart Visualization**: Displays monthly emissions as a connected line chart
- **Month Labels**: X-axis shows abbreviated month names (Jan, Feb, Mar, etc.)
- **Data Points**: Each month with data is marked with a visible dot
- **Gap Handling**: Missing months are shown as gaps in the line (not interpolated)
- **Trend Indicator**: Shows whether emissions are increasing or decreasing over time
- **Statistics Summary**: Displays total, average, peak, and lowest emissions
- **Interactive Tooltips**: Hover over data points to see detailed emission values
- **Loading State**: Shows spinner while data is being fetched
- **Error State**: Displays error message with retry option
- **Empty State**: Shows helpful message when no data is available
- **Responsive Design**: Adapts to different screen sizes

## Usage

### Basic Usage

```tsx
import { MonthlyTrendChart } from "./components/charts";
import { useAnalytics } from "./hooks/useAnalytics";

function Dashboard() {
  const { monthlyData, loading, error, refresh } = useAnalytics();

  return (
    <MonthlyTrendChart
      data={monthlyData}
      loading={loading}
      error={error}
      onRefresh={refresh}
    />
  );
}
```

### With Custom Year

```tsx
<MonthlyTrendChart
  data={monthlyData}
  loading={loading}
  error={error}
  year={2023}
  onRefresh={refresh}
/>
```

### Standalone with Mock Data

```tsx
<MonthlyTrendChart
  data={{
    year: 2024,
    months: [
      {
        month: 1,
        month_name: "January",
        total_emissions: 45000,
        record_count: 12,
      },
      {
        month: 2,
        month_name: "February",
        total_emissions: 52000,
        record_count: 15,
      },
      // ... more months
    ],
  }}
  loading={false}
  error={null}
/>
```

## Props

| Prop        | Type                               | Required | Default | Description                                     |
| ----------- | ---------------------------------- | -------- | ------- | ----------------------------------------------- |
| `data`      | `MonthlyEmissionsResponse \| null` | No       | `null`  | Monthly emissions data from the API             |
| `loading`   | `boolean`                          | No       | `false` | Whether data is currently being loaded          |
| `error`     | `Error \| null`                    | No       | `null`  | Error object if data fetch failed               |
| `year`      | `number`                           | No       | -       | Year to display (overrides data.year in title)  |
| `onRefresh` | `() => void`                       | No       | -       | Callback function when refresh/retry is clicked |

## Data Structure

The component expects data in the following format:

```typescript
interface MonthlyEmissionsResponse {
  year: number;
  months: MonthlyEmission[];
}

interface MonthlyEmission {
  month: number; // 1-12
  month_name: string; // "January", "February", etc.
  total_emissions: number; // Total emissions in kgCO2e
  record_count: number; // Number of emission records
}
```

## Features in Detail

### Gap Handling

The component handles missing months intelligently:

- Creates a full 12-month array (Jan-Dec)
- Maps API data to corresponding months
- Missing months are shown as gaps in the line (not connected)
- This makes it clear which months have no data

### Trend Calculation

The component calculates a simple linear regression to determine if emissions are trending up or down:

- Uses all available data points
- Displays "↑ Increasing" or "↓ Decreasing" indicator
- Color-coded: red for increasing, green for decreasing

### Statistics

The component displays four key statistics:

- **Total**: Sum of all monthly emissions
- **Average**: Mean emissions across months with data
- **Peak**: Highest monthly emission value
- **Lowest**: Lowest monthly emission value

### Responsive Design

The statistics grid adapts to screen size:

- Mobile: 2 columns
- Tablet/Desktop: 4 columns

## Styling

The component uses Tailwind CSS classes and follows the design system:

- **Card**: White background with rounded corners and shadow
- **Line Color**: Blue (#3b82f6) for consistency with other charts
- **Trend Colors**: Red for increasing, green for decreasing
- **Grid**: Responsive grid for statistics

## Accessibility

- Semantic HTML structure
- ARIA labels for screen readers
- Keyboard-accessible tooltips
- Sufficient color contrast
- Descriptive axis labels

## Testing

To test the component in isolation:

```bash
# Run the test file
npm run dev -- --open /src/test-monthly-trend-chart.tsx
```

The test file includes examples of:

- Real data from API
- Loading state
- Error state
- Empty state
- Partial year data
- Full year with gaps

## Integration with Backend

The component expects data from the `/api/analytics/monthly` endpoint:

```
GET /api/analytics/monthly?year=2024
```

Response:

```json
{
  "year": 2024,
  "months": [
    {
      "month": 1,
      "month_name": "January",
      "total_emissions": 45000.5,
      "record_count": 12
    },
    ...
  ]
}
```

## Requirements Satisfied

This component satisfies the following requirements from the spec:

- **6.1**: Fetches monthly emission data for the current year
- **6.2**: Renders a line chart with months on X-axis and emissions on Y-axis
- **6.3**: Plots a line connecting monthly emission totals
- **6.4**: Includes data points for each month with values
- **6.5**: Displays tooltips showing month and emission value on hover
- **6.6**: Includes axis labels (Y-axis: "Emissions (kgCO2e)", X-axis: "Month")
- **6.7**: Formats X-axis with month abbreviations
- **6.8**: Handles missing data by showing gaps (not interpolating)
- **6.9**: Includes trend indicator to highlight overall trends
- **10.2**: Uses Recharts library for visualization

## Related Components

- `YoYChart`: Year-over-year comparison
- `HotspotDonutChart`: Emission source breakdown
- `IntensityKPICard`: Emission intensity metrics
- `useAnalytics`: Hook for fetching analytics data

## Notes

- The component does not interpolate missing data to maintain data integrity
- The trend calculation is a simple linear regression (not a moving average)
- All emissions are displayed in kgCO2e units
- The component is fully responsive and works on mobile, tablet, and desktop
