import os

frontend_dir = r"c:\Users\Dell\OneDrive\Desktop\PANCHAYATGUARD\panchayatguard\frontend\src"

# 1. Update App.tsx
app_tsx_path = os.path.join(frontend_dir, "App.tsx")
with open(app_tsx_path, "r", encoding="utf-8") as f:
    app_tsx = f.read()

if "import Vendors" not in app_tsx:
    app_tsx = app_tsx.replace(
        "import Procurement from './pages/Procurement';",
        "import Procurement from './pages/Procurement';\nimport Vendors from './pages/Vendors';\nimport VendorDetails from './pages/VendorDetails';\nimport RiskAnalysis from './pages/RiskAnalysis';"
    )
    app_tsx = app_tsx.replace(
        "<Route path=\"/vendors\" element={<Placeholder />} />",
        "<Route path=\"/vendors\" element={<Vendors />} />\n              <Route path=\"/vendors/:id\" element={<VendorDetails />} />"
    )
    app_tsx = app_tsx.replace(
        "<Route path=\"/risk-analysis\" element={<Placeholder />} />",
        "<Route path=\"/risk-analysis\" element={<RiskAnalysis />} />"
    )
    with open(app_tsx_path, "w", encoding="utf-8") as f:
        f.write(app_tsx)

# 2. Vendors.tsx
vendors_tsx_path = os.path.join(frontend_dir, "pages", "Vendors.tsx")
with open(vendors_tsx_path, "w", encoding="utf-8") as f:
    f.write("""import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { Search, Filter, Plus, Eye, Edit, Trash2, ChevronLeft, ChevronRight, CheckCircle, XCircle } from 'lucide-react';

export default function Vendors() {
  const navigate = useNavigate();
  const [vendors, setVendors] = useState<any[]>([]);
  const [totalItems, setTotalItems] = useState(0);
  const [page, setPage] = useState(1);
  const pageSize = 10;
  
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchVendors = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams({ page: page.toString(), page_size: pageSize.toString() });
      if (search) params.append('search', search);
      if (category) params.append('category', category);
      if (status) params.append('status', status);
      
      const res = await api.get(`/vendors?${params.toString()}`);
      setVendors(res.data.data);
      setTotalItems(res.data.total);
    } catch (e) { console.error(e); } finally { setLoading(false); }
  };

  useEffect(() => {
    const delay = setTimeout(() => { fetchVendors(); }, 300);
    return () => clearTimeout(delay);
  }, [page, search, category, status]);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
           <div className="text-sm text-gray-500 mb-1">Dashboard > Vendors</div>
           <h1 className="text-2xl font-bold text-gray-900">Vendor Management</h1>
           <p className="text-sm text-gray-500">Manage registered vendors, monitor performance, and assess risk.</p>
        </div>
      </div>

      {/* Filters Area */}
      <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm space-y-4">
         <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="relative w-full md:w-96">
               <Search className="absolute left-3 top-1.5 h-4 w-4 text-gray-400" />
               <input 
                 type="text" 
                 placeholder="Search by name, reg number..." 
                 className="w-full pl-9 pr-3 py-1.5 text-sm border border-gray-300 rounded focus:ring-1 focus:ring-pg-blue outline-none"
                 value={search}
                 onChange={(e) => setSearch(e.target.value)}
               />
            </div>
            <div className="flex items-center gap-3 w-full md:w-auto">
               <select className="text-sm border border-gray-300 rounded p-1.5 focus:ring-1 focus:ring-pg-blue" value={status} onChange={e=>setStatus(e.target.value)}>
                 <option value="">All Statuses</option>
                 <option value="Active">Active</option>
                 <option value="Inactive">Inactive</option>
                 <option value="Blacklisted">Blacklisted</option>
               </select>
               <button className="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-white bg-pg-blue rounded hover:bg-blue-700 shadow-sm">
                  <Plus className="w-4 h-4" /> Add Vendor
               </button>
            </div>
         </div>
      </div>

      {/* Table Area */}
      <div className="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden flex flex-col">
         <div className="overflow-x-auto">
            <table className="w-full text-sm text-left text-gray-600">
               <thead className="text-xs text-gray-700 uppercase bg-gray-50 border-b border-gray-200">
                  <tr>
                     <th className="px-4 py-3 font-semibold">Vendor Name</th>
                     <th className="px-4 py-3 font-semibold">Reg. No</th>
                     <th className="px-4 py-3 font-semibold">Category</th>
                     <th className="px-4 py-3 font-semibold">Total Procurement</th>
                     <th className="px-4 py-3 font-semibold">Risk Score</th>
                     <th className="px-4 py-3 font-semibold">Status</th>
                     <th className="px-4 py-3 font-semibold text-center">Actions</th>
                  </tr>
               </thead>
               <tbody>
                  {loading ? (
                     <tr><td colSpan={7} className="px-4 py-8 text-center text-gray-500">Loading...</td></tr>
                  ) : vendors.map(v => (
                     <tr key={v.id} className="border-b border-gray-50 hover:bg-gray-50 transition-colors">
                        <td className="px-4 py-3 font-bold text-pg-blue cursor-pointer" onClick={() => navigate(`/vendors/${v.id}`)}>{v.vendor_name}</td>
                        <td className="px-4 py-3">{v.registration_number}</td>
                        <td className="px-4 py-3">{v.category}</td>
                        <td className="px-4 py-3 text-gray-900 font-medium">₹ {(v.total_procurement_value || 0).toLocaleString()}</td>
                        <td className="px-4 py-3">
                           <span className={`font-bold ${v.risk_score >= 80 ? 'text-red-600' : v.risk_score >= 60 ? 'text-orange-500' : 'text-green-600'}`}>{v.risk_score || 0}</span>
                        </td>
                        <td className="px-4 py-3">
                           <span className={`px-2 py-1 flex w-fit items-center gap-1 rounded text-xs font-semibold ${v.status === 'Active' ? 'bg-green-100 text-green-700' : v.status === 'Blacklisted' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-700'}`}>
                             {v.status === 'Active' ? <CheckCircle className="w-3 h-3"/> : <XCircle className="w-3 h-3"/>}
                             {v.status}
                           </span>
                        </td>
                        <td className="px-4 py-3 flex items-center justify-center gap-2">
                           <button onClick={() => navigate(`/vendors/${v.id}`)} className="p-1 text-pg-blue hover:bg-blue-50 rounded"><Eye className="w-4 h-4"/></button>
                           <button className="p-1 text-pg-blue hover:bg-blue-50 rounded"><Edit className="w-4 h-4"/></button>
                        </td>
                     </tr>
                  ))}
               </tbody>
            </table>
         </div>
         
         <div className="p-4 border-t border-gray-200 flex items-center justify-between text-sm text-gray-500">
            <div>Showing {(page-1)*pageSize + 1}-{Math.min(page*pageSize, totalItems)} of {totalItems.toLocaleString()} vendors</div>
            <div className="flex items-center gap-2">
               <button disabled={page === 1} onClick={() => setPage(p => p-1)} className="p-1 border border-gray-200 rounded disabled:opacity-50"><ChevronLeft className="w-4 h-4"/></button>
               <span className="px-2 font-medium text-gray-900">{page}</span>
               <button disabled={page * pageSize >= totalItems} onClick={() => setPage(p => p+1)} className="p-1 border border-gray-200 rounded disabled:opacity-50"><ChevronRight className="w-4 h-4"/></button>
            </div>
         </div>
      </div>
    </div>
  );
}
""")

# 3. VendorDetails.tsx
vendordetails_tsx_path = os.path.join(frontend_dir, "pages", "VendorDetails.tsx")
with open(vendordetails_tsx_path, "w", encoding="utf-8") as f:
    f.write("""import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import { ArrowLeft, Edit, Ban, FileText, IndianRupee, ShieldAlert, PieChart, Map, AlertTriangle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart as RechartsPieChart, Pie, Cell } from 'recharts';

export default function VendorDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchVendor = async () => {
      try {
        const res = await api.get(`/vendors/${id}`);
        setData(res.data);
      } catch (e) { console.error(e); } finally { setLoading(false); }
    };
    fetchVendor();
  }, [id]);

  if (loading) return <div className="p-8">Loading vendor details...</div>;
  if (!data) return <div className="p-8 text-red-500">Vendor not found</div>;

  const COLORS = ['#0f172a', '#1e40af', '#3b82f6', '#60a5fa', '#93c5fd', '#cbd5e1'];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-3 mb-2 text-sm text-gray-500">
         <span className="cursor-pointer hover:underline" onClick={() => navigate('/vendors')}>Vendors</span> &gt; <span>Vendor Details</span>
      </div>
      
      <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
         <div className="flex items-start gap-4">
            <button onClick={() => navigate('/vendors')} className="p-2 border border-gray-200 rounded-lg hover:bg-gray-50"><ArrowLeft className="w-5 h-5"/></button>
            <div>
               <div className="flex items-center gap-3">
                  <h1 className="text-3xl font-extrabold text-gray-900">{data.vendor_name}</h1>
                  <span className={`px-2 py-0.5 rounded text-xs font-semibold ${data.status === 'Active' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>{data.status}</span>
               </div>
               <p className="text-gray-500 font-medium text-sm mt-1">Reg. No: {data.registration_number} | {data.category} | {data.district}, {data.state}</p>
            </div>
         </div>
         <div className="flex items-center gap-3">
            <button className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-50 shadow-sm">
               <Edit className="w-4 h-4"/> Edit Vendor
            </button>
            <button className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-red-600 bg-white border border-red-200 rounded hover:bg-red-50 shadow-sm">
               <Ban className="w-4 h-4"/> Deactivate
            </button>
         </div>
      </div>

      {/* KPI Stats */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
         <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex flex-col">
            <div className="text-gray-500 text-xs font-semibold mb-1 flex items-center gap-2"><IndianRupee className="w-4 h-4"/> Total Procurement</div>
            <div className="text-2xl font-bold text-gray-900">₹ {(data.total_procurement_value / 10000000).toFixed(2)} Cr</div>
         </div>
         <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex flex-col">
            <div className="text-gray-500 text-xs font-semibold mb-1 flex items-center gap-2"><FileText className="w-4 h-4"/> Total Transactions</div>
            <div className="text-2xl font-bold text-gray-900">{data.transaction_count}</div>
         </div>
         <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex flex-col">
            <div className="text-gray-500 text-xs font-semibold mb-1 flex items-center gap-2"><BarChart className="w-4 h-4"/> Average Transaction</div>
            <div className="text-2xl font-bold text-gray-900">₹ {(data.avg_transaction / 100000).toFixed(2)} Lakh</div>
         </div>
         <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex flex-col relative overflow-hidden">
            <div className={`absolute right-0 top-0 bottom-0 w-1 ${data.risk_score >= 80 ? 'bg-red-500' : data.risk_score >= 40 ? 'bg-orange-500' : 'bg-green-500'}`}></div>
            <div className="text-gray-500 text-xs font-semibold mb-1 flex items-center gap-2"><ShieldAlert className="w-4 h-4"/> Risk Score</div>
            <div className="flex items-end gap-2">
               <span className={`text-2xl font-bold ${data.risk_score >= 80 ? 'text-red-600' : data.risk_score >= 40 ? 'text-orange-500' : 'text-green-600'}`}>{data.risk_score} <span className="text-sm font-normal text-gray-400">/ 100</span></span>
            </div>
            <div className={`text-xs font-semibold mt-1 ${data.risk_score >= 80 ? 'text-red-500' : data.risk_score >= 40 ? 'text-orange-500' : 'text-green-500'}`}>{data.risk_score >= 80 ? 'High Risk' : data.risk_score >= 40 ? 'Medium Risk' : 'Low Risk'}</div>
         </div>
         <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex flex-col">
            <div className="text-gray-500 text-xs font-semibold mb-1 flex items-center gap-2"><PieChart className="w-4 h-4"/> Procurement Share</div>
            <div className="text-2xl font-bold text-gray-900">{data.procurement_share}%</div>
            <div className="text-xs text-gray-500 mt-1">of total procurement</div>
         </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
         {/* Vendor Info & Activity */}
         <div className="space-y-6">
            <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
               <div className="bg-gray-50 px-5 py-3 border-b font-bold text-gray-800">Vendor Information</div>
               <div className="p-5 space-y-3 text-sm">
                  <div className="grid grid-cols-3"><span className="text-gray-500 font-medium">Vendor Name</span><span className="col-span-2 font-medium text-gray-900">{data.vendor_name}</span></div>
                  <div className="grid grid-cols-3"><span className="text-gray-500 font-medium">Reg. Number</span><span className="col-span-2 text-gray-900">{data.registration_number}</span></div>
                  <div className="grid grid-cols-3"><span className="text-gray-500 font-medium">Category</span><span className="col-span-2 text-gray-900">{data.category}</span></div>
                  <div className="grid grid-cols-3"><span className="text-gray-500 font-medium">Address</span><span className="col-span-2 text-gray-900">{data.address}, {data.district}, {data.state}</span></div>
                  <div className="grid grid-cols-3"><span className="text-gray-500 font-medium">Email</span><span className="col-span-2 text-pg-blue">{data.contact_email}</span></div>
                  <div className="grid grid-cols-3"><span className="text-gray-500 font-medium">Phone</span><span className="col-span-2 text-gray-900">{data.contact_phone}</span></div>
               </div>
            </div>

            <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
               <div className="bg-gray-50 px-5 py-3 border-b font-bold text-gray-800 flex justify-between">Panchayats Served <span className="text-xs text-pg-blue font-semibold cursor-pointer">View All</span></div>
               <div className="p-5 flex items-center justify-around">
                  <div className="text-center">
                     <div className="text-3xl font-extrabold text-pg-navy">{data.panchayats_served}</div>
                     <div className="text-xs text-gray-500 font-medium mt-1 uppercase">Panchayats</div>
                  </div>
                  <div className="text-center">
                     <div className="text-3xl font-extrabold text-pg-navy">{data.districts_served}</div>
                     <div className="text-xs text-gray-500 font-medium mt-1 uppercase">Districts</div>
                  </div>
               </div>
            </div>
         </div>

         {/* Charts */}
         <div className="col-span-2 space-y-6">
            <div className="grid grid-cols-2 gap-6">
               <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-5">
                  <h3 className="font-bold text-gray-800 mb-4">Monthly Procurement Value</h3>
                  <div className="h-64">
                     <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={data.monthly_chart} margin={{top: 10, right: 10, left: -20, bottom: 0}}>
                           <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
                           <XAxis dataKey="month" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#6b7280'}} />
                           <YAxis axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#6b7280'}} tickFormatter={(v) => `${(v/100000).toFixed(0)}L`} />
                           <Tooltip cursor={{fill: '#f3f4f6'}} contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}} formatter={(val: number) => [`₹ ${(val/100000).toFixed(1)}L`, 'Amount']} />
                           <Bar dataKey="value" fill="#60a5fa" radius={[4, 4, 0, 0]} />
                        </BarChart>
                     </ResponsiveContainer>
                  </div>
               </div>
               <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-5">
                  <h3 className="font-bold text-gray-800 mb-4">Transactions by Category</h3>
                  <div className="h-64 flex flex-col items-center">
                     <ResponsiveContainer width="100%" height="100%">
                        <RechartsPieChart>
                           <Pie data={data.category_chart} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={2} dataKey="value">
                              {data.category_chart.map((_: any, i: number) => <Cell key={`cell-${i}`} fill={COLORS[i % COLORS.length]} />)}
                           </Pie>
                           <Tooltip formatter={(val: number) => `₹ ${(val/100000).toFixed(2)}L`} />
                        </RechartsPieChart>
                     </ResponsiveContainer>
                  </div>
               </div>
            </div>

            {/* Risk & Recent Tx */}
            <div className="grid grid-cols-2 gap-6">
               <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
                  <div className="bg-gray-50 px-5 py-3 border-b font-bold text-gray-800 flex justify-between">Risk Factors & Alerts <span className="text-xs text-pg-blue font-semibold cursor-pointer">View All</span></div>
                  <div className="p-4 space-y-3 max-h-64 overflow-y-auto">
                     {data.risk_alerts && data.risk_alerts.length > 0 ? data.risk_alerts.map((a: any, i: number) => (
                        <div key={i} className="flex items-start gap-3 p-3 rounded-lg border border-gray-100 bg-gray-50">
                           <AlertTriangle className={`w-5 h-5 shrink-0 ${a.severity==='Critical'||a.severity==='High'?'text-red-500':'text-orange-500'}`} />
                           <div>
                              <div className="font-bold text-sm text-gray-900">{a.type.replace('_', ' ')}</div>
                              <div className="text-xs text-gray-600 mt-0.5">{a.explanation}</div>
                           </div>
                           <div className={`ml-auto text-xs font-bold px-2 py-0.5 rounded ${a.severity==='Critical'||a.severity==='High'?'text-red-600 bg-red-100':'text-orange-600 bg-orange-100'}`}>{a.severity}</div>
                        </div>
                     )) : (
                        <div className="text-sm text-green-600 p-4 text-center">No risk alerts found for this vendor.</div>
                     )}
                  </div>
               </div>

               <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
                  <div className="bg-gray-50 px-5 py-3 border-b font-bold text-gray-800 flex justify-between">Recent Transactions <span className="text-xs text-pg-blue font-semibold cursor-pointer">View All</span></div>
                  <div className="overflow-x-auto">
                     <table className="w-full text-xs text-left">
                        <thead className="bg-gray-50 text-gray-500 uppercase border-b">
                           <tr>
                              <th className="px-4 py-2 font-semibold">ID</th>
                              <th className="px-4 py-2 font-semibold">Date</th>
                              <th className="px-4 py-2 font-semibold">Amount</th>
                              <th className="px-4 py-2 font-semibold">Risk</th>
                           </tr>
                        </thead>
                        <tbody>
                           {data.recent_transactions && data.recent_transactions.map((tx: any, i: number) => (
                              <tr key={i} className="border-b hover:bg-gray-50">
                                 <td className="px-4 py-2 font-medium text-pg-blue">{tx.transaction_id}</td>
                                 <td className="px-4 py-2 text-gray-600">{new Date(tx.date).toLocaleDateString('en-GB', {day:'2-digit',month:'short'})}</td>
                                 <td className="px-4 py-2 font-medium">₹ {(tx.amount/100000).toFixed(2)}L</td>
                                 <td className="px-4 py-2 font-bold"><span className={tx.risk_score >= 80 ? 'text-red-600' : tx.risk_score >= 40 ? 'text-orange-500' : 'text-green-600'}>{tx.risk_score}</span></td>
                              </tr>
                           ))}
                        </tbody>
                     </table>
                  </div>
               </div>
            </div>
         </div>
      </div>
    </div>
  );
}
""")

# 4. RiskAnalysis.tsx
riskanalysis_tsx_path = os.path.join(frontend_dir, "pages", "RiskAnalysis.tsx")
with open(riskanalysis_tsx_path, "w", encoding="utf-8") as f:
    f.write("""import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { ShieldAlert, AlertTriangle, Activity, Target } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

export default function RiskAnalysis() {
  const [data, setData] = useState<any>(null);
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await api.get('/risk/summary');
        setData(res.data);
      } catch (e) { console.error(e); }
    };
    fetchData();
  }, []);

  if (!data) return <div className="p-8">Loading risk analysis...</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
           <div className="text-sm text-gray-500 mb-1">Dashboard > Risk Analysis</div>
           <h1 className="text-2xl font-bold text-gray-900">Procurement Risk Analysis</h1>
           <p className="text-sm text-gray-500">Monitor and mitigate systemic anomalies using deterministic risk engines.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
         <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm flex items-center gap-4">
            <div className="p-4 bg-red-50 rounded-full text-red-500"><ShieldAlert className="w-8 h-8"/></div>
            <div>
               <div className="text-sm text-gray-500 font-medium">System Risk Score</div>
               <div className="text-3xl font-extrabold text-gray-900">{data.overall_score} <span className="text-sm font-normal text-gray-400">/ 100</span></div>
            </div>
         </div>
         <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm flex items-center justify-between col-span-3">
            <div className="flex items-center gap-6 w-full">
               <div className="flex-1">
                  <div className="text-sm font-medium text-gray-500 mb-2">High/Critical Alerts</div>
                  <div className="text-2xl font-bold text-red-600">{data.distribution?.critical_high || 0}</div>
               </div>
               <div className="w-px h-12 bg-gray-200"></div>
               <div className="flex-1">
                  <div className="text-sm font-medium text-gray-500 mb-2">Medium Risk Alerts</div>
                  <div className="text-2xl font-bold text-orange-500">{data.distribution?.medium || 0}</div>
               </div>
               <div className="w-px h-12 bg-gray-200"></div>
               <div className="flex-1">
                  <div className="text-sm font-medium text-gray-500 mb-2">Safe Transactions</div>
                  <div className="text-2xl font-bold text-green-600">{data.distribution?.low || 0}</div>
               </div>
            </div>
         </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
         <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-5">
            <h3 className="font-bold text-gray-800 mb-4 flex items-center gap-2"><Activity className="w-5 h-5 text-pg-blue"/> System Risk Trend</h3>
            <div className="h-72">
               <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={data.trend} margin={{top: 10, right: 10, left: -20, bottom: 0}}>
                     <defs>
                        <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                           <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                           <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                        </linearGradient>
                     </defs>
                     <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
                     <XAxis dataKey="month" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#6b7280'}} />
                     <YAxis axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#6b7280'}} />
                     <RechartsTooltip contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}} />
                     <Area type="monotone" dataKey="avg_score" stroke="#ef4444" strokeWidth={3} fillOpacity={1} fill="url(#colorScore)" />
                  </AreaChart>
               </ResponsiveContainer>
            </div>
         </div>

         <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-5">
            <h3 className="font-bold text-gray-800 mb-4 flex items-center gap-2"><Target className="w-5 h-5 text-pg-blue"/> Top Risky Vendors</h3>
            <div className="space-y-4">
               {data.by_vendor && data.by_vendor.map((v: any, i: number) => (
                  <div key={i} className="flex items-center justify-between p-3 rounded-lg border border-gray-100 hover:bg-gray-50">
                     <div>
                        <div className="font-bold text-gray-900">{v.name}</div>
                        <div className="text-xs text-gray-500">{v.alerts} Active Alerts</div>
                     </div>
                     <div className={`px-3 py-1 rounded text-sm font-bold ${v.score >= 80 ? 'bg-red-100 text-red-700' : 'bg-orange-100 text-orange-700'}`}>
                        Score: {v.score}
                     </div>
                  </div>
               ))}
            </div>
         </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
         <div className="bg-red-50 px-5 py-4 border-b border-red-100 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-red-600"/>
            <h3 className="font-bold text-red-900">Critical Alerts Feed</h3>
         </div>
         <div className="divide-y divide-gray-100">
            {data.critical_alerts && data.critical_alerts.length > 0 ? data.critical_alerts.map((a: any, i: number) => (
               <div key={i} className="p-4 hover:bg-gray-50 flex items-start gap-4">
                  <div className="w-12 h-12 bg-red-100 text-red-600 rounded-full flex items-center justify-center font-bold">{a.score}</div>
                  <div className="flex-1">
                     <div className="flex items-center justify-between">
                        <div className="font-bold text-gray-900 text-lg">{a.type.replace('_', ' ')}</div>
                        <div className="text-xs font-semibold text-gray-500">{new Date(a.date).toLocaleString()}</div>
                     </div>
                     <div className="text-sm text-gray-700 mt-1">{a.explanation}</div>
                     <div className="flex items-center gap-4 mt-2 text-xs font-medium text-gray-500">
                        <span>Vendor: <span className="text-pg-blue cursor-pointer">{a.vendor}</span></span>
                        <span>|</span>
                        <span>Transaction: <span className="text-pg-blue cursor-pointer">{a.transaction}</span></span>
                     </div>
                  </div>
               </div>
            )) : (
               <div className="p-8 text-center text-gray-500 font-medium">No critical alerts detected in the system.</div>
            )}
         </div>
      </div>
    </div>
  );
}
""")

print("Phase 4 Frontend components generated successfully!")
