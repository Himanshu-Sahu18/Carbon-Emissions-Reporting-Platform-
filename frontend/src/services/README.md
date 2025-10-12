# Services Layer

This directory contains the API client services for communicating with the backend.

## Structure

- `apiClient.ts` - Base API client class with axios instance and error handling interceptors
- `analyticsService.ts` - Service for fetching analytics data (YoY, intensity, hotspots)
- `emissionsService.ts` - Service for submitting emission records
- `metricsService.ts` - Service for submitting business metrics

## Configuration

The API base URL is configured via environment variables:

- Development: `.env.development` - `VITE_API_BASE_URL`
- Production: `.env.production` - `VITE_API_BASE_URL`

Default: `http://localhost:8000`

## Usage

### Analytics Service

```typescript
import { analyticsService } from "./services";

// Get Year-over-Year emissions
const yoyData = await analyticsService.getYoYEmissions(2024, 2023);

// Get emission intensity
const intensityData = await analyticsService.getEmissionIntensity(
  "2024-01-01",
  "2024-03-31",
  "Tons of Steel Produced"
);

// Get emission hotspots
const hotspotsData = await analyticsService.getEmissionHotspots({
  limit: 10,
  scope: 1,
});

// Get monthly emissions
const monthlyData = await analyticsService.getMonthlyEmissions(2024);
```

### Emissions Service

```typescript
import { emissionsService } from "./services";

// Create emission record
const emission = await emissionsService.createEmission({
  activity_name: "Diesel",
  activity_value: 1000,
  activity_unit: "litres",
  activity_date: "2024-10-01",
  scope: 1,
  location: "Plant A",
  department: "Production",
});
```

### Metrics Service

```typescript
import { metricsService } from "./services";

// Create business metric
const metric = await metricsService.createMetric({
  metric_name: "Tons of Steel Produced",
  value: 150000,
  unit: "tons",
  metric_date: "2024-10-01",
});
```

## Error Handling

All services include automatic error handling via axios interceptors:

- Network errors: "No response from server. Please check your connection."
- Server errors: Extracts error message from API response
- Request errors: "Failed to make request. Please try again."

Errors are thrown as standard JavaScript `Error` objects and should be caught in components/hooks.
