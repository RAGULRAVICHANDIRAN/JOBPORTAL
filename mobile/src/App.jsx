import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import useAuthStore from './store/authStore';

// Screens
import LoginScreen from './screens/auth/LoginScreen';
import RegisterScreen from './screens/auth/RegisterScreen';
import DashboardScreen from './screens/dashboard/DashboardScreen';
import JobsScreen from './screens/jobs/JobsScreen';
import ApplicationsScreen from './screens/applications/ApplicationsScreen';
import AutomationScreen from './screens/automation/AutomationScreen';
import ProfileScreen from './screens/profile/ProfileScreen';

// Components
import BottomNav from './components/BottomNav';

function ProtectedRoute({ children }) {
  const { isAuthenticated, isLoading } = useAuthStore();

  if (isLoading) {
    return (
      <div className="loading-screen">
        <div style={{
          fontSize: '2rem', fontWeight: 800,
          background: 'linear-gradient(135deg, var(--primary-400), var(--accent-400))',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
        }}>
          JobPilot AI
        </div>
        <div className="spinner" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

function AuthRoute({ children }) {
  const { isAuthenticated, isLoading } = useAuthStore();

  if (isLoading) return null;
  if (isAuthenticated) return <Navigate to="/" replace />;
  return children;
}

function AppLayout() {
  return (
    <div className="app-container">
      <Routes>
        <Route path="/" element={<DashboardScreen />} />
        <Route path="/jobs" element={<JobsScreen />} />
        <Route path="/applications" element={<ApplicationsScreen />} />
        <Route path="/automation" element={<AutomationScreen />} />
        <Route path="/profile" element={<ProfileScreen />} />
      </Routes>
      <BottomNav />
    </div>
  );
}

export default function App() {
  const { initialize } = useAuthStore();

  useEffect(() => {
    initialize();
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        {/* Auth routes — no bottom nav */}
        <Route path="/login" element={
          <AuthRoute><LoginScreen /></AuthRoute>
        } />
        <Route path="/register" element={
          <AuthRoute><RegisterScreen /></AuthRoute>
        } />

        {/* Protected app routes — with bottom nav */}
        <Route path="/*" element={
          <ProtectedRoute><AppLayout /></ProtectedRoute>
        } />
      </Routes>
    </BrowserRouter>
  );
}
