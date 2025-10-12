# Common UI Components

This directory contains reusable UI components used throughout the dashboard application.

## Components

### Button

A flexible button component with multiple variants and sizes.

**Props:**

- `variant`: 'primary' | 'secondary' | 'danger' (default: 'primary')
- `size`: 'sm' | 'md' | 'lg' (default: 'md')
- `fullWidth`: boolean (default: false)
- `loading`: boolean (default: false) - Shows loading spinner
- All standard button HTML attributes

**Usage:**

```tsx
import { Button } from '@/components';

<Button variant="primary" onClick={handleClick}>
  Submit
</Button>

<Button variant="secondary" size="sm" loading={isLoading}>
  Loading...
</Button>
```

### Card

A container component for consistent styling across the dashboard.

**Props:**

- `title`: string (optional) - Card header title
- `subtitle`: string (optional) - Card header subtitle
- `headerAction`: React.ReactNode (optional) - Action button/element in header
- `padding`: 'none' | 'sm' | 'md' | 'lg' (default: 'md')
- `className`: string (optional) - Additional CSS classes
- `children`: React.ReactNode - Card content

**Usage:**

```tsx
import { Card } from '@/components';

<Card title="Emissions Data" subtitle="Last 30 days">
  <p>Card content goes here</p>
</Card>

<Card
  title="Analytics"
  headerAction={<Button size="sm">Refresh</Button>}
>
  <ChartComponent />
</Card>
```

### LoadingSpinner

A loading spinner component for indicating loading states.

**Props:**

- `size`: 'sm' | 'md' | 'lg' (default: 'md')
- `className`: string (optional) - Additional CSS classes

**Usage:**

```tsx
import { LoadingSpinner } from "@/components";

{
  loading && <LoadingSpinner size="lg" />;
}
```

### ErrorMessage

An error message component with optional retry functionality.

**Props:**

- `message`: string - Error message to display
- `onRetry`: () => void (optional) - Callback for retry button
- `className`: string (optional) - Additional CSS classes

**Usage:**

```tsx
import { ErrorMessage } from "@/components";

{
  error && <ErrorMessage message={error.message} onRetry={handleRetry} />;
}
```

### EmptyState

A component for displaying empty states with optional actions.

**Props:**

- `message`: string - Main message to display
- `description`: string (optional) - Additional description
- `icon`: React.ReactNode (optional) - Custom icon
- `action`: { label: string, onClick: () => void } (optional) - Action button
- `className`: string (optional) - Additional CSS classes

**Usage:**

```tsx
import { EmptyState } from "@/components";

<EmptyState
  message="No data available"
  description="Start by adding some emission records"
  action={{
    label: "Add Record",
    onClick: handleAddRecord,
  }}
/>;
```

## Accessibility

All components follow WCAG 2.1 AA guidelines:

- Semantic HTML elements
- ARIA labels and roles
- Keyboard navigation support
- Sufficient color contrast
- Screen reader support

## Styling

Components use Tailwind CSS utility classes and follow the design system defined in the project's Tailwind configuration.
