import React, { useState, useEffect } from 'react';
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
         {(activeTab === 'Profile' ) && (
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
         {(activeTab === 'Security' ) && (
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
                  {(activeTab === 'Notifications') && (
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
            </div>
         )}

         {(activeTab === 'Dashboard Preferences') && (
            <div className="space-y-6">
               <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Dashboard Preferences</h3>
                  <div className="space-y-4">
                     <div className="grid grid-cols-2 gap-4">
                        <div>
                           <label className="block text-xs font-medium text-gray-700 mb-1">Default District</label>
                           <select className="w-full p-2 border rounded text-sm focus:ring-1 focus:ring-pg-blue" value={prefs.district} onChange={e=>handlePrefChange('district', e.target.value)}>
                              <option>All Districts</option><option>Kanpur</option><option>Lucknow</option><option>Varanasi</option>
                           </select>
                        </div>
                        <div>
                           <label className="block text-xs font-medium text-gray-700 mb-1">Theme</label>
                           <select className="w-full p-2 border rounded text-sm focus:ring-1 focus:ring-pg-blue" value={prefs.theme} onChange={e=>{
                               handlePrefChange('theme', e.target.value);
                               if(e.target.value === 'Dark') {
                                   document.body.classList.add('dark-theme');
                               } else {
                                   document.body.classList.remove('dark-theme');
                               }
                               // Fire an event so AppLayout can listen
                               window.dispatchEvent(new Event('theme_changed'));
                           }}>
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
