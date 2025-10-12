import React from "react";

interface CardProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  className?: string;
  headerAction?: React.ReactNode;
  padding?: "none" | "sm" | "md" | "lg";
}

const Card: React.FC<CardProps> = ({
  children,
  title,
  subtitle,
  className = "",
  headerAction,
  padding = "md",
}) => {
  const paddingClasses = {
    none: "",
    sm: "p-3 sm:p-4",
    md: "p-4 sm:p-6",
    lg: "p-6 sm:p-8",
  };

  return (
    <div
      className={`bg-white rounded-lg shadow-md border border-gray-200 ${className}`}
    >
      {(title || subtitle || headerAction) && (
        <div className={`border-b border-gray-200 ${paddingClasses[padding]}`}>
          <div className="flex items-start justify-between">
            <div className="min-w-0 flex-1">
              {title && (
                <h3 className="text-lg sm:text-xl font-semibold text-gray-800 truncate">
                  {title}
                </h3>
              )}
              {subtitle && (
                <p className="mt-1 text-xs sm:text-sm text-gray-500 truncate">
                  {subtitle}
                </p>
              )}
            </div>
            {headerAction && (
              <div className="ml-4 flex-shrink-0">{headerAction}</div>
            )}
          </div>
        </div>
      )}
      <div className={paddingClasses[padding]}>{children}</div>
    </div>
  );
};

export default Card;
