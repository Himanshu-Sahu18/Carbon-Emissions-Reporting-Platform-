# Common Components Quick Reference

## Import Statement

```tsx
import {
  Button,
  Card,
  LoadingSpinner,
  ErrorMessage,
  EmptyState,
} from "@/components";
```

## Button

### Basic Usage

```tsx
<Button onClick={handleClick}>Click Me</Button>
```

### Variants

```tsx
<Button variant="primary">Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="danger">Delete</Button>
```

### Sizes

```tsx
<Button size="sm">Small</Button>
<Button size="md">Medium</Button>
<Button size="lg">Large</Button>
```

### States

```tsx
<Button loading={isLoading}>Submit</Button>
<Button disabled>Disabled</Button>
<Button fullWidth>Full Width</Button>
```

---

## Card

### Basic Card

```tsx
<Card>
  <p>Content goes here</p>
</Card>
```

### Card with Title

```tsx
<Card title="Dashboard" subtitle="Overview of emissions">
  <p>Content</p>
</Card>
```

### Card with Header Action

```tsx
<Card title="Analytics" headerAction={<Button size="sm">Refresh</Button>}>
  <ChartComponent />
</Card>
```

### Custom Padding

```tsx
<Card padding="lg">Large padding content</Card>
<Card padding="none">No padding content</Card>
```

---

## LoadingSpinner

### Basic Usage

```tsx
{
  loading && <LoadingSpinner />;
}
```

### Different Sizes

```tsx
<LoadingSpinner size="sm" />
<LoadingSpinner size="md" />
<LoadingSpinner size="lg" />
```

### In a Container

```tsx
<div className="min-h-[200px] flex items-center justify-center">
  <LoadingSpinner size="lg" />
</div>
```

---

## ErrorMessage

### With Retry

```tsx
{
  error && <ErrorMessage message={error.message} onRetry={handleRetry} />;
}
```

### Without Retry

```tsx
<ErrorMessage message="Something went wrong" />
```

### Custom Styling

```tsx
<ErrorMessage message="Error occurred" className="my-4" />
```

---

## EmptyState

### Basic Usage

```tsx
<EmptyState message="No data available" />
```

### With Description

```tsx
<EmptyState
  message="No emissions recorded"
  description="Start by adding your first emission record"
/>
```

### With Action

```tsx
<EmptyState
  message="No data found"
  description="Try adjusting your filters"
  action={{
    label: "Reset Filters",
    onClick: handleReset,
  }}
/>
```

### With Custom Icon

```tsx
<EmptyState message="No results" icon={<CustomIcon />} />
```

---

## Common Patterns

### Loading State Pattern

```tsx
function MyComponent() {
  const { data, loading, error } = useData();

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error.message} />;
  if (!data) return <EmptyState message="No data" />;

  return <div>{/* Render data */}</div>;
}
```

### Card with Loading

```tsx
<Card title="Analytics">
  {loading ? (
    <LoadingSpinner />
  ) : error ? (
    <ErrorMessage message={error.message} onRetry={refetch} />
  ) : (
    <ChartComponent data={data} />
  )}
</Card>
```

### Form with Button States

```tsx
<form onSubmit={handleSubmit}>
  {/* Form fields */}
  <Button type="submit" loading={isSubmitting} fullWidth>
    {isSubmitting ? "Submitting..." : "Submit"}
  </Button>
</form>
```

### Dashboard Grid with Cards

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
  <Card title="Chart 1">
    <ChartComponent />
  </Card>
  <Card title="Chart 2">
    <ChartComponent />
  </Card>
</div>
```

---

## Accessibility Features

All components include:

- ✅ Semantic HTML
- ✅ ARIA labels and roles
- ✅ Keyboard navigation
- ✅ Screen reader support
- ✅ Focus indicators
- ✅ Color contrast compliance

---

## Styling Customization

All components accept a `className` prop for additional Tailwind classes:

```tsx
<Button className="mt-4 shadow-lg">Custom Styled</Button>
<Card className="border-2 border-blue-500">Custom Border</Card>
<LoadingSpinner className="my-8" />
```

---

## TypeScript Support

All components are fully typed. Import types if needed:

```tsx
import type { ButtonProps } from "@/components/common/Button";
import type { CardProps } from "@/components/common/Card";
```
