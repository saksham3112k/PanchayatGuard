import os

base_dir = r"c:\Users\Dell\OneDrive\Desktop\PANCHAYATGUARD\panchayatguard"
frontend_dir = os.path.join(base_dir, "frontend", "src")

# 1. Update App.tsx (NotFound and Settings)
app_tsx_path = os.path.join(frontend_dir, "App.tsx")
with open(app_tsx_path, "r", encoding="utf-8") as f:
    app_tsx = f.read()

if "import Settings" not in app_tsx:
    app_tsx = app_tsx.replace(
        "import Placeholder from './pages/Placeholder';",
        "import Placeholder from './pages/Placeholder';\nimport Settings from './pages/Settings';\nimport NotFound from './pages/NotFound';"
    )
    app_tsx = app_tsx.replace(
        '<Route path="/settings" element={<Placeholder />} />',
        '<Route path="/settings" element={<Settings />} />'
    )
    # Add catch all * for NotFound (replacing the Navigate fallback if present)
    app_tsx = app_tsx.replace(
        '<Route path="*" element={<Navigate to="/" replace />} />',
        '<Route path="*" element={<NotFound />} />'
    )
    with open(app_tsx_path, "w", encoding="utf-8") as f:
        f.write(app_tsx)

# 2. Settings.tsx
settings_tsx_path = os.path.join(frontend_dir, "pages", "Settings.tsx")
with open(settings_tsx_path, "w", encoding="utf-8") as f:
    f.write("""import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from '../hooks/useAuth';
import { User, Shield, Bell, LayoutDashboard, Settings as SettingsIcon, Save, LogOut } from 'lucide-react';

export default function Settings() {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('Profile');
  
  // Profile state
  const [name, setName] = useState(user?.name || '');
  const [department, setDepartment] = useState(user?.department || 'Rural Development');
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState('');

  // Password state
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');

  // Preferences (LocalStorage)
  const [notifs, setNotifs] = useState({
     highRisk: localStorage.getItem('pg_notif_highRisk') !== 'false',
     newGrievances: localStorage.getItem('pg_notif_grievances') !== 'false',
     reportGen: localStorage.getItem('pg_notif_reports') !== 'false',
     sysUpdates: localStorage.getItem('pg_notif_sys') !== 'false',
     emailNotifs: localStorage.getItem('pg_notif_email') !== 'false',
     inApp: localStorage.getItem('pg_notif_inapp') !== 'false',
  });
  const [prefs, setPrefs] = useState({
     state: localStorage.getItem('pg_pref_state') || 'Uttar Pradesh',
     district: localStorage.getItem('pg_pref_district') || 'All Districts',
     dateRange: localStorage.getItem('pg_pref_date') || 'Last 6 Months',
     theme: localStorage.getItem('pg_pref_theme') || 'Light',
     showAi: localStorage.getItem('pg_pref_ai') !== 'false',
  });

  const handleProfileSave = async () => {
    setLoading(true); setMsg('');
    try {
       await api.put('/settings/profile', { name, department });
       setMsg('Profile updated successfully');
    } catch(e) { setMsg('Error updating profile'); }
    setLoading(false);
    setTimeout(()=>setMsg(''), 3000);
  };

  const handlePasswordSave = async () => {
    setLoading(true); setMsg('');
    try {
       await api.put('/settings/password', { current_password: currentPassword, new_password: newPassword });
       setMsg('Password updated successfully');
       setCurrentPassword(''); setNewPassword('');
    } catch(e) { setMsg('Error updating password'); }
    setLoading(false);
    setTimeout(()=>setMsg(''), 3000);
  };

  const handleNotifToggle = (key: keyof typeof notifs) => {
     const newVal = !notifs[key];
     setNotifs(p => ({...p, [key]: newVal}));
     localStorage.setItem(`pg_notif_${key}`, newVal.toString());
  };

  const handlePrefChange = (key: keyof typeof prefs, val: any) => {
     setPrefs(p => ({...p, [key]: val}));
     localStorage.setItem(`pg_pref_${key}`, val.toString());
  };

  return (
    <div className="space-y-6 pb-12">
      <div className="flex justify-between items-start">
        <div>
           <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
           <p className="text-sm text-gray-500">Manage your account, security, preferences and system configuration</p>
        </div>
      </div>

      <div className="border-b border-gray-200">
         <nav className="flex space-x-8">
            {['Profile', 'Security', 'Notifications', 'Dashboard Preferences'].map(tab => (
               <button key={tab} onClick={()=>setActiveTab(tab)} className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2 ${activeTab===tab ? 'border-pg-blue text-pg-blue':'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}>
                 {tab === 'Profile' && <User className="w-4 h-4"/>}
                 {tab === 'Security' && <Shield className="w-4 h-4"/>}
                 {tab === 'Notifications' && <Bell className="w-4 h-4"/>}
                 {tab === 'Dashboard Preferences' && <LayoutDashboard className="w-4 h-4"/>}
                 {tab}
               </button>
            ))}
         </nav>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
         {/* Profile */}
         {(activeTab === 'Profile' || window.innerWidth >= 1024) && (
            <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6 col-span-2 lg:col-span-1">
               <h3 className="text-lg font-bold text-gray-900 mb-4">Profile Information</h3>
               <div className="space-y-4">
                  <div className="flex items-center gap-4 mb-6">
                     <div className="w-16 h-16 bg-pg-navy text-white rounded-full flex items-center justify-center text-2xl font-bold">
                        {name.split(' ').map((n:any)=>n[0]).join('')}
                     </div>
                     <div>
                        <div className="font-bold text-gray-900 text-lg">{name}</div>
                        <div className="text-sm text-gray-500">{user?.role}</div>
                     </div>
                  </div>
                  <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                     <input type="text" className="w-full p-2 border rounded text-sm focus:ring-1 focus:ring-pg-blue" value={name} onChange={e=>setName(e.target.value)} />
                  </div>
                  <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">Email Address (Read Only)</label>
                     <input type="email" disabled className="w-full p-2 border rounded text-sm bg-gray-50 text-gray-500" value={user?.email} />
                  </div>
                  <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">Department</label>
                     <input type="text" className="w-full p-2 border rounded text-sm focus:ring-1 focus:ring-pg-blue" value={department} onChange={e=>setDepartment(e.target.value)} />
                  </div>
                  <button onClick={handleProfileSave} disabled={loading} className="w-full mt-4 bg-pg-blue text-white py-2 rounded font-bold hover:bg-blue-700 transition-colors flex justify-center items-center gap-2">
                     <Save className="w-4 h-4"/> {loading ? 'Saving...' : 'Save Changes'}
                  </button>
                  {msg && msg.includes('Profile') && <p className="text-sm text-green-600 mt-2 text-center font-medium">{msg}</p>}
               </div>
            </div>
         )}

         {/* Security */}
         {(activeTab === 'Security' || window.innerWidth >= 1024) && (
            <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
               <h3 className="text-lg font-bold text-gray-900 mb-4">Security</h3>
               <div className="space-y-6">
                  <div>
                     <h4 className="text-sm font-bold text-gray-800 mb-2">Change Password</h4>
                     <input type="password" placeholder="Current Password" value={currentPassword} onChange={e=>setCurrentPassword(e.target.value)} className="w-full p-2 mb-2 border rounded text-sm focus:ring-1 focus:ring-pg-blue" />
                     <input type="password" placeholder="New Password" value={newPassword} onChange={e=>setNewPassword(e.target.value)} className="w-full p-2 border rounded text-sm focus:ring-1 focus:ring-pg-blue" />
                     <button onClick={handlePasswordSave} disabled={loading || !currentPassword || !newPassword} className="mt-3 text-sm bg-gray-100 text-gray-700 py-1.5 px-4 rounded font-bold hover:bg-gray-200 w-full disabled:opacity-50">Update Password</button>
                     {msg && msg.includes('Password') && <p className="text-sm text-center mt-2 font-medium text-green-600">{msg}</p>}
                  </div>
                  <hr/>
                  <div className="flex justify-between items-center">
                     <div>
                        <h4 className="text-sm font-bold text-gray-800">Two-Factor Authentication</h4>
                        <p className="text-xs text-gray-500">Add an extra layer of security</p>
                     </div>
                     <span className="text-xs font-bold text-pg-green bg-green-50 px-2 py-1 rounded">Enabled</span>
                  </div>
                  <hr/>
                  <div className="flex justify-between items-center">
                     <div>
                        <h4 className="text-sm font-bold text-gray-800">Logout All Sessions</h4>
                        <p className="text-xs text-gray-500">Sign out from all devices</p>
                     </div>
                     <button onClick={logout} className="text-xs text-red-600 font-bold border border-red-200 bg-red-50 px-3 py-1.5 rounded hover:bg-red-100 flex items-center gap-1">
                        <LogOut className="w-3 h-3"/> Logout All
                     </button>
                  </div>
               </div>
            </div>
         )}

         {/* Notifications & Preferences */}
         {(activeTab === 'Notifications' || activeTab === 'Dashboard Preferences' || window.innerWidth >= 1024) && (
            <div className="space-y-6">
               <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Notification Preferences</h3>
                  <div className="space-y-4">
                     {[
                        { k: 'highRisk', title: 'High-risk alerts', desc: 'Get notified about critical risk alerts', c: 'text-red-500' },
                        { k: 'newGrievances', title: 'New grievances', desc: 'Get notified about new grievances', c: 'text-blue-500' },
                        { k: 'reportGen', title: 'Report generation', desc: 'Get notified when reports are ready', c: 'text-green-500' },
                        { k: 'emailNotifs', title: 'Email notifications', desc: 'Receive important notifications via email', c: 'text-gray-600' }
                     ].map(n => (
                        <div key={n.k} className="flex justify-between items-center">
                           <div>
                              <h4 className="text-sm font-bold text-gray-800">{n.title}</h4>
                              <p className="text-xs text-gray-500">{n.desc}</p>
                           </div>
                           <button onClick={()=>handleNotifToggle(n.k as keyof typeof notifs)} className={`w-10 h-5 rounded-full relative transition-colors ${notifs[n.k as keyof typeof notifs] ? 'bg-pg-blue':'bg-gray-300'}`}>
                              <div className={`w-4 h-4 bg-white rounded-full absolute top-0.5 transition-all ${notifs[n.k as keyof typeof notifs] ? 'left-5':'left-1'}`}/>
                           </button>
                        </div>
                     ))}
                  </div>
               </div>

               <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Dashboard Preferences</h3>
                  <div className="space-y-4">
                     <div className="grid grid-cols-2 gap-4">
                        <div>
                           <label className="block text-xs font-medium text-gray-700 mb-1">Default District</label>
                           <select className="w-full p-2 border rounded text-sm focus:ring-1 focus:ring-pg-blue" value={prefs.district} onChange={e=>handlePrefChange('district', e.target.value)}>
                              <option>All Districts</option><option>Kanpur</option><option>Lucknow</option>
                           </select>
                        </div>
                        <div>
                           <label className="block text-xs font-medium text-gray-700 mb-1">Theme</label>
                           <select className="w-full p-2 border rounded text-sm focus:ring-1 focus:ring-pg-blue" value={prefs.theme} onChange={e=>handlePrefChange('theme', e.target.value)}>
                              <option>Light</option><option>Dark</option><option>System</option>
                           </select>
                        </div>
                     </div>
                     <div className="flex items-center gap-2">
                        <input type="checkbox" id="ai-toggle" checked={prefs.showAi} onChange={e=>handlePrefChange('showAi', e.target.checked)} className="rounded text-pg-blue focus:ring-pg-blue" />
                        <label htmlFor="ai-toggle" className="text-sm text-gray-700 font-medium">Show AI insights on dashboard</label>
                     </div>
                  </div>
               </div>
            </div>
         )}
      </div>
    </div>
  );
}
""")

# 3. NotFound.tsx
notfound_tsx_path = os.path.join(frontend_dir, "pages", "NotFound.tsx")
with open(notfound_tsx_path, "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShieldCheck, ArrowLeft, Home } from 'lucide-react';

export default function NotFound() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 px-4">
       <div className="bg-pg-navy p-4 rounded-full mb-6">
          <ShieldCheck className="w-16 h-16 text-pg-green" />
       </div>
       <h1 className="text-6xl font-extrabold text-pg-navy mb-2">404</h1>
       <h2 className="text-2xl font-bold text-gray-900 mb-4">Page not found</h2>
       <p className="text-gray-600 mb-8 max-w-md text-center">
          The page you are looking for doesn't exist or has been moved. Please check the URL or navigate back to the dashboard.
       </p>
       <div className="flex gap-4 w-full max-w-xs">
          <button onClick={() => navigate(-1)} className="flex-1 flex justify-center items-center gap-2 py-2.5 px-4 border border-gray-300 rounded-lg text-sm font-semibold text-gray-700 hover:bg-gray-100 transition-colors">
             <ArrowLeft className="w-4 h-4" /> Go Back
          </button>
          <Link to="/" className="flex-1 flex justify-center items-center gap-2 py-2.5 px-4 bg-pg-blue rounded-lg text-sm font-bold text-white hover:bg-blue-700 shadow transition-colors">
             <Home className="w-4 h-4" /> Dashboard
          </Link>
       </div>
    </div>
  );
}
""")

# 4. AppLayout.tsx Responsive Updates
layout_tsx_path = os.path.join(frontend_dir, "layouts", "AppLayout.tsx")
with open(layout_tsx_path, "r", encoding="utf-8") as f:
    layout_tsx = f.read()

if "Menu" not in layout_tsx:
    # Add Menu icon to imports
    layout_tsx = layout_tsx.replace("Bell, ChevronDown", "Bell, ChevronDown, Menu, X")
    
    # Add mobile sidebar state
    layout_tsx = layout_tsx.replace("const [showNotifs, setShowNotifs] = useState(false);", "const [showNotifs, setShowNotifs] = useState(false);\n  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);")
    
    # Update Sidebar classes for responsiveness
    layout_tsx = layout_tsx.replace(
        '<div className="w-64 bg-pg-navy text-gray-300 flex flex-col h-full flex-shrink-0">',
        '<div className={`fixed inset-y-0 left-0 z-50 w-64 bg-pg-navy text-gray-300 flex flex-col h-full transform transition-transform duration-300 md:relative md:translate-x-0 ${mobileMenuOpen ? "translate-x-0" : "-translate-x-full"}`}>'
    )
    
    # Add hamburger button to header
    hamburger = """<button className="md:hidden p-2 -ml-2 text-gray-600 hover:bg-gray-100 rounded" onClick={() => setMobileMenuOpen(true)}>
             <Menu className="w-6 h-6" />
          </button>"""
    layout_tsx = layout_tsx.replace(
        '<div className="flex items-center w-1/2 max-w-lg relative">',
        f'<div className="flex items-center w-full md:w-1/2 max-w-lg relative gap-3">\n             {hamburger}'
    )
    
    # Add close button to sidebar for mobile
    close_btn = """<button className="md:hidden absolute top-4 right-4 text-gray-400 hover:text-white" onClick={() => setMobileMenuOpen(false)}>
            <X className="w-6 h-6" />
          </button>"""
    layout_tsx = layout_tsx.replace(
        '<div className="bg-white p-1 rounded">',
        f'{close_btn}\n          <div className="bg-white p-1 rounded">'
    )
    
    # Also add click handler to sidebar links to close menu on mobile
    layout_tsx = layout_tsx.replace(
        'className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors',
        'onClick={() => setMobileMenuOpen(false)}\n                  className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors'
    )

    with open(layout_tsx_path, "w", encoding="utf-8") as f:
        f.write(layout_tsx)

# 5. docker-compose.yml
docker_path = os.path.join(base_dir, "docker-compose.yml")
with open(docker_path, "w", encoding="utf-8") as f:
    f.write("""version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres}
      POSTGRES_DB: ${POSTGRES_DB:-panchayatguard}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER:-postgres}:${POSTGRES_PASSWORD:-postgres}@db:5432/${POSTGRES_DB:-panchayatguard}
      - SECRET_KEY=${SECRET_KEY:-your-super-secret-production-key}
      - ACCESS_TOKEN_EXPIRE_MINUTES=1440
    depends_on:
      db:
        condition: service_healthy
    command: uvicorn app.main:app --host 0.0.0.1 --port 8000

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
""")

# 6. .env.example
env_example = os.path.join(base_dir, ".env.example")
with open(env_example, "w", encoding="utf-8") as f:
    f.write("""# PanchayatGuard Production Environment Variables

# Backend
SECRET_KEY=generate_a_secure_random_string_here
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Database (PostgreSQL recommended for production)
# SQLite fallback: sqlite:///./panchayatguard.db
DATABASE_URL=postgresql://postgres:postgres@db:5432/panchayatguard
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=panchayatguard

# Frontend API URL
VITE_API_URL=http://localhost:8000/api
""")

print("Phase 7 files (Settings, 404, Responsive layout, Docker) generated successfully.")
