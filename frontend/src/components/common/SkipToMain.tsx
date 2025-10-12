import React from "react";

/**
 * SkipToMain Component
 * Provides a skip link for keyboard users to jump directly to main content
 * This improves accessibility by allowing users to bypass repetitive navigation
 */
const SkipToMain: React.FC = () => {
  return (
    <a
      href="#main-content"
      className="skip-to-main"
      aria-label="Skip to main content"
    >
      Skip to main content
    </a>
  );
};

export default SkipToMain;
