import os

frontend_dir = r"c:\Users\Dell\OneDrive\Desktop\PANCHAYATGUARD\panchayatguard\frontend"
src_dir = os.path.join(frontend_dir, "src")
dirs = ["components", "layouts", "pages", "routes", "services", "hooks", "utils", "types", "assets"]
for d in dirs:
    os.makedirs(os.path.join(src_dir, d), exist_ok=True)

# 1. tailwind.config.js
with open(os.path.join(frontend_dir, "tailwind.config.js"), "w", encoding="utf-8") as f:
    f.write("""/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        pg: {
          navy: '#0A2540',
          blue: '#1E40AF',
          green: '#10B981',
          amber: '#F59E0B',
          red: '#EF4444',
          slate: '#475569',
          light: '#F8FAFC'
        }
      }
    },
  },
  plugins: [],
}
""")

# 2. src/index.css
with open(os.path.join(src_dir, "index.css"), "w", encoding="utf-8") as f:
    f.write("""@tailwind base;
@tailwind components;
@tailwind utilities;

html, body, #root {
    height: 100%;
    margin: 0;
    background-color: #F8FAFC;
    font-family: 'Inter', system-ui, sans-serif;
}
""")

# 3. src/services/api.ts
with open(os.path.join(src_dir, "services", "api.ts"), "w", encoding="utf-8") as f:
    f.write("""import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
""")

# 4. src/hooks/useAuth.tsx
with open(os.path.join(src_dir, "hooks", "useAuth.tsx"), "w", encoding="utf-8") as f:
    f.write("""import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}

interface AuthContextType {
  user: User | null;
  login: (token: string) => void;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export const AuthProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const res = await api.get('/auth/me');
          setUser(res.data);
        } catch (error) {
          localStorage.removeItem('token');
        }
      }
      setLoading(false);
    };
    fetchUser();
  }, []);

  const login = async (token: string) => {
    localStorage.setItem('token', token);
    const res = await api.get('/auth/me');
    setUser(res.data);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
""")

# 5. src/pages/Login.tsx
with open(os.path.join(src_dir, "pages", "Login.tsx"), "w", encoding="utf-8") as f:
    f.write("""import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useNavigate } from 'react-router-dom';
import { ShieldCheck, Eye, EyeOff } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import api from '../services/api';

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(1, 'Password is required'),
});

type LoginForm = z.infer<typeof loginSchema>;

export default function Login() {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema)
  });
  const [showPassword, setShowPassword] = useState(false);
  const [authError, setAuthError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const onSubmit = async (data: LoginForm) => {
    try {
      setAuthError('');
      const formData = new URLSearchParams();
      formData.append('username', data.email);
      formData.append('password', data.password);
      
      const response = await api.post('/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      
      await login(response.data.access_token);
      navigate('/');
    } catch (error: any) {
      setAuthError(error.response?.data?.detail || 'Authentication failed');
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Left Pane */}
      <div className="hidden lg:flex lg:w-1/2 bg-pg-navy text-white p-12 flex-col justify-between" style={{
        backgroundImage: "linear-gradient(rgba(10, 37, 64, 0.8), rgba(10, 37, 64, 0.95)), url('https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80')",
        backgroundSize: 'cover',
        backgroundPosition: 'center'
      }}>
        <div>
          <div className="flex items-center gap-3 mb-16">
            <div className="bg-white p-2 rounded-lg">
              <ShieldCheck className="w-8 h-8 text-pg-green" />
            </div>
            <div>
              <h1 className="text-2xl font-bold">PanchayatGuard</h1>
              <p className="text-sm text-gray-300">Transparent Panchayat. Stronger Bharat.</p>
            </div>
          </div>
          <h2 className="text-5xl font-light leading-tight mb-4">
            Empowering <br />
            <span className="font-bold">Transparent Governance</span><br />
            Across Rural India
          </h2>
          <div className="flex items-center gap-2 mb-12">
            <div className="h-1 w-12 bg-orange-500 rounded-full"></div>
            <div className="h-1 w-12 bg-white rounded-full"></div>
            <div className="h-1 w-12 bg-green-500 rounded-full"></div>
          </div>
          <p className="text-xl text-gray-300">Monitor. Detect. Prevent. Build Trust.</p>
        </div>
      </div>

      {/* Right Pane */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-pg-light">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8">
          <div className="mb-8">
            <p className="text-gray-500 mb-2">Welcome to</p>
            <h2 className="text-3xl font-bold text-pg-navy mb-2">PanchayatGuard</h2>
            <p className="text-sm text-gray-500">Sign in to access the procurement intelligence platform</p>
          </div>

          {authError && (
            <div className="bg-red-50 text-red-600 p-3 rounded-md mb-6 text-sm border border-red-200">
              {authError}
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
              <input 
                {...register('email')}
                type="email"
                placeholder="admin@panchayatguard.gov.in"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pg-blue focus:border-pg-blue outline-none"
              />
              {errors.email && <p className="text-red-500 text-xs mt-1">{errors.email.message}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
              <div className="relative">
                <input 
                  {...register('password')}
                  type={showPassword ? 'text' : 'password'}
                  placeholder="â€¢â€¢â€¢â€¢â€¢â€¢â€¢â€¢â€¢â€¢â€¢â€¢"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pg-blue focus:border-pg-blue outline-none"
                />
                <button 
                  type="button" 
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
              {errors.password && <p className="text-red-500 text-xs mt-1">{errors.password.message}</p>}
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" className="rounded text-pg-blue focus:ring-pg-blue" />
                <span className="text-sm text-gray-600">Remember me</span>
              </label>
              <a href="#" className="text-sm text-pg-blue hover:underline">Forgot password?</a>
            </div>

            <button 
              type="submit"
              className="w-full bg-pg-navy text-white py-3 rounded-lg font-medium hover:bg-opacity-90 transition-colors"
            >
              Sign In â†’
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
""")

# 6. src/layouts/AppLayout.tsx
with open(os.path.join(src_dir, "layouts", "AppLayout.tsx"), "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import { Outlet, Navigate, Link, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { 
  LayoutDashboard, 
  ShoppingCart, 
  Users, 
  AlertTriangle, 
  Receipt, 
  Map, 
  BarChart, 
  Brain, 
  MessageSquare, 
  ShieldAlert, 
  Settings,
  LogOut,
  ShieldCheck
} from 'lucide-react';

const MENU_ITEMS = [
  { name: 'Dashboard', path: '/', icon: LayoutDashboard },
  { name: 'Procurement', path: '/procurement', icon: ShoppingCart },
  { name: 'Vendors', path: '/vendors', icon: Users },
  { name: 'Risk Analysis', path: '/risk', icon: AlertTriangle },
  { name: 'Transactions', path: '/transactions', icon: Receipt },
  { name: 'Geographic View', path: '/geo', icon: Map },
  { name: 'Reports', path: '/reports', icon: BarChart },
  { name: 'AI Insights', path: '/ai', icon: Brain },
  { name: 'Grievances', path: '/grievances', icon: MessageSquare },
  { name: 'Audit Logs', path: '/audit', icon: ShieldAlert },
  { name: 'Settings', path: '/settings', icon: Settings },
];

export default function AppLayout() {
  const { user, logout } = useAuth();
  const location = useLocation();

  if (!user) {
    return <Navigate to="/login" />;
  }

  return (
    <div className="flex h-screen bg-pg-light">
      {/* Sidebar */}
      <div className="w-64 bg-pg-navy text-gray-300 flex flex-col">
        <div className="p-4 flex items-center gap-3 border-b border-gray-700">
          <div className="bg-white p-1 rounded">
            <ShieldCheck className="w-6 h-6 text-pg-green" />
          </div>
          <span className="text-white font-bold text-lg">PanchayatGuard</span>
        </div>
        
        <div className="flex-1 overflow-y-auto py-4">
          <nav className="space-y-1 px-2">
            {MENU_ITEMS.map((item) => {
              const active = location.pathname === item.path;
              return (
                <Link
                  key={item.name}
                  to={item.path}
                  className={`flex items-center gap-3 px-3 py-2 rounded-md transition-colors ${active ? 'bg-pg-blue text-white' : 'hover:bg-gray-800 hover:text-white'}`}
                >
                  <item.icon className="w-5 h-5" />
                  <span className="text-sm font-medium">{item.name}</span>
                </Link>
              );
            })}
          </nav>
        </div>

        <div className="p-4 border-t border-gray-700">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-8 h-8 rounded-full bg-pg-blue flex items-center justify-center text-white font-bold">
              {user.name.charAt(0)}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-white truncate">{user.name}</p>
              <p className="text-xs text-gray-400 truncate">{user.role}</p>
            </div>
          </div>
          <button 
            onClick={logout}
            className="flex items-center gap-2 text-sm text-gray-400 hover:text-white transition-colors w-full"
          >
            <LogOut className="w-4 h-4" />
            Sign out
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Navbar */}
        <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6">
          <h2 className="text-xl font-semibold text-gray-800 capitalize">
            {location.pathname === '/' ? 'Dashboard' : location.pathname.replace('/', '')}
          </h2>
          <div className="flex items-center gap-4">
             <span className="bg-green-100 text-green-800 text-xs font-semibold px-2.5 py-0.5 rounded border border-green-200">
               Role: {user.role}
             </span>
          </div>
        </header>

        {/* Content Area */}
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
""")

# 7. src/pages/Dashboard.tsx
with open(os.path.join(src_dir, "pages", "Dashboard.tsx"), "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import { useAuth } from '../hooks/useAuth';
import { Activity, Users, AlertOctagon, TrendingUp } from 'lucide-react';

export default function Dashboard() {
  const { user } = useAuth();

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h3 className="text-lg font-semibold text-gray-800 mb-2">Welcome back, {user?.name}</h3>
        <p className="text-gray-600">This is the Phase 1 Foundation of PanchayatGuard. Further modules are under development.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          { label: 'Total Procurements', value: 'â‚¹42.5 Cr', icon: TrendingUp, color: 'text-blue-600', bg: 'bg-blue-50' },
          { label: 'Active Panchayats', value: '1,248', icon: Activity, color: 'text-green-600', bg: 'bg-green-50' },
          { label: 'Registered Vendors', value: '3,892', icon: Users, color: 'text-purple-600', bg: 'bg-purple-50' },
          { label: 'High Risk Alerts', value: '14', icon: AlertOctagon, color: 'text-red-600', bg: 'bg-red-50' },
        ].map((stat, i) => (
          <div key={i} className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
            <div className={`p-3 rounded-lg ${stat.bg}`}>
              <stat.icon className={`w-6 h-6 ${stat.color}`} />
            </div>
            <div>
              <p className="text-sm text-gray-500 font-medium">{stat.label}</p>
              <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
""")

# 8. src/pages/Placeholder.tsx
with open(os.path.join(src_dir, "pages", "Placeholder.tsx"), "w", encoding="utf-8") as f:
    f.write("""import React from 'react';

export default function Placeholder() {
  return (
    <div className="flex items-center justify-center h-full">
      <div className="text-center">
        <div className="bg-gray-100 p-4 rounded-full inline-block mb-4">
          <svg className="w-12 h-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
          </svg>
        </div>
        <h3 className="text-xl font-medium text-gray-900 mb-1">Module Not Yet Enabled</h3>
        <p className="text-gray-500">This feature will be available in Phase 2.</p>
      </div>
    </div>
  );
}
""")

# 9. src/App.tsx
with open(os.path.join(src_dir, "App.tsx"), "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './hooks/useAuth';
import AppLayout from './layouts/AppLayout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Placeholder from './pages/Placeholder';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          
          <Route element={<AppLayout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/procurement" element={<Placeholder />} />
            <Route path="/vendors" element={<Placeholder />} />
            <Route path="/risk" element={<Placeholder />} />
            <Route path="/transactions" element={<Placeholder />} />
            <Route path="/geo" element={<Placeholder />} />
            <Route path="/reports" element={<Placeholder />} />
            <Route path="/ai" element={<Placeholder />} />
            <Route path="/grievances" element={<Placeholder />} />
            <Route path="/audit" element={<Placeholder />} />
            <Route path="/settings" element={<Placeholder />} />
          </Route>
          
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
""")

# 10. src/main.tsx
with open(os.path.join(src_dir, "main.tsx"), "w", encoding="utf-8") as f:
    f.write("""import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
""")

print("Frontend files generated successfully!")
