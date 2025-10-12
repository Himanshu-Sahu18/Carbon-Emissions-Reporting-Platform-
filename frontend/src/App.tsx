import "./App.css";
import { DashboardLayout } from "./components";
import { ErrorBoundary } from "./components/common";

function App() {
  return (
    <ErrorBoundary>
      <DashboardLayout />
    </ErrorBoundary>
  );
}

export default App;
