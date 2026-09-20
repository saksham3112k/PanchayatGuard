import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './hooks/useAuth';
import AppLayout from './layouts/AppLayout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Procurement from './pages/Procurement';
import Vendors from './pages/Vendors';
import VendorDetails from './pages/VendorDetails';
import RiskAnalysis from './pages/RiskAnalysis';
import GeographicView from './pages/GeographicView';
import Reports from './pages/Reports';
import AIInsights from './pages/AIInsights';
import Grievances from './pages/Grievances';
import AuditLogs from './pages/AuditLogs';
import Placeholder from './pages/Placeholder';
import Settings from './pages/Settings';
import NotFound from './pages/NotFound';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          
          <Route element={<AppLayout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/procurement" element={<Procurement />} />
            <Route path="/vendors" element={<Vendors />} />
              <Route path="/vendors/:id" element={<VendorDetails />} />
            <Route path="/risk-analysis" element={<RiskAnalysis />} />
            <Route path="/transactions" element={<Procurement />} />
            <Route path="/geo" element={<GeographicView />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/ai" element={<AIInsights />} />
            <Route path="/grievances" element={<Grievances />} />
            <Route path="/audit" element={<AuditLogs />} />
            <Route path="/settings" element={<Settings />} />
          </Route>
          
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
