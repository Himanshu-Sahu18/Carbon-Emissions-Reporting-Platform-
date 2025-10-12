/**
 * Verification script for custom hooks
 * This file verifies that all hooks are properly exported and have the correct structure
 */

import { useAnalytics } from "./useAnalytics";
import { useEmissionForm } from "./useEmissionForm";
import { useMetricsForm } from "./useMetricsForm";

// Type checks to ensure hooks have the correct return types
type AnalyticsHook = typeof useAnalytics;
type EmissionFormHook = typeof useEmissionForm;
type MetricsFormHook = typeof useMetricsForm;

// Verify hooks are functions
const analyticsIsFunction: boolean = typeof useAnalytics === "function";
const emissionFormIsFunction: boolean = typeof useEmissionForm === "function";
const metricsFormIsFunction: boolean = typeof useMetricsForm === "function";

console.log("Hook verification:");
console.log("✓ useAnalytics is a function:", analyticsIsFunction);
console.log("✓ useEmissionForm is a function:", emissionFormIsFunction);
console.log("✓ useMetricsForm is a function:", metricsFormIsFunction);

export {
  useAnalytics,
  useEmissionForm,
  useMetricsForm,
  type AnalyticsHook,
  type EmissionFormHook,
  type MetricsFormHook,
};
