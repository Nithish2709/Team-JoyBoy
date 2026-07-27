import { useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import MainLayout from './layouts/MainLayout';
import { useThemeStore } from './store/useThemeStore';

// Pages
import DashboardPage from './pages/DashboardPage';
import StateOverviewPage from './pages/StateOverviewPage';
import DistrictMonitoringPage from './pages/DistrictMonitoringPage';
import FPSMonitoringPage from './pages/FPSMonitoringPage';
import ComplaintAnalyticsPage from './pages/ComplaintAnalyticsPage';
import PredictionDashboardPage from './pages/PredictionDashboardPage';
import InvestigationCenterPage from './pages/InvestigationCenterPage';
import InspectionQueuePage from './pages/InspectionQueuePage';
import ReportsPage from './pages/ReportsPage';
import SettingsPage from './pages/SettingsPage';
import AuthPage from './pages/AuthPage';
import NotFoundPage from './pages/NotFoundPage';

const queryClient = new QueryClient();

function App() {
  const isDarkMode = useThemeStore((state) => state.isDarkMode);

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<AuthPage />} />
          
          <Route path="/" element={<MainLayout />}>
            <Route index element={<DashboardPage />} />
            <Route path="state" element={<StateOverviewPage />} />
            <Route path="districts" element={<DistrictMonitoringPage />} />
            <Route path="districts/:id" element={<DistrictMonitoringPage />} />
            <Route path="shops" element={<FPSMonitoringPage />} />
            <Route path="shops/:id" element={<FPSMonitoringPage />} />
            <Route path="complaints" element={<ComplaintAnalyticsPage />} />
            <Route path="predictions" element={<PredictionDashboardPage />} />
            <Route path="investigations" element={<InvestigationCenterPage />} />
            <Route path="inspections" element={<InspectionQueuePage />} />
            <Route path="reports" element={<ReportsPage />} />
            <Route path="settings" element={<SettingsPage />} />
          </Route>

          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
