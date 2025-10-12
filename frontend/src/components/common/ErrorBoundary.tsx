import { Component } from "react";
import type { ErrorInfo, ReactNode } from "react";
import Button from "./Button";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

/**
 * ErrorBoundary Component
 * Catches JavaScript errors anywhere in the child component tree,
 * logs those errors, and displays a fallback UI
 */
class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    // Update state so the next render will show the fallback UI
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    // Log error details for debugging
    console.error("Error caught by ErrorBoundary:", error, errorInfo);

    // Update state with error info
    this.setState({
      error,
      errorInfo,
    });

    // You can also log the error to an error reporting service here
    // Example: logErrorToService(error, errorInfo);
  }

  handleReset = (): void => {
    // Reset the error boundary state
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
  };

  handleReload = (): void => {
    // Reload the page
    window.location.reload();
  };

  render(): ReactNode {
    if (this.state.hasError) {
      // Custom fallback UI provided by parent
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // Default fallback UI
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
          <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-6 sm:p-8">
            <div className="flex items-center justify-center w-12 h-12 mx-auto bg-red-100 rounded-full mb-4">
              <svg
                className="w-6 h-6 text-red-600"
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
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
            </div>

            <h2 className="text-2xl font-bold text-gray-900 text-center mb-2">
              Something went wrong
            </h2>

            <p className="text-gray-600 text-center mb-6">
              We're sorry, but something unexpected happened. Please try
              reloading the page or contact support if the problem persists.
            </p>

            {/* Error details (only in development) */}
            {import.meta.env.DEV && this.state.error && (
              <div className="mb-6 p-4 bg-gray-50 rounded-md border border-gray-200">
                <h3 className="text-sm font-semibold text-gray-700 mb-2">
                  Error Details (Development Only):
                </h3>
                <p className="text-xs text-red-600 font-mono break-words mb-2">
                  {this.state.error.toString()}
                </p>
                {this.state.errorInfo && (
                  <details className="text-xs text-gray-600">
                    <summary className="cursor-pointer font-medium mb-1">
                      Component Stack
                    </summary>
                    <pre className="whitespace-pre-wrap overflow-auto max-h-40 p-2 bg-white rounded border border-gray-200">
                      {this.state.errorInfo.componentStack}
                    </pre>
                  </details>
                )}
              </div>
            )}

            <div className="space-y-3">
              <Button
                variant="primary"
                fullWidth
                onClick={this.handleReload}
                aria-label="Reload page"
              >
                Reload Page
              </Button>

              <Button
                variant="secondary"
                fullWidth
                onClick={this.handleReset}
                aria-label="Try again without reloading"
              >
                Try Again
              </Button>
            </div>

            {/* Additional help text */}
            <p className="text-xs text-gray-500 text-center mt-6">
              If this issue continues, please contact support with the error
              details above.
            </p>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
