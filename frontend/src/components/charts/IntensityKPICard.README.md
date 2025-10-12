# IntensityKPICard Component

## Overview

The `IntensityKPICard` component displays emission intensity metrics in a prominent, easy-to-read KPI card format. It shows the intensity value with color coding based on thresholds, along with supporting metrics like total emissions and production data.

## Features

✅ **Prominent Display**: Large, bold intensity value for quick visibility  
✅ **Color Coding**: Automatic color coding based on intensity thresholds (green/yellow/red)  
✅ **Supporting Metrics**: Shows total emissions, production, and data point count  
✅ **Date Range**: Displays the calculation period  
✅ **Loading State**: Shows spinner during data fetch  
✅ **Error Handling**: Displays error messages with retry option  
✅ **Empty States**: Handles missing data and no production data scenarios  
✅ **Responsive Design**: Adapts to different screen sizes  
✅ **Accessibility**: Includes proper ARIA labels and semantic HTML

## Usage

### Basic Usage with useAnalytics Hook

```tsx
import { IntensityKPICard } from "./components/charts";
import { useAnalytics } from "./hooks/useAnalytics";

function Dashboard() {
  const { intensityData, loading, error, refresh } = useAnalytics();

  return (
    <IntensityKPICard
      data={intensityData}
      loading={loading}
      error={error}
      startDate={new Date("2024-01-01")}
      endDate={new Date("2024-03-31")}
      metricName="Tons of Steel Produced"
      onRefresh={refresh}
    />
  );
}
```

### Custom Data

```tsx
import { IntensityKPICard } from "./components/charts";

function CustomKPI() {
  const customData = {
    period: {
      start_date: "2024-01-01",
      end_date: "2024-03-31",
    },
    metric_name: "Tons of Steel Produced",
    total_emissions: 125000,
    total_production: 150000,
    production_unit: "tons",
    intensity: 0.833,
    intensity_unit: "kgCO2e per ton",
    record_count: 52,
  };

  return (
    <IntensityKPICard
      data={customData}
      loading={false}
      error={null}
      startDate={new Date("2024-01-01")}
      endDate={new Date("2024-03-31")}
      metricName="Tons of Steel Produced"
    />
  );
}
```

## Props

| Prop         | Type                        | Required | Default     | Description                       |
| ------------ | --------------------------- | -------- | ----------- | --------------------------------- |
| `data`       | `IntensityResponse \| null` | No       | `undefined` | Intensity data from API           |
| `loading`    | `boolean`                   | No       | `false`     | Loading state indicator           |
| `error`      | `Error \| null`             | No       | `null`      | Error object if fetch failed      |
| `startDate`  | `Date`                      | Yes      | -           | Start date for calculation period |
| `endDate`    | `Date`                      | Yes      | -           | End date for calculation period   |
| `metricName` | `string`                    | Yes      | -           | Name of the business metric       |
| `onRefresh`  | `() => void`                | No       | `undefined` | Callback for refresh action       |

## Data Structure

The component expects data in the following format:

```typescript
interface IntensityResponse {
  period: {
    start_date: string; // ISO date format
    end_date: string; // ISO date format
  };
  metric_name: string;
  total_emissions: number; // in kgCO2e
  total_production: number; // production quantity
  production_unit: string; // e.g., "tons", "units"
  intensity: number; // emissions per production unit
  intensity_unit: string; // e.g., "kgCO2e per ton"
  record_count: number; // number of data points
}
```

## Color Coding Thresholds

The component applies color coding based on intensity values:

- **Green** (Low): intensity < 0.5
- **Yellow** (Medium): 0.5 ≤ intensity < 1.0
- **Red** (High): intensity ≥ 1.0

These thresholds can be adjusted in the component based on industry standards or organizational goals.

## States

### Loading State

Displays a centered loading spinner while data is being fetched.

### Error State

Shows an error message with the option to retry the data fetch.

### Empty State

Displays when no data is available for the selected period.

### No Production Data State

Shows a specific message when production data is unavailable, explaining that intensity cannot be calculated.

### Success State

Displays the full KPI card with:

- Large intensity value with color coding
- Intensity unit
- Date range
- Total emissions
- Total production
- Data point count
- Intensity level indicator legend

## Styling

The component uses Tailwind CSS classes for styling and follows the design system:

- **Card**: White background with shadow and border
- **Intensity Display**: Large text (6xl) with color-coded background
- **Supporting Metrics**: Smaller text with clear labels
- **Responsive**: Adapts to container width

## Accessibility

- Semantic HTML structure
- Calendar icon for date range
- Clear labels for all metrics
- Color is not the only indicator (text labels included)
- Proper contrast ratios

## Integration with Dashboard

The component is designed to work seamlessly with the dashboard layout:

```tsx
import {
  IntensityKPICard,
  YoYChart,
  HotspotDonutChart,
} from "./components/charts";
import { useAnalytics } from "./hooks/useAnalytics";

function Dashboard() {
  const { yoyData, intensityData, hotspotsData, loading, error, refresh } =
    useAnalytics();

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <YoYChart
        data={yoyData}
        loading={loading}
        error={error}
        onRefresh={refresh}
      />
      <HotspotDonutChart
        data={hotspotsData}
        loading={loading}
        error={error}
        onRefresh={refresh}
      />
      <IntensityKPICard
        data={intensityData}
        loading={loading}
        error={error}
        startDate={new Date("2024-01-01")}
        endDate={new Date("2024-03-31")}
        metricName="Tons of Steel Produced"
        onRefresh={refresh}
      />
    </div>
  );
}
```

## Requirements Mapping

This component satisfies the following requirements from the spec:

- **5.1**: Fetches intensity data from API endpoint
- **5.2**: Displays KPI card with intensity value
- **5.3**: Includes intensity unit
- **5.4**: Shows date range for calculation
- **5.5**: Displays supporting metrics (emissions, production)
- **5.6**: Optional trend indicator support (can be added)
- **5.7**: Visual styling with prominent metric value
- **5.8**: Handles missing production data scenario

## Testing

To test the component, use the test file:

```bash
# Run the test component
npm run dev
# Then navigate to the test page
```

The test file (`test-intensity-kpi.tsx`) includes:

- Loading state test
- Error state test
- Empty data test
- No production data test
- Low intensity test (green)
- Medium intensity test (yellow)
- High intensity test (red)

## Future Enhancements

Potential improvements for future iterations:

1. **Trend Indicator**: Add up/down arrow showing change from previous period
2. **Historical Comparison**: Show intensity values from previous periods
3. **Customizable Thresholds**: Allow configuration of color coding thresholds
4. **Export Functionality**: Add button to export KPI data
5. **Drill-down**: Click to see detailed breakdown of intensity calculation
6. **Multiple Metrics**: Support displaying multiple intensity metrics in one card
7. **Animations**: Add smooth transitions when data updates

## Related Components

- `YoYChart`: Year-over-year emissions comparison
- `HotspotDonutChart`: Emission source breakdown
- `MonthlyTrendChart`: Monthly emissions trend
- `LoadingSpinner`: Loading state indicator
- `ErrorMessage`: Error display component
- `EmptyState`: Empty state display component
