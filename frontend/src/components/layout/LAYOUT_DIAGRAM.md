# Dashboard Layout Visual Diagram

## Desktop Layout (> 1024px)

```
┌─────────────────────────────────────────────────────────────────────┐
│  🌍  Carbon Emissions Dashboard                    [🔄 Refresh]     │
│      Track and analyze your organization's carbon footprint         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────┐  ┌────────────────────────────────────┐  │
│  │  Submit Emissions    │  │  Analytics & Insights              │  │
│  │  Data                │  │                                    │  │
│  │  ┌────────────────┐  │  │  ┌──────────────────────────────┐ │  │
│  │  │ Activity Name  │  │  │  │  Year-over-Year Comparison   │ │  │
│  │  │ Activity Value │  │  │  │  ┌────┐         ┌────┐       │ │  │
│  │  │ Activity Unit  │  │  │  │  │2023│         │2024│       │ │  │
│  │  │ Activity Date  │  │  │  │  │ S3 │         │ S3 │       │ │  │
│  │  │ Location       │  │  │  │  │ S2 │         │ S2 │       │ │  │
│  │  │ Department     │  │  │  │  │ S1 │         │ S1 │       │ │  │
│  │  │                │  │  │  │  └────┘         └────┘       │ │  │
│  │  │   [Submit]     │  │  │  └──────────────────────────────┘ │  │
│  │  └────────────────┘  │  │                                    │  │
│  │                      │  │  ┌──────────────┐ ┌──────────────┐ │  │
│  │  Submit Business     │  │  │  Emission    │ │  Intensity   │ │  │
│  │  Metrics             │  │  │  Hotspots    │ │  KPI Card    │ │  │
│  │  ┌────────────────┐  │  │  │              │ │              │ │  │
│  │  │ Metric Name    │  │  │  │   ╱─────╲   │ │    0.83      │ │  │
│  │  │ Value          │  │  │  │ ╱  255k  ╲  │ │  kgCO2e/ton  │ │  │
│  │  │ Unit           │  │  │  ││  kgCO2e   │ │ │              │ │  │
│  │  │ Metric Date    │  │  │  │ ╲         ╱  │ │  Q1 2024     │ │  │
│  │  │                │  │  │  │   ╲─────╱   │ │              │ │  │
│  │  │   [Submit]     │  │  │  └──────────────┘ └──────────────┘ │  │
│  │  └────────────────┘  │  │                                    │  │
│  │                      │  │  ┌──────────────────────────────┐ │  │
│  └──────────────────────┘  │  │  Monthly Emissions Trend     │ │  │
│                             │  │              ●               │ │  │
│                             │  │            ╱                 │ │  │
│                             │  │          ●                   │ │  │
│                             │  │        ╱                     │ │  │
│                             │  │      ●                       │ │  │
│                             │  │    ╱                         │ │  │
│                             │  │  ●                           │ │  │
│                             │  │  J F M A M J J A S O N D     │ │  │
│                             │  └──────────────────────────────┘ │  │
│                             └────────────────────────────────────┘  │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│  Carbon Emissions Tracking Platform © 2025                          │
└─────────────────────────────────────────────────────────────────────┘
```

## Tablet Layout (768px - 1024px)

```
┌──────────────────────────────────────────┐
│  🌍  Carbon Emissions Dashboard  [🔄]    │
├──────────────────────────────────────────┤
│                                          │
│  Submit Emissions Data                   │
│  ┌────────────────────────────────────┐  │
│  │ Activity Name, Value, Unit, Date   │  │
│  │ Location, Department               │  │
│  │           [Submit]                 │  │
│  └────────────────────────────────────┘  │
│                                          │
│  Submit Business Metrics                 │
│  ┌────────────────────────────────────┐  │
│  │ Metric Name, Value, Unit, Date     │  │
│  │           [Submit]                 │  │
│  └────────────────────────────────────┘  │
│                                          │
│  Analytics & Insights                    │
│  ┌──────────────────────────────────┐   │
│  │  Year-over-Year Comparison       │   │
│  │  ┌────┐         ┌────┐           │   │
│  │  │2023│         │2024│           │   │
│  └──────────────────────────────────┘   │
│                                          │
│  ┌────────────────┐ ┌────────────────┐  │
│  │  Hotspots      │ │  Intensity KPI │  │
│  │   Donut        │ │     0.83       │  │
│  └────────────────┘ └────────────────┘  │
│                                          │
│  ┌──────────────────────────────────┐   │
│  │  Monthly Trend                   │   │
│  │      ●                           │   │
│  │    ╱                             │   │
│  │  ●                               │   │
│  └──────────────────────────────────┘   │
│                                          │
├──────────────────────────────────────────┤
│  © 2025                                  │
└──────────────────────────────────────────┘
```

## Mobile Layout (< 768px)

```
┌────────────────────────┐
│  🌍  Dashboard  [🔄]   │
├────────────────────────┤
│                        │
│  Submit Emissions      │
│  ┌──────────────────┐  │
│  │ Activity Name    │  │
│  │ Activity Value   │  │
│  │ Activity Unit    │  │
│  │ Activity Date    │  │
│  │ Location         │  │
│  │ Department       │  │
│  │    [Submit]      │  │
│  └──────────────────┘  │
│                        │
│  Submit Metrics        │
│  ┌──────────────────┐  │
│  │ Metric Name      │  │
│  │ Value            │  │
│  │ Unit             │  │
│  │ Metric Date      │  │
│  │    [Submit]      │  │
│  └──────────────────┘  │
│                        │
│  Analytics & Insights  │
│                        │
│  ┌──────────────────┐  │
│  │  YoY Comparison  │  │
│  │  ┌────┐  ┌────┐  │  │
│  │  │2023│  │2024│  │  │
│  └──────────────────┘  │
│                        │
│  ┌──────────────────┐  │
│  │  Hotspots Donut  │  │
│  │    ╱─────╲       │  │
│  │  ╱  255k  ╲      │  │
│  │  │ kgCO2e  │     │  │
│  │    ╲─────╱       │  │
│  └──────────────────┘  │
│                        │
│  ┌──────────────────┐  │
│  │  Intensity KPI   │  │
│  │      0.83        │  │
│  │   kgCO2e/ton     │  │
│  └──────────────────┘  │
│                        │
│  ┌──────────────────┐  │
│  │  Monthly Trend   │  │
│  │      ●           │  │
│  │    ╱             │  │
│  │  ●               │  │
│  └──────────────────┘  │
│                        │
├────────────────────────┤
│  © 2025                │
└────────────────────────┘
```

## Component Hierarchy

```
App
└── DashboardLayout
    ├── ErrorBoundary (wrapper)
    ├── Header
    │   ├── Logo (Globe Icon)
    │   ├── Title & Subtitle
    │   └── Refresh Button
    │
    ├── Main Content
    │   ├── Global Error Message (if error)
    │   │
    │   ├── Data Entry Section (Sidebar)
    │   │   ├── EmissionForm
    │   │   │   ├── Activity Name Input
    │   │   │   ├── Activity Value Input
    │   │   │   ├── Activity Unit Input
    │   │   │   ├── Activity Date Picker
    │   │   │   ├── Location Input
    │   │   │   ├── Department Input
    │   │   │   └── Submit Button
    │   │   │
    │   │   └── MetricsForm
    │   │       ├── Metric Name Dropdown
    │   │       ├── Value Input
    │   │       ├── Unit Input
    │   │       ├── Metric Date Picker
    │   │       └── Submit Button
    │   │
    │   └── Visualization Section (Main)
    │       ├── Loading Spinner (if loading)
    │       │
    │       └── Charts Grid (if loaded)
    │           ├── YoYChart (full width)
    │           ├── HotspotDonutChart
    │           ├── IntensityKPICard
    │           └── MonthlyTrendChart (full width)
    │
    └── Footer
        └── Copyright Text
```

## Grid System

### Desktop Grid (lg:grid-cols-12)

```
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│  1  │  2  │  3  │  4  │  5  │  6  │  7  │  8  │  9  │ 10  │ 11  │ 12  │
├─────┴─────┴─────┴─────┼─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┤
│                       │                                                 │
│   Sidebar (4 cols)    │         Main Content (8 cols)                  │
│   - Forms             │         - Charts in 2-column grid              │
│                       │                                                 │
└───────────────────────┴─────────────────────────────────────────────────┘
```

### Tablet/Mobile Grid (grid-cols-1)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                          Full Width (12 cols)                           │
│                          - Stacked Layout                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## State Management Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      DashboardLayout                             │
│                                                                  │
│  const { loading, error, refresh } = useAnalytics()             │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  useAnalytics Hook                                     │    │
│  │  ├── yoyData                                           │    │
│  │  ├── intensityData                                     │    │
│  │  ├── hotspotsData                                      │    │
│  │  ├── monthlyData                                       │    │
│  │  ├── loading                                           │    │
│  │  ├── error                                             │    │
│  │  └── refresh()                                         │    │
│  └────────────────────────────────────────────────────────┘    │
│                           │                                     │
│                           ├──> Header (onRefresh={refresh})    │
│                           │                                     │
│                           ├──> Forms (onSuccess={refresh})     │
│                           │                                     │
│                           └──> Charts (data from hook)         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Responsive Breakpoints

| Breakpoint    | Width          | Layout                            |
| ------------- | -------------- | --------------------------------- |
| Mobile        | < 768px        | Single column, stacked            |
| Tablet        | 768px - 1024px | 2-column grid for charts          |
| Desktop       | > 1024px       | Sidebar (4) + Main (8)            |
| Large Desktop | > 1280px       | Same as desktop with more spacing |

## Color Scheme

```
Background:     bg-gray-50      #F9FAFB
Cards:          bg-white        #FFFFFF
Text Primary:   text-gray-900   #111827
Text Secondary: text-gray-600   #4B5563
Borders:        border-gray-200 #E5E7EB
Primary:        bg-primary-500  #22C55E (Green)
Scope 1:        text-red-500    #EF4444
Scope 2:        text-blue-500   #3B82F6
Scope 3:        text-green-500  #10B981
```

## Accessibility Features

```
Semantic HTML:
  <header>    - Page header
  <main>      - Main content
  <aside>     - Sidebar with forms
  <section>   - Content sections
  <footer>    - Page footer

ARIA Labels:
  aria-label="Refresh dashboard data"
  aria-labelledby="emission-form-title"
  role="main"
  role="alert"

Screen Reader:
  <span className="sr-only">Loading...</span>
  Hidden text for context

Keyboard Navigation:
  Tab order follows visual flow
  Enter/Space activates buttons
  Focus indicators visible
```

## Loading States

```
Initial Load:
┌─────────────────────────┐
│  Header with Refresh    │
├─────────────────────────┤
│  Forms (always visible) │
│                         │
│  ┌───────────────────┐  │
│  │                   │  │
│  │   ⟳ Loading...    │  │
│  │                   │  │
│  └───────────────────┘  │
└─────────────────────────┘

Refresh:
┌─────────────────────────┐
│  Header [⟳ Refreshing]  │
├─────────────────────────┤
│  Forms (still visible)  │
│                         │
│  Charts (still visible) │
│  (with loading overlay) │
└─────────────────────────┘
```

## Error States

```
API Error:
┌─────────────────────────┐
│  Header with Refresh    │
├─────────────────────────┤
│  ⚠ Error Message        │
│  [Try Again]            │
├─────────────────────────┤
│  Forms (still visible)  │
│                         │
│  (Charts hidden)        │
└─────────────────────────┘

Component Error:
┌─────────────────────────┐
│  ⚠ Something went wrong │
│                         │
│  Error Details:         │
│  [Error message]        │
│                         │
│  [Reload Page] [Home]   │
└─────────────────────────┘
```
