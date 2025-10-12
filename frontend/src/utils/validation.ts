/**
 * Validation utilities and schemas for form validation
 * Provides reusable validation rules and error messages
 */

import type { EmissionFormData, MetricsFormData } from "../types/api.types";

/**
 * Validation error messages
 */
export const ValidationMessages = {
  required: (field: string) => `${field} is required`,
  minLength: (field: string, min: number) =>
    `${field} must be at least ${min} characters`,
  maxLength: (field: string, max: number) =>
    `${field} must not exceed ${max} characters`,
  positiveNumber: (field: string) => `${field} must be a positive number`,
  futureDate: "Date cannot be in the future",
  invalidDate: "Please enter a valid date",
  invalidEmail: "Please enter a valid email address",
  invalidUrl: "Please enter a valid URL",
} as const;

/**
 * Common validation rules
 */
export const ValidationRules = {
  /**
   * Validate that a value is not empty
   */
  required: (value: any): boolean => {
    if (typeof value === "string") {
      return value.trim().length > 0;
    }
    return value !== null && value !== undefined && value !== "";
  },

  /**
   * Validate minimum length for strings
   */
  minLength: (value: string, min: number): boolean => {
    return value.trim().length >= min;
  },

  /**
   * Validate maximum length for strings
   */
  maxLength: (value: string, max: number): boolean => {
    return value.trim().length <= max;
  },

  /**
   * Validate positive number
   */
  positiveNumber: (value: number): boolean => {
    return !isNaN(value) && value > 0;
  },

  /**
   * Validate that date is not in the future
   */
  notFutureDate: (date: Date | string): boolean => {
    const selectedDate = new Date(date);
    const currentDate = new Date();
    currentDate.setHours(0, 0, 0, 0);
    selectedDate.setHours(0, 0, 0, 0);
    return selectedDate <= currentDate;
  },

  /**
   * Validate email format
   */
  email: (value: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(value);
  },

  /**
   * Validate URL format
   */
  url: (value: string): boolean => {
    try {
      new URL(value);
      return true;
    } catch {
      return false;
    }
  },
} as const;

/**
 * Emission Form Validation Schema
 * React Hook Form compatible validation rules
 */
export const emissionFormValidation = {
  activity_name: {
    required: ValidationMessages.required("Activity name"),
    minLength: {
      value: 2,
      message: ValidationMessages.minLength("Activity name", 2),
    },
    maxLength: {
      value: 100,
      message: ValidationMessages.maxLength("Activity name", 100),
    },
  },
  activity_value: {
    required: ValidationMessages.required("Activity value"),
    min: {
      value: 0.01,
      message: ValidationMessages.positiveNumber("Activity value"),
    },
    valueAsNumber: true,
  },
  activity_unit: {
    required: ValidationMessages.required("Activity unit"),
    maxLength: {
      value: 50,
      message: ValidationMessages.maxLength("Activity unit", 50),
    },
  },
  activity_date: {
    required: ValidationMessages.required("Activity date"),
    validate: (value: string | Date) => {
      if (!ValidationRules.notFutureDate(value)) {
        return ValidationMessages.futureDate;
      }
      return true;
    },
  },
  location: {
    maxLength: {
      value: 100,
      message: ValidationMessages.maxLength("Location", 100),
    },
  },
  department: {
    maxLength: {
      value: 100,
      message: ValidationMessages.maxLength("Department", 100),
    },
  },
} as const;

/**
 * Metrics Form Validation Schema
 * React Hook Form compatible validation rules
 */
export const metricsFormValidation = {
  metric_name: {
    required: ValidationMessages.required("Metric name"),
    minLength: {
      value: 2,
      message: ValidationMessages.minLength("Metric name", 2),
    },
    maxLength: {
      value: 100,
      message: ValidationMessages.maxLength("Metric name", 100),
    },
  },
  value: {
    required: ValidationMessages.required("Value"),
    min: {
      value: 0.01,
      message: ValidationMessages.positiveNumber("Value"),
    },
    valueAsNumber: true,
  },
  unit: {
    required: ValidationMessages.required("Unit"),
    maxLength: {
      value: 50,
      message: ValidationMessages.maxLength("Unit", 50),
    },
  },
  metric_date: {
    required: ValidationMessages.required("Metric date"),
    validate: (value: string | Date) => {
      if (!ValidationRules.notFutureDate(value)) {
        return ValidationMessages.futureDate;
      }
      return true;
    },
  },
} as const;

/**
 * Validate emission form data programmatically
 * Useful for custom validation outside of React Hook Form
 */
export function validateEmissionForm(data: Partial<EmissionFormData>): {
  isValid: boolean;
  errors: Record<string, string>;
} {
  const errors: Record<string, string> = {};

  // Activity name validation
  if (!data.activity_name || !ValidationRules.required(data.activity_name)) {
    errors.activity_name = ValidationMessages.required("Activity name");
  } else if (!ValidationRules.minLength(data.activity_name, 2)) {
    errors.activity_name = ValidationMessages.minLength("Activity name", 2);
  }

  // Activity value validation
  if (
    data.activity_value === undefined ||
    data.activity_value === null ||
    !ValidationRules.positiveNumber(data.activity_value)
  ) {
    errors.activity_value = ValidationMessages.positiveNumber("Activity value");
  }

  // Activity unit validation
  if (!data.activity_unit || !ValidationRules.required(data.activity_unit)) {
    errors.activity_unit = ValidationMessages.required("Activity unit");
  }

  // Activity date validation
  if (!data.activity_date) {
    errors.activity_date = ValidationMessages.required("Activity date");
  } else if (!ValidationRules.notFutureDate(data.activity_date)) {
    errors.activity_date = ValidationMessages.futureDate;
  }

  // Optional fields validation
  if (data.location && !ValidationRules.maxLength(data.location, 100)) {
    errors.location = ValidationMessages.maxLength("Location", 100);
  }

  if (data.department && !ValidationRules.maxLength(data.department, 100)) {
    errors.department = ValidationMessages.maxLength("Department", 100);
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  };
}

/**
 * Validate metrics form data programmatically
 * Useful for custom validation outside of React Hook Form
 */
export function validateMetricsForm(data: Partial<MetricsFormData>): {
  isValid: boolean;
  errors: Record<string, string>;
} {
  const errors: Record<string, string> = {};

  // Metric name validation
  if (!data.metric_name || !ValidationRules.required(data.metric_name)) {
    errors.metric_name = ValidationMessages.required("Metric name");
  } else if (!ValidationRules.minLength(data.metric_name, 2)) {
    errors.metric_name = ValidationMessages.minLength("Metric name", 2);
  }

  // Value validation
  if (
    data.value === undefined ||
    data.value === null ||
    !ValidationRules.positiveNumber(data.value)
  ) {
    errors.value = ValidationMessages.positiveNumber("Value");
  }

  // Unit validation
  if (!data.unit || !ValidationRules.required(data.unit)) {
    errors.unit = ValidationMessages.required("Unit");
  }

  // Metric date validation
  if (!data.metric_date) {
    errors.metric_date = ValidationMessages.required("Metric date");
  } else if (!ValidationRules.notFutureDate(data.metric_date)) {
    errors.metric_date = ValidationMessages.futureDate;
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  };
}

/**
 * Format validation errors for display
 */
export function formatValidationErrors(
  errors: Record<string, string>
): string[] {
  return Object.values(errors);
}

/**
 * Get first validation error message
 */
export function getFirstValidationError(
  errors: Record<string, string>
): string | null {
  const errorKeys = Object.keys(errors);
  return errorKeys.length > 0 ? errors[errorKeys[0]] : null;
}
