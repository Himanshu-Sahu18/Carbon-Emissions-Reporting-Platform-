# Carbon Emissions Dashboard - Frontend

A modern, responsive web application for tracking and visualizing carbon emissions data. Built with React, TypeScript, and Tailwind CSS, this dashboard provides an intuitive interface for submitting emission data and viewing advanced ESG analytics.

## Features

- **Data Entry Forms**: Submit Scope 1 emission activities and business metrics
- **Interactive Visualizations**:
  - Year-over-Year emissions comparison (stacked bar chart)
  - Emission hotspots breakdown (donut chart)
  - Emission intensity KPI card
  - Monthly emissions trend (line chart)
- **Responsive Design**: Optimized for mobile, tablet, and desktop
- **Accessibility**: WCAG 2.1 AA compliant with keyboard navigation and screen reader support
- **Real-time Updates**: Automatic data refresh after form submissions
- **Error Handling**: Comprehensive error handling with user-friendly messages

## Technology Stack

- **Framework**: React 19 with TypeScript
- **Build Tool**: Vite 7
- **Styling**: Tailwind CSS 4
- **Charts**: Recharts 3
- **Forms**: React Hook Form 7
- **HTTP Client**: Axios 1.12
- **State Management**: React hooks (useState, useEffect, useCallback)

## Prerequisites

- Node.js 18+ and npm 9+
- Backend API running (see backend README)

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Create environment files for development and production:

**Development (.env.development)**:

```env
VITE_API_BASE_URL=http://localhost:8000
```

**Production (.env.production)**:

```env
VITE_API_BASE_URL=/api
```

### 3. Run Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### 4. Build for Production

```bash
npm run build
```

The production build will be created in the `dist/` directory.

### 5. Preview Production Build

```bash
npm run preview
```

## Available Scripts

| Script                 | Description                                        |
| ---------------------- | -------------------------------------------------- |
| `npm run dev`          | Start development server with hot reload           |
| `npm run build`        | Build for production (runs TypeScript check first) |
| `npm run build:prod`   | Build for production with production mode          |
| `npm run lint`         | Run ESLint to check code quality                   |
| `npm run preview`      | Preview production build locally                   |
| `npm run docker:build` | Build Docker image                                 |
| `npm run docker:run`   | Run Docker container                               |

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── charts/         # Chart components (YoY, Donut, KPI, Line)
│   │   ├── common/         # Reusable UI components (Button, Card, etc.)
│   │   ├── forms/          # Form components (Emission, Metrics)
│   │   └── layout/         # Layout components (Dashboard, Header)
│   ├── hooks/              # Custom React hooks
│   │   ├── useAnalytics.ts    # Analytics data fetching
│   │   ├── useEmissionForm.ts # Emission form submission
│   │   └── useMetricsForm.ts  # Metrics form submission
│   ├── services/           # API service layer
│   │   ├── analyticsService.ts # Analytics API calls
│   │   ├── emissionsService.ts # Emissions API calls
│   │   ├── metricsService.ts   # Metrics API calls
│   │   └── apiClient.ts        # Base Axios configuration
│   ├── types/              # TypeScript type definitions
│   │   ├── api.types.ts       # API request/response types
│   │   ├── component.types.ts # Component prop types
│   │   └── hook.types.ts      # Hook return types
│   ├── utils/              # Utility functions
│   │   └── validation.ts      # Form validation rules
│   ├── App.tsx             # Main application component
│   ├── main.tsx            # Application entry point
│   └── index.css           # Global styles
├── public/                 # Static assets
├── dist/                   # Production build output
├── .env.development        # Development environment variables
├── .env.production         # Production environment variables
├── Dockerfile              # Docker configuration
├── nginx.conf              # Nginx configuration for production
├── package.json            # Dependencies and scripts
├── tsconfig.json           # TypeScript configuration
├── vite.config.ts          # Vite configuration
└── tailwind.config.js      # Tailwind CSS configuration
```

## Environment Variables

| Variable            | Description          | Default (Dev)           | Default (Prod) |
| ------------------- | -------------------- | ----------------------- | -------------- |
| `VITE_API_BASE_URL` | Backend API base URL | `http://localhost:8000` | `/api`         |

## Component API Reference

### Chart Components

#### YoYChart

Displays year-over-year emissions comparison by scope.

**Props**:

```typescript
interface YoYChartProps {
  data: YoYResponse | null;
  loading?: boolean;
  error?: Error | null;
  onRefresh?: () => void;
}
```

#### HotspotDonutChart

Shows emission hotspots as a donut chart.

**Props**:

```typescript
interface HotspotDonutChartProps {
  data: HotspotsResponse | null;
  loading?: boolean;
  error?: Error | null;
  onRefresh?: () => void;
}
```

#### IntensityKPICard

Displays emission intensity metric as a KPI card.

**Props**:

```typescript
interface IntensityKPICardProps {
  data: IntensityResponse | null;
  loading?: boolean;
  error?: Error | null;
  onRefresh?: () => void;
}
```

#### MonthlyTrendChart

Shows monthly emissions trend as a line chart.

**Props**:

```typescript
interface MonthlyTrendChartProps {
  data: MonthlyEmissionsResponse | null;
  loading?: boolean;
  error?: Error | null;
  onRefresh?: () => void;
}
```

### Form Components

#### EmissionForm

Form for submitting Scope 1 emission data.

**Props**:

```typescript
interface EmissionFormProps {
  onSuccess?: () => void;
  onError?: (error: Error) => void;
}
```

**Fields**:

- `activity_name` (required): Name of the emission activity
- `activity_value` (required): Numeric value of the activity
- `activity_unit` (required): Unit of measurement
- `activity_date` (required): Date of the activity (cannot be future)
- `location` (optional): Location where activity occurred
- `department` (optional): Department responsible

#### MetricsForm

Form for submitting business metrics.

**Props**:

```typescript
interface MetricsFormProps {
  onSuccess?: () => void;
  onError?: (error: Error) => void;
}
```

**Fields**:

- `metric_name` (required): Name of the metric
- `value` (required): Numeric value
- `unit` (required): Unit of measurement
- `metric_date` (required): Date of the metric (cannot be future)

### Custom Hooks

#### useAnalytics

Fetches and manages all analytics data.

**Returns**:

```typescript
interface UseAnalyticsReturn {
  yoyData: YoYResponse | null;
  intensityData: IntensityResponse | null;
  hotspotsData: HotspotsResponse | null;
  monthlyData: MonthlyEmissionsResponse | null;
  loading: boolean;
  refreshing: boolean;
  error: Error | null;
  refresh: () => Promise<void>;
}
```

#### useEmissionForm

Manages emission form submission.

**Returns**:

```typescript
interface UseEmissionFormReturn {
  submitEmission: (data: EmissionFormData) => Promise<void>;
  loading: boolean;
  error: Error | null;
  success: boolean;
  reset: () => void;
}
```

#### useMetricsForm

Manages metrics form submission.

**Returns**:

```typescript
interface UseMetricsFormReturn {
  submitMetric: (data: MetricsFormData) => Promise<void>;
  loading: boolean;
  error: Error | null;
  success: boolean;
  reset: () => void;
}
```

## Docker Deployment

### Build Docker Image

```bash
docker build -t ghg-frontend .
```

### Run Docker Container

```bash
docker run -p 80:80 ghg-frontend
```

### Using Docker Compose

The frontend is included in the main `docker-compose.yml` at the project root:

```bash
# From project root
docker-compose up -d
```

The frontend will be available at `http://localhost`

## Nginx Configuration

The production build uses Nginx to serve static files and proxy API requests. The configuration includes:

- Gzip compression for better performance
- Caching headers for static assets
- API proxy to backend at `/api`
- SPA routing support (all routes serve index.html)

See `nginx.conf` for full configuration.

## Accessibility Features

- **Keyboard Navigation**: All interactive elements accessible via Tab key
- **Screen Reader Support**: ARIA labels and semantic HTML throughout
- **Color Contrast**: WCAG AA compliant contrast ratios
- **Focus Indicators**: Clear visual focus states
- **Responsive Touch Targets**: Minimum 44x44px touch areas on mobile
- **Reduced Motion**: Respects user's motion preferences

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari 14+, Chrome Android 90+)

## Troubleshooting

### API Connection Issues

If you see "No response from server" errors:

1. Verify backend is running: `curl http://localhost:8000/api/health`
2. Check `VITE_API_BASE_URL` in your `.env` file
3. Ensure CORS is configured correctly in the backend

### Build Errors

If TypeScript compilation fails:

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Run TypeScript check
npx tsc --noEmit
```

### Port Already in Use

If port 5173 is already in use:

```bash
# Use a different port
npm run dev -- --port 3000
```

## Development Guidelines

### Code Style

- Use TypeScript for all new files
- Follow ESLint rules: `npm run lint`
- Use functional components with hooks
- Keep components small and focused (< 300 lines)
- Extract complex logic into custom hooks

### Component Structure

```typescript
// 1. Imports
import React from 'react';
import { useCustomHook } from '../hooks';

// 2. Type definitions
interface ComponentProps {
  // ...
}

// 3. Component definition with JSDoc
/**
 * Component description
 * @param props - Component props
 */
const Component: React.FC<ComponentProps> = ({ prop1, prop2 }) => {
  // 4. Hooks
  const { data, loading } = useCustomHook();

  // 5. Event handlers
  const handleClick = () => {
    // ...
  };

  // 6. Render logic
  if (loading) return <LoadingSpinner />;

  return (
    // JSX
  );
};

// 7. Export
export default Component;
```

### Adding New Components

1. Create component file in appropriate directory
2. Add TypeScript types in `src/types/`
3. Export from `index.ts` in the component directory
4. Add tests (if implementing test tasks)
5. Update this README if it's a major component

## Performance Optimization

- **Code Splitting**: Components are lazy-loaded where appropriate
- **Memoization**: Expensive calculations use `useMemo`
- **Debouncing**: Form inputs debounced to reduce API calls
- **Parallel Requests**: Analytics data fetched in parallel
- **Caching**: API responses cached for 5 minutes

## Contributing

1. Follow the existing code style and structure
2. Add TypeScript types for all new code
3. Ensure accessibility compliance
4. Test on multiple screen sizes
5. Run linter before committing: `npm run lint`

## License

This project is part of the Carbon Emissions Tracking Platform.

## Support

For issues or questions:

1. Check existing documentation in the `frontend/` directory
2. Review the design document at `.kiro/specs/frontend-dashboard/design.md`
3. Check the backend API documentation at `backend/API_DOCUMENTATION.md`
