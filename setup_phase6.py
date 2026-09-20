import os

frontend_dir = r"c:\Users\Dell\OneDrive\Desktop\PANCHAYATGUARD\panchayatguard\frontend\src"

# 1. Update App.tsx
app_tsx_path = os.path.join(frontend_dir, "App.tsx")
with open(app_tsx_path, "r", encoding="utf-8") as f:
    app_tsx = f.read()

imports_to_add = """import AIInsights from './pages/AIInsights';
import Grievances from './pages/Grievances';
import AuditLogs from './pages/AuditLogs';"""

if "import AIInsights" not in app_tsx:
    app_tsx = app_tsx.replace(
        "import Reports from './pages/Reports';",
        "import Reports from './pages/Reports';\n" + imports_to_add
    )
    app_tsx = app_tsx.replace(
        "<Route path=\"/ai\" element={<Placeholder />} />",
        "<Route path=\"/ai\" element={<AIInsights />} />"
    )
    app_tsx = app_tsx.replace(
        "<Route path=\"/grievances\" element={<Placeholder />} />",
        "<Route path=\"/grievances\" element={<Grievances />} />"
    )
    app_tsx = app_tsx.replace(
        "<Route path=\"/audit\" element={<Placeholder />} />",
        "<Route path=\"/audit\" element={<AuditLogs />} />"
    )
    with open(app_tsx_path, "w", encoding="utf-8") as f:
        f.write(app_tsx)

# 2. AIInsights.tsx
ai_tsx_path = os.path.join(frontend_dir, "pages", "AIInsights.tsx")
with open(ai_tsx_path, "w", encoding="utf-8") as f:
    f.write("""import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Brain, Activity, Users, FileDuplicate, Share2, Target, AlertTriangle } from 'lucide-react';

export default function AIInsights() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await api.get('/ai-insights');
        setData(res.data);
      } catch (e) { console.error(e); } finally { setLoading(false); }
    };
    fetchData();
  }, []);

  if (!data) return <div className="p-8">Loading AI Insights...</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
           <div className="text-sm text-gray-500 mb-1">Dashboard > AI Insights</div>
           <h1 className="text-2xl font-bold text-gray-900">AI Insights</h1>
           <p className="text-sm text-gray-500">Data-driven intelligence to detect anomalies, uncover risks and promote transparent governance.</p>
        </div>
        <div className="text-right text-pg-blue italic text-sm font-medium">
           "From Data to Integrity<br/>Towards a Corruption-Free Tomorrow"
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
         <div className="bg-white p-4 rounded-xl border border-blue-200 shadow-sm">
            <div className="flex items-center gap-2 text-blue-600 mb-2"><Activity className="w-5 h-5 font-bold"/><span className="font-semibold text-sm">Price Anomalies</span></div>
            <div className="text-2xl font-bold text-gray-900">{data.categories['Price Anomalies']}</div>
         </div>
         <div className="bg-white p-4 rounded-xl border border-indigo-200 shadow-sm">
            <div className="flex items-center gap-2 text-indigo-600 mb-2"><Users className="w-5 h-5 font-bold"/><span className="font-semibold text-sm">Vendor Anomalies</span></div>
            <div className="text-2xl font-bold text-gray-900">{data.categories['Vendor Anomalies']}</div>
         </div>
         <div className="bg-white p-4 rounded-xl border border-red-200 shadow-sm">
            <div className="flex items-center gap-2 text-red-600 mb-2"><FileDuplicate className="w-5 h-5 font-bold"/><span className="font-semibold text-sm">Duplicate Tx</span></div>
            <div className="text-2xl font-bold text-gray-900">{data.categories['Duplicate Transactions']}</div>
         </div>
         <div className="bg-white p-4 rounded-xl border border-purple-200 shadow-sm">
            <div className="flex items-center gap-2 text-purple-600 mb-2"><Share2 className="w-5 h-5 font-bold"/><span className="font-semibold text-sm">Tx Splitting</span></div>
            <div className="text-2xl font-bold text-gray-900">{data.categories['Transaction Splitting']}</div>
         </div>
         <div className="bg-white p-4 rounded-xl border border-orange-200 shadow-sm">
            <div className="flex items-center gap-2 text-orange-600 mb-2"><Target className="w-5 h-5 font-bold"/><span className="font-semibold text-sm">Concentration Risk</span></div>
            <div className="text-2xl font-bold text-gray-900">{data.categories['Concentration Risks']}</div>
         </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
         <div className="p-5 border-b bg-gray-50 flex justify-between items-center">
            <h3 className="font-bold text-gray-800 flex items-center gap-2"><Brain className="w-5 h-5 text-pg-blue"/> Active AI Insights & Alerts</h3>
         </div>
         <div className="divide-y divide-gray-100">
            {data.insights.map((insight: any) => (
               <div key={insight.id} className="p-5 hover:bg-gray-50 flex gap-4 transition-colors items-center justify-between">
                  <div className="flex gap-4 w-1/3">
                      <div className={`p-3 rounded-xl h-fit ${insight.severity==='Critical'||insight.severity==='CRITICAL' ? 'bg-red-100 text-red-600' : insight.severity==='High'||insight.severity==='HIGH' ? 'bg-orange-100 text-orange-600' : 'bg-yellow-100 text-yellow-600'}`}>
                         <AlertTriangle className="w-6 h-6"/>
                      </div>
                      <div>
                         <h4 className="font-bold text-gray-900">{insight.title}</h4>
                         <p className="text-sm text-gray-600 mt-1">{insight.description}</p>
                         <div className="mt-2 flex gap-2">
                             <span className="text-xs font-semibold px-2 py-1 rounded bg-gray-100 text-gray-600">{insight.category}</span>
                             <span className={`text-xs font-semibold px-2 py-1 rounded ${insight.severity==='Critical'||insight.severity==='CRITICAL'?'bg-red-100 text-red-700':insight.severity==='High'||insight.severity==='HIGH'?'bg-orange-100 text-orange-700':'bg-yellow-100 text-yellow-700'}`}>{insight.severity}</span>
                         </div>
                      </div>
                  </div>
                  
                  <div className="w-1/3 text-sm text-gray-600 space-y-1 border-l pl-4">
                     <div><span className="font-medium text-gray-800">Transaction:</span> <span className="text-pg-blue cursor-pointer hover:underline">{insight.transaction_id}</span></div>
                     <div><span className="font-medium text-gray-800">Vendor:</span> {insight.vendor}</div>
                     <div><span className="font-medium text-gray-800">Panchayat:</span> {insight.panchayat}</div>
                  </div>

                  <div className="w-1/6 text-sm text-gray-500 font-medium">
                     {new Date(insight.date).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })}
                  </div>
                  
                  <div className="w-1/6 text-right">
                     <button className="px-4 py-2 border border-gray-300 rounded text-sm font-semibold text-pg-blue hover:bg-blue-50 transition-colors">View Details</button>
                  </div>
               </div>
            ))}
            {data.insights.length === 0 && <div className="p-8 text-center text-gray-500">No active insights.</div>}
         </div>
      </div>
    </div>
  );
}
""")

# 3. Grievances.tsx
grievances_tsx_path = os.path.join(frontend_dir, "pages", "Grievances.tsx")
with open(grievances_tsx_path, "w", encoding="utf-8") as f:
    f.write("""import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { MessageSquare, Plus, Search, Filter } from 'lucide-react';

export default function Grievances() {
  const [grievances, setGrievances] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('All');

  const fetchGrievances = async () => {
     setLoading(true);
     try {
       const params = new URLSearchParams();
       if (search) params.append('search', search);
       if (status) params.append('status', status);
       const res = await api.get(`/grievances?${params.toString()}`);
       setGrievances(res.data);
     } catch (e) { console.error(e); } finally { setLoading(false); }
  };

  useEffect(() => {
    fetchGrievances();
  }, [status]); // Trigger on status change, for search we can use form submit or debounce

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
           <div className="text-sm text-gray-500 mb-1">Dashboard > Grievances</div>
           <h1 className="text-2xl font-bold text-gray-900">Grievance Redressal</h1>
           <p className="text-sm text-gray-500">Manage and track public and internal grievances related to procurement.</p>
        </div>
        <button className="bg-pg-blue text-white px-4 py-2 rounded font-bold flex items-center gap-2 hover:bg-blue-700 transition-colors">
           <Plus className="w-4 h-4"/> New Grievance
        </button>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
         <div className="p-4 border-b flex justify-between items-center bg-gray-50">
            <div className="flex gap-4 w-1/2">
               <div className="relative flex-1">
                  <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"/>
                  <input type="text" placeholder="Search ID or subject..." className="w-full pl-9 pr-4 py-2 text-sm border rounded bg-white focus:ring-1 focus:ring-pg-blue" value={search} onChange={e=>setSearch(e.target.value)} onKeyDown={e=>e.key==='Enter' && fetchGrievances()}/>
               </div>
               <select className="border rounded text-sm px-3 py-2 bg-white" value={status} onChange={e=>setStatus(e.target.value)}>
                  <option>All</option>
                  <option>Open</option>
                  <option>Under Review</option>
                  <option>Resolved</option>
                  <option>Rejected</option>
               </select>
            </div>
         </div>
         <table className="w-full text-left text-sm">
            <thead className="bg-gray-50 text-gray-600 font-medium border-b">
               <tr>
                  <th className="px-6 py-3">ID</th>
                  <th className="px-6 py-3">Subject</th>
                  <th className="px-6 py-3">Panchayat</th>
                  <th className="px-6 py-3">Submitted By</th>
                  <th className="px-6 py-3">Date</th>
                  <th className="px-6 py-3">Priority</th>
                  <th className="px-6 py-3">Status</th>
                  <th className="px-6 py-3">Actions</th>
               </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
               {loading ? <tr><td colSpan={8} className="p-8 text-center text-gray-500">Loading...</td></tr> : 
                grievances.map(g => (
                  <tr key={g.id} className="hover:bg-gray-50">
                     <td className="px-6 py-4 font-bold text-pg-blue">{g.grievance_id}</td>
                     <td className="px-6 py-4 text-gray-900 font-medium max-w-xs truncate" title={g.description}>{g.subject}</td>
                     <td className="px-6 py-4 text-gray-600">{g.panchayat_name}</td>
                     <td className="px-6 py-4 text-gray-600">{g.submitted_by}</td>
                     <td className="px-6 py-4 text-gray-600">{new Date(g.date).toLocaleDateString()}</td>
                     <td className="px-6 py-4">
                        <span className={`px-2 py-1 rounded text-xs font-bold ${g.priority==='High'?'bg-red-100 text-red-700':g.priority==='Medium'?'bg-orange-100 text-orange-700':'bg-green-100 text-green-700'}`}>{g.priority}</span>
                     </td>
                     <td className="px-6 py-4">
                        <span className={`px-2 py-1 rounded-full border text-xs font-bold ${g.status==='Open'?'bg-red-50 text-red-600 border-red-200':g.status==='Under Review'?'bg-yellow-50 text-yellow-600 border-yellow-200':g.status==='Resolved'?'bg-green-50 text-green-600 border-green-200':'bg-gray-100 text-gray-600 border-gray-300'}`}>{g.status}</span>
                     </td>
                     <td className="px-6 py-4">
                        <button className="text-pg-blue font-semibold hover:underline">View</button>
                     </td>
                  </tr>
               ))}
            </tbody>
         </table>
      </div>
    </div>
  );
}
""")

# 4. AuditLogs.tsx
audit_tsx_path = os.path.join(frontend_dir, "pages", "AuditLogs.tsx")
with open(audit_tsx_path, "w", encoding="utf-8") as f:
    f.write("""import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { ShieldAlert } from 'lucide-react';

export default function AuditLogs() {
  const [logs, setLogs] = useState<any[]>([]);

  useEffect(() => {
    api.get('/audit-logs').then(res => setLogs(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
           <div className="text-sm text-gray-500 mb-1">Dashboard > Audit Logs</div>
           <h1 className="text-2xl font-bold text-gray-900">System Audit Logs</h1>
           <p className="text-sm text-gray-500">Immutable record of all system modifications and user activities.</p>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
         <div className="p-4 border-b bg-gray-50">
            <h3 className="font-bold text-gray-800 flex items-center gap-2"><ShieldAlert className="w-5 h-5 text-pg-navy"/> Recent Activity</h3>
         </div>
         <table className="w-full text-left text-sm">
            <thead className="bg-gray-50 text-gray-600 font-medium border-b">
               <tr>
                  <th className="px-6 py-3">Timestamp</th>
                  <th className="px-6 py-3">User</th>
                  <th className="px-6 py-3">Action</th>
                  <th className="px-6 py-3">Entity Type</th>
                  <th className="px-6 py-3">Entity ID</th>
                  <th className="px-6 py-3">Details</th>
               </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
               {logs.map(log => (
                  <tr key={log.id} className="hover:bg-gray-50">
                     <td className="px-6 py-3 text-gray-600">{new Date(log.timestamp).toLocaleString()}</td>
                     <td className="px-6 py-3 font-semibold text-gray-900">{log.user}</td>
                     <td className="px-6 py-3">
                        <span className={`px-2 py-1 rounded text-xs font-bold ${log.action==='CREATE'?'bg-green-100 text-green-700':log.action==='UPDATE'?'bg-blue-100 text-blue-700':log.action==='DELETE'?'bg-red-100 text-red-700':'bg-gray-100 text-gray-700'}`}>{log.action}</span>
                     </td>
                     <td className="px-6 py-3 text-gray-600">{log.entity_type}</td>
                     <td className="px-6 py-3 text-gray-600 font-mono text-xs">{log.entity_id}</td>
                     <td className="px-6 py-3 text-gray-600 max-w-sm truncate" title={log.details}>{log.details}</td>
                  </tr>
               ))}
            </tbody>
         </table>
      </div>
    </div>
  );
}
""")

# 5. Modify AppLayout.tsx to add notification fetching and dropdown
layout_tsx_path = os.path.join(frontend_dir, "layouts", "AppLayout.tsx")
with open(layout_tsx_path, "r", encoding="utf-8") as f:
    layout_tsx = f.read()

notif_logic = """
  const [notifs, setNotifs] = useState<any[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [showNotifs, setShowNotifs] = useState(false);

  useEffect(() => {
    if(user) {
       api.get('/notifications').then(res => {
         setNotifs(res.data.notifications);
         setUnreadCount(res.data.unread_count);
       });
    }
  }, [user]);

  const markAsRead = async (id: number) => {
     await api.put(`/notifications/${id}/read`);
     setNotifs(notifs.map(n => n.id === id ? {...n, is_read: true} : n));
     setUnreadCount(Math.max(0, unreadCount - 1));
  };
  
  const markAllRead = async () => {
     await api.put(`/notifications/read-all`);
     setNotifs(notifs.map(n => ({...n, is_read: true})));
     setUnreadCount(0);
  };
"""

if "setNotifs" not in layout_tsx:
    # insert state
    layout_tsx = layout_tsx.replace(
        "const [searchResults, setSearchResults] = useState<any[]>([]);",
        "const [searchResults, setSearchResults] = useState<any[]>([]);\n" + notif_logic
    )
    # update notification bell
    notif_ui = """
             <div className="relative cursor-pointer" onClick={() => setShowNotifs(!showNotifs)}>
               <Bell className="w-5 h-5 text-gray-600" />
               {unreadCount > 0 && <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full flex items-center justify-center text-[10px] text-white font-bold">{unreadCount}</span>}
               
               {showNotifs && (
                 <div className="absolute top-full right-0 mt-2 w-80 bg-white border border-gray-200 rounded-xl shadow-xl z-50 overflow-hidden cursor-default" onClick={e=>e.stopPropagation()}>
                    <div className="p-3 border-b flex justify-between items-center bg-gray-50">
                       <h3 className="font-bold text-gray-800">Notifications</h3>
                       <button onClick={markAllRead} className="text-xs text-pg-blue hover:underline">Mark all as read</button>
                    </div>
                    <div className="max-h-80 overflow-y-auto divide-y divide-gray-100">
                       {notifs.map(n => (
                          <div key={n.id} className={`p-4 flex gap-3 ${!n.is_read ? 'bg-blue-50/30' : ''}`}>
                             <div className={`p-2 rounded-full h-fit ${n.type==='alert' ? 'bg-red-100 text-red-500' : 'bg-blue-100 text-pg-blue'}`}>
                                <AlertTriangle className="w-4 h-4"/>
                             </div>
                             <div className="flex-1">
                                <h4 className="text-sm font-semibold text-gray-900">{n.title}</h4>
                                <p className="text-xs text-gray-600 mt-1">{n.message}</p>
                                <div className="text-[10px] text-gray-400 mt-2 flex justify-between">
                                   <span>{new Date(n.created_at).toLocaleString()}</span>
                                   {!n.is_read && <button onClick={()=>markAsRead(n.id)} className="text-pg-blue hover:underline font-semibold">Mark read</button>}
                                </div>
                             </div>
                          </div>
                       ))}
                       {notifs.length === 0 && <div className="p-6 text-center text-sm text-gray-500">No notifications</div>}
                    </div>
                 </div>
               )}
             </div>
"""
    # Replace old bell logic
    # Find <Bell ... /> block
    # Actually just replace the entire div containing bell
    start = layout_tsx.find('<div className="relative cursor-pointer">')
    end = layout_tsx.find('</div>', start) + 6
    if start != -1:
        layout_tsx = layout_tsx[:start] + notif_ui.strip() + layout_tsx[end:]
        with open(layout_tsx_path, "w", encoding="utf-8") as f:
            f.write(layout_tsx)

print("Phase 6 Frontend components generated successfully!")
