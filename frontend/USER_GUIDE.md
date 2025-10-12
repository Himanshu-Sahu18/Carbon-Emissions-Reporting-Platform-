# Carbon Emissions Dashboard - User Guide

Welcome to the Carbon Emissions Dashboard! This guide will help you understand and use all the features of the application.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard Overview](#dashboard-overview)
3. [Submitting Emission Data](#submitting-emission-data)
4. [Submitting Business Metrics](#submitting-business-metrics)
5. [Understanding Visualizations](#understanding-visualizations)
6. [Refreshing Data](#refreshing-data)
7. [Accessibility Features](#accessibility-features)
8. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Accessing the Dashboard

1. Open your web browser
2. Navigate to the dashboard URL (e.g., `http://localhost:5173` for development)
3. The dashboard will load automatically with the latest data

### System Requirements

- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection
- JavaScript enabled
- Minimum screen resolution: 320px width (mobile)

---

## Dashboard Overview

The dashboard is organized into two main sections:

### 1. Data Entry Section (Left Side)

Contains two forms for submitting data:

- **Emission Form**: Submit Scope 1 emission activities
- **Metrics Form**: Submit business metrics (production data)

### 2. Visualization Section (Right Side)

Displays four interactive charts:

- **Year-over-Year Chart**: Compare emissions across years
- **Emission Hotspots**: See which activities contribute most
- **Intensity KPI**: Track emissions per unit of production
- **Monthly Trend**: Monitor emissions over time

### Layout on Different Devices

**Desktop (1024px+)**:

- Forms on the left
- Charts in a 2x2 grid on the right

**Tablet (768px - 1024px)**:

- Forms at the top
- Charts in a 2-column grid below

**Mobile (< 768px)**:

- All components stacked vertically
- Optimized for touch interaction

---

## Submitting Emission Data

The Emission Form allows you to record Scope 1 emission activities (direct emissions from sources you own or control).

### Step-by-Step Instructions

1. **Locate the Emission Form** in the left sidebar or top section

2. **Fill in Required Fields** (marked with \*):

   **Activity Name**

   - Enter the name of the emission activity
   - Examples: "Diesel", "Natural Gas", "Company Vehicles"
   - Must be at least 2 characters

   **Activity Value**

   - Enter the numeric quantity
   - Must be a positive number
   - Can include decimals (e.g., 1000.50)

   **Activity Unit**

   - Enter the unit of measurement
   - Examples: "litres", "kWh", "km", "cubic meters"

   **Activity Date**

   - Select the date when the activity occurred
   - Cannot be a future date
   - Use the date picker or type in YYYY-MM-DD format

3. **Fill in Optional Fields**:

   **Location**

   - Where the activity occurred
   - Examples: "Plant A", "Building 3", "Warehouse"
   - Maximum 100 characters

   **Department**

   - Which department is responsible
   - Examples: "Production", "Operations", "Logistics"
   - Maximum 100 characters

4. **Submit the Form**
   - Click the "Submit Emission Data" button
   - Wait for the success message
   - The form will clear automatically

### Example Submission

```
Activity Name: Diesel
Activity Value: 1500
Activity Unit: litres
Activity Date: 2024-10-15
Location: Plant A
Department: Production
```

### Validation Rules

- All required fields must be filled
- Activity value must be positive
- Activity date cannot be in the future
- If validation fails, error messages will appear below the relevant fields

### Success and Error Messages

**Success**: Green notification appears at the bottom of the form

- "Emission data submitted successfully!"
- Form clears automatically
- Dashboard data may refresh

**Error**: Red notification appears with details

- Read the error message
- Correct the issue
- Try submitting again

---

## Submitting Business Metrics

The Metrics Form allows you to record business metrics like production volume, which are used to calculate emission intensity.

### Step-by-Step Instructions

1. **Locate the Metrics Form** below the Emission Form

2. **Fill in Required Fields**:

   **Metric Name**

   - Select from dropdown or enter custom name
   - Common options:
     - "Tons of Steel Produced"
     - "Units Manufactured"
     - "Square Meters Produced"
     - "Revenue (USD)"

   **Value**

   - Enter the numeric value
   - Must be a positive number
   - Can include decimals

   **Unit**

   - Enter the unit of measurement
   - Examples: "tons", "units", "square meters", "USD"

   **Metric Date**

   - Select the date for this metric
   - Cannot be a future date

3. **Submit the Form**
   - Click the "Submit Metric Data" button
   - Wait for the success message
   - Form clears automatically

### Example Submission

```
Metric Name: Tons of Steel Produced
Value: 15000
Unit: tons
Metric Date: 2024-10-15
```

### Why Submit Metrics?

Business metrics are essential for calculating **emission intensity**, which shows how efficiently you're producing relative to your emissions. For example:

- Total Emissions: 125,000 kgCO2e
- Production: 150,000 tons
- **Intensity: 0.83 kgCO2e per ton**

This helps you track whether you're becoming more or less carbon-efficient over time.

---

## Understanding Visualizations

### 1. Year-over-Year Emissions Chart

**What it shows**: Comparison of total emissions between the current year and previous year, broken down by scope.

**How to read it**:

- Two bars: one for each year
- Each bar is divided into three colored sections:
  - **Red**: Scope 1 (direct emissions)
  - **Blue**: Scope 2 (indirect emissions from energy)
  - **Green**: Scope 3 (other indirect emissions)
- Percentage change shown in top-right corner
  - ↑ Red = Emissions increased
  - ↓ Green = Emissions decreased

**Interactive features**:

- Hover over any section to see exact values
- Legend at bottom identifies each scope

**What to look for**:

- Are emissions trending up or down?
- Which scope contributes most?
- How much progress toward reduction goals?

### 2. Emission Hotspots Donut Chart

**What it shows**: Percentage breakdown of emissions by activity type.

**How to read it**:

- Each colored segment represents an emission source
- Segment size = percentage of total emissions
- Center shows total emissions value
- Legend lists all activities with colors

**Interactive features**:

- Hover over segments for details:
  - Activity name
  - Total emissions
  - Percentage of total
  - Number of records

**What to look for**:

- Which activities are the biggest contributors?
- Where should reduction efforts focus?
- Are there any surprising hotspots?

### 3. Emission Intensity KPI Card

**What it shows**: Emissions per unit of production (efficiency metric).

**How to read it**:

- Large number = intensity value
- Unit shown below (e.g., "kgCO2e per ton")
- Period indicates date range
- Supporting metrics show totals

**Color coding**:

- **Green**: Good efficiency
- **Yellow**: Moderate efficiency
- **Red**: High intensity (needs improvement)

**What to look for**:

- Is intensity improving over time?
- How does it compare to industry benchmarks?
- Impact of efficiency initiatives

### 4. Monthly Emissions Trend Chart

**What it shows**: Total emissions for each month of the current year.

**How to read it**:

- X-axis: Months (Jan, Feb, Mar, etc.)
- Y-axis: Total emissions (kgCO2e)
- Line connects monthly totals
- Data points show exact values

**Interactive features**:

- Hover over points to see month and value

**What to look for**:

- Seasonal patterns
- Month-to-month changes
- Impact of reduction initiatives
- Unusual spikes or drops

---

## Refreshing Data

### Manual Refresh

1. **Locate the Refresh Button** in the top-right corner of the header
2. **Click the button** (circular arrow icon)
3. **Wait for data to reload**
   - Charts will show loading indicators
   - Existing data remains visible during refresh
4. **View updated data** once loading completes

### Automatic Refresh

The dashboard may automatically refresh after:

- Submitting emission data
- Submitting business metrics
- Successful form submissions

### When to Refresh

- After submitting new data
- When you suspect data is outdated
- If you see an error and want to retry
- After other users submit data

---

## Accessibility Features

The dashboard is designed to be accessible to all users.

### Keyboard Navigation

**Tab Key**: Move between interactive elements

- Forms fields
- Buttons
- Chart elements

**Enter/Space**: Activate buttons and controls

**Shift + Tab**: Move backward through elements

**Escape**: Close modals or dialogs (if any)

### Screen Reader Support

All charts and visualizations include:

- Descriptive ARIA labels
- Text alternatives for visual data
- Semantic HTML structure
- Status announcements for dynamic content

**Example**: When hovering over the YoY chart, screen readers announce:

> "Year-over-year emissions comparison chart. 2023 total emissions: 250,000 kilograms CO2 equivalent. 2024 total emissions: 275,000 kilograms CO2 equivalent. This represents an increase of 10 percent."

### Visual Accessibility

- **High Contrast**: All text meets WCAG AA standards
- **Focus Indicators**: Clear visual focus on active elements
- **Color Independence**: Information not conveyed by color alone
- **Responsive Text**: Text scales with browser zoom

### Touch Accessibility

On mobile devices:

- Minimum 44x44px touch targets
- Adequate spacing between interactive elements
- Touch-friendly form controls
- Swipe-friendly charts

### Reduced Motion

If you have "Reduce Motion" enabled in your system settings:

- Animations are minimized
- Transitions are simplified
- Charts load without animation

---

## Troubleshooting

### Common Issues and Solutions

#### "No response from server" Error

**Problem**: Cannot connect to the backend API

**Solutions**:

1. Check your internet connection
2. Verify the backend server is running
3. Contact your system administrator
4. Try refreshing the page

#### Form Validation Errors

**Problem**: Cannot submit form due to validation errors

**Solutions**:

1. Read error messages below each field
2. Ensure all required fields are filled
3. Check that values are positive numbers
4. Verify dates are not in the future
5. Remove any special characters if not allowed

#### Charts Not Loading

**Problem**: Charts show loading spinner indefinitely

**Solutions**:

1. Click the refresh button
2. Check browser console for errors (F12)
3. Verify backend API is accessible
4. Clear browser cache and reload
5. Try a different browser

#### "No data available" Message

**Problem**: Charts show empty state

**Solutions**:

1. Submit some emission data first
2. Check date filters (if any)
3. Verify data exists in the database
4. Contact administrator to check backend

#### Mobile Display Issues

**Problem**: Layout looks broken on mobile

**Solutions**:

1. Rotate device to landscape mode
2. Zoom out if zoomed in
3. Update browser to latest version
4. Clear browser cache
5. Try a different mobile browser

#### Slow Performance

**Problem**: Dashboard is slow or unresponsive

**Solutions**:

1. Close other browser tabs
2. Clear browser cache
3. Check internet connection speed
4. Disable browser extensions
5. Try a different browser

### Getting Help

If you continue to experience issues:

1. **Check Documentation**:

   - README.md for setup instructions
   - COMPONENT_API.md for technical details
   - Backend API documentation

2. **Browser Console**:

   - Press F12 to open developer tools
   - Check Console tab for error messages
   - Share error messages with support

3. **Contact Support**:
   - Provide error messages
   - Describe steps to reproduce
   - Include browser and OS information
   - Share screenshots if helpful

---

## Tips for Best Results

### Data Entry Best Practices

1. **Be Consistent**: Use the same naming conventions

   - "Diesel" not "diesel" or "DIESEL"
   - "litres" not "L" or "liters"

2. **Enter Data Regularly**: Don't wait until month-end

   - More accurate trends
   - Easier to remember details
   - Better real-time insights

3. **Use Optional Fields**: Location and department help with:

   - Detailed analysis
   - Identifying improvement areas
   - Accountability

4. **Double-Check Values**: Before submitting:
   - Correct units
   - Reasonable quantities
   - Accurate dates

### Analyzing Data Effectively

1. **Look for Patterns**:

   - Seasonal variations
   - Day-of-week effects
   - Impact of initiatives

2. **Compare Periods**:

   - Month-over-month
   - Year-over-year
   - Before/after changes

3. **Focus on Hotspots**:

   - Biggest contributors
   - Easiest to reduce
   - Quick wins

4. **Track Intensity**:
   - More meaningful than absolute emissions
   - Accounts for production changes
   - Better for benchmarking

### Dashboard Maintenance

1. **Regular Refresh**: Keep data current
2. **Monitor Errors**: Address issues promptly
3. **Update Browser**: Use latest version
4. **Clear Cache**: Periodically clear browser cache
5. **Report Issues**: Help improve the system

---

## Frequently Asked Questions

**Q: How often is data updated?**
A: Data updates immediately after submission. Charts refresh when you click the refresh button or after form submissions.

**Q: Can I edit or delete submitted data?**
A: Currently, data cannot be edited through the dashboard. Contact your administrator for data corrections.

**Q: What's the difference between Scope 1, 2, and 3?**
A:

- **Scope 1**: Direct emissions you control (vehicles, facilities)
- **Scope 2**: Indirect emissions from purchased energy
- **Scope 3**: Other indirect emissions (supply chain, travel)

**Q: Why is my intensity metric not showing?**
A: You need to submit business metrics (production data) for the same period as your emissions data.

**Q: Can I export data or charts?**
A: Export functionality may be available through the backend API. Contact your administrator.

**Q: Does the dashboard work offline?**
A: No, an internet connection is required to fetch and submit data.

**Q: Can multiple users submit data simultaneously?**
A: Yes, the system supports multiple concurrent users.

**Q: How far back does historical data go?**
A: This depends on when your organization started using the system. The YoY chart compares the current and previous year.

---

## Glossary

**Emission**: Release of greenhouse gases into the atmosphere

**kgCO2e**: Kilograms of carbon dioxide equivalent (standard unit)

**Scope 1/2/3**: Categories of emissions based on source

**Intensity**: Emissions per unit of production (efficiency metric)

**Hotspot**: Activity or source with high emissions

**YoY**: Year-over-Year (comparison between years)

**KPI**: Key Performance Indicator (important metric)

**API**: Application Programming Interface (backend connection)

---

## Additional Resources

- **Technical Documentation**: See README.md
- **Component API**: See COMPONENT_API.md
- **Backend API**: See backend/API_DOCUMENTATION.md
- **Deployment Guide**: See DEPLOYMENT.md
- **Accessibility Guide**: See ACCESSIBILITY.md

---

**Last Updated**: January 2025
**Version**: 1.0
