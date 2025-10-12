import React from "react";
import Button from "../common/Button";

interface HeaderProps {
  onRefresh?: () => void;
  isRefreshing?: boolean;
}

const Header: React.FC<HeaderProps> = ({ onRefresh, isRefreshing = false }) => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-10">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-3 sm:py-4">
        <div className="flex items-center justify-between gap-2 sm:gap-4">
          {/* Logo and Title */}
          <div className="flex items-center space-x-2 sm:space-x-4 min-w-0 flex-1">
            <div className="flex items-center justify-center h-8 w-8 sm:h-10 sm:w-10 bg-primary-500 rounded-lg flex-shrink-0">
              <svg
                className="h-5 w-5 sm:h-6 sm:w-6 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <div className="min-w-0 flex-1">
              <h1 className="text-base sm:text-xl md:text-2xl font-bold text-gray-900 truncate">
                Carbon Emissions Dashboard
              </h1>
              <p className="text-xs sm:text-sm text-gray-600 hidden sm:block truncate">
                Track and analyze your organization's carbon footprint
              </p>
            </div>
          </div>

          {/* Refresh Button - Touch-friendly on mobile */}
          {onRefresh && (
            <Button
              variant="secondary"
              onClick={onRefresh}
              disabled={isRefreshing}
              className="flex items-center space-x-1 sm:space-x-2 flex-shrink-0 min-h-[44px] min-w-[44px] sm:min-w-0"
              aria-label="Refresh dashboard data"
            >
              <svg
                className={`h-5 w-5 ${isRefreshing ? "animate-spin" : ""}`}
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
              <span className="hidden sm:inline text-sm">
                {isRefreshing ? "Refreshing..." : "Refresh"}
              </span>
            </Button>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
