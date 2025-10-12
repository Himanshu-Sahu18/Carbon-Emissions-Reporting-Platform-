# Dashboard Layout Components

This directory contains the main layout components for the Carbon Emissions Dashboard.

## Components

### DashboardLayout

The main layout component that orchestrates the entire dashboard interface.

**Features:**

- Single-page layout with all components visible
- Responsive grid layout (mobile: stacked, tablet: 2-column, desktop: sidebar + main)
- Integrates with `useAnalytics` hook for data management
- Auto-refresh on form submission
- Global error handling with ErrorBoundary
- Loading states during data fetches
- Accessible with ARIA labels and semantic HTML

**Layout Structure:**

```
┌─────────────────────────────────────────────┐
│  Header (Logo, Title, Refresh Button)       │
├─────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────────────┐ │
│  │ Data Entry   │  │  Visualizations      │ │
│  │ - Emissions  │  │  ┌────────┬────────┐ │ │
│  │ - Metrics    │  │  │ YoY    │ Donut  │ │ │
│  │              │  │  └────────┴────────┘ │ │
│  │              │  │  ┌────────┬────────┐ │ │
│  │              │  │  │ KPI    │ Trend  │ │ │
│  └──────────────┘  │  └────────┴────────┘ │ │
│                    └──────────────────────┘ │
├─────────────────────────────────────────────┤
│  Footer                                      │
└─────────────────────────────────────────────┘
```

**Responsive Breakpoints:**

- Mobile (< 768px): Single column, stacked layout
- Tablet (768px - 1024px): 2-column grid for visualizations
- Desktop (> 1024px): Sidebar (4 cols) + Main content (8 cols)

**Usage:**

```tsx
import { DashboardLayout } from "./components";

function App() {
  return <DashboardLayout />;
}
```

### Header

The header component with branding and refresh functionality.

**Props:**

- `onRefresh?: () => void` - Callback function for refresh button
- `isRefreshing?: boolean` - Loading state for refresh button

**Features:**

- Logo and application title
- Responsive text (hides subtitle on mobile)
- Refresh button with loading animation
- Accessible with ARIA labels

**Usage:**

```tsx
<Header onRefresh={handleRefresh} isRefreshing={loading} />
```

## Integration with useAnalytics Hook

The DashboardLayout component integrates with the `useAnalytics` hook to:

1. Fetch all analytics data on mount
2. Provide refresh functionality via the header button
3. Auto-refresh after successful form submissions
4. Handle loading and error states globally

```tsx
const { loading, error, refresh } = useAnalytics();
```

## Error Handling

The layout is wrapped in an ErrorBoundary component that:

- Catches React component errors
- Displays user-friendly error messages
- Provides reload and home navigation options
- Shows stack traces in development mode

## Accessibility Features

- Semantic HTML elements (`<header>`, `<main>`, `<aside>`, `<section>`, `<footer>`)
- ARIA labels for sections and interactive elements
- Keyboard navigation support
- Screen reader friendly
- Focus indicators on interactive elements

## Styling

Uses Tailwind CSS with:

- Responsive utilities (`lg:col-span-8`, `md:col-span-2`)
- Consistent spacing (`space-y-6`, `gap-6`)
- Container constraints (`container mx-auto`)
- Accessible color contrast

## Requirements Satisfied

This implementation satisfies the following requirements from the spec:

- **7.1**: Single-page dashboard with all components visible
- **7.2**: Organized into data entry and visualization sections
- **7.3**: Responsive layout adapting to different screen sizes
- **7.4**: Header with application title and navigation elements
- **7.5**: Grid layout maximizing readability
- **7.6**: Loading indicators during data fetches
- **7.7**: Loading spinners for visualizations
- **7.8**: User-friendly error messages without breaking the dashboard

## Testing

Run tests with:

```bash
npm run test -- DashboardLayout.test.tsx
```

## Future Enhancements

- Add navigation tabs for different dashboard views
- Implement user preferences for layout customization
- Add export functionality for reports
- Implement dark mode support
