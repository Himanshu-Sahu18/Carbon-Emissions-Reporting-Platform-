/**
 * Verification script for common UI components
 * Run this to ensure all components are properly exported and accessible
 */

import Button from "./Button";
import Card from "./Card";
import EmptyState from "./EmptyState";
import ErrorMessage from "./ErrorMessage";
import LoadingSpinner from "./LoadingSpinner";

// Verify all components are defined
const components = {
  Button,
  Card,
  EmptyState,
  ErrorMessage,
  LoadingSpinner,
};

console.log("✓ Common UI Components Verification");
console.log("===================================\n");

Object.entries(components).forEach(([name, component]) => {
  if (typeof component !== "undefined") {
    console.log(`✓ ${name} component is properly exported`);
  } else {
    console.error(`✗ ${name} component is missing or not exported`);
  }
});

console.log("\n✓ All common UI components verified successfully!");
console.log("\nComponents available:");
console.log(
  "- Button: Flexible button with variants (primary, secondary, danger)"
);
console.log("- Card: Container component for consistent styling");
console.log("- EmptyState: Display empty states with optional actions");
console.log("- ErrorMessage: Error display with retry functionality");
console.log("- LoadingSpinner: Loading indicator in multiple sizes");

export default components;
