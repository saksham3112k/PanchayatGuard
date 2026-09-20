import os

frontend_dir = r"c:\Users\Dell\OneDrive\Desktop\PANCHAYATGUARD\panchayatguard\frontend\src"

# 1. AppLayout.tsx
with open(os.path.join(frontend_dir, "layouts", "AppLayout.tsx"), "w", encoding="utf-8") as f:
    f.write("""import React, { useState, useEffect } from 'react';
import { Outlet, Navigate, Link, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { 
  LayoutDashboard, ShoppingCart, Users, AlertTriangle, Receipt, Map, 
  BarChart, Brain, MessageSquare, ShieldAlert, Settings, LogOut, ShieldCheck,
  Search, MapPin, Bell, ChevronDown
} from 'lucide-react';
import api from '../services/api';

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
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);

  useEffect(() => {
    const delayDebounceFn = setTimeout(async () => {
      if (searchQuery.length >= 2) {
        try {
          const res = await api.get(`/dashboard/search?q=${searchQuery}`);
          setSearchResults(res.data);
        } catch (e) {
          console.error(e);
        }
      } else {
        setSearchResults([]);
      }
    }, 300);
    return () => clearTimeout(delayDebounceFn);
  }, [searchQuery]);

  if (!user) {
    return <Navigate to="/login" />;
  }

  return (
    <div className="flex h-screen bg-pg-light">
      {/* Sidebar */}
      <div className="w-64 bg-pg-navy text-gray-300 flex flex-col h-full flex-shrink-0">
        <div className="p-5 flex items-center gap-3">
          <div className="bg-white p-1 rounded">
            <ShieldCheck className="w-7 h-7 text-pg-green" />
          </div>
          <div>
            <span className="text-white font-bold text-lg block leading-tight">PanchayatGuard</span>
            <span className="text-[10px] text-gray-400 block leading-tight">Transparent Panchayat. Stronger Bharat.</span>
          </div>
        </div>
        
        <div className="flex-1 overflow-y-auto py-4">
          <nav className="space-y-1 px-3">
            {MENU_ITEMS.map((item) => {
              const active = location.pathname === item.path;
              return (
                <Link
                  key={item.name}
                  to={item.path}
                  className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${active ? 'bg-pg-blue text-white' : 'hover:bg-gray-800 hover:text-white'}`}
                >
                  <item.icon className={`w-5 h-5 ${active ? 'text-white' : 'text-gray-400'}`} />
                  <span className="text-sm font-medium">{item.name}</span>
                </Link>
              );
            })}
          </nav>
        </div>

        <div className="p-5">
           <div className="text-center">
              <div className="flex justify-center mb-2 opacity-50">
                {/* SVG for decorative graphic can go here */}
              </div>
              <p className="text-[10px] text-gray-500">Digital Governance<br/>for Stronger Communities</p>
           </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Top Navbar */}
        <header className="h-16 bg-white flex items-center justify-between px-6 flex-shrink-0 z-10 shadow-sm relative">
          <div className="flex items-center w-1/2 max-w-lg relative">
             <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
               <Search className="h-4 w-4 text-gray-400" />
             </div>
             <input 
               type="text"
               value={searchQuery}
               onChange={(e) => setSearchQuery(e.target.value)}
               placeholder="Search transactions, vendors, panchayats..."
               className="w-full pl-10 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-pg-blue focus:bg-white"
             />
             
             {/* Search Dropdown */}
             {searchResults.length > 0 && (
               <div className="absolute top-full mt-1 w-full bg-white border border-gray-200 rounded-lg shadow-lg z-50 py-2 max-h-64 overflow-y-auto">
                 {searchResults.map((res, i) => (
                   <div key={i} className="px-4 py-2 hover:bg-gray-50 cursor-pointer">
                     <span className="text-xs font-semibold text-pg-blue bg-blue-50 px-2 py-0.5 rounded mr-2">{res.type}</span>
                     <span className="text-sm text-gray-800">{res.title}</span>
                   </div>
                 ))}
               </div>
             )}
          </div>
          
          <div className="flex items-center gap-6">
             <div className="flex items-center gap-1 text-sm text-gray-600 bg-gray-50 px-3 py-1.5 rounded-full border border-gray-200 cursor-pointer">
               <MapPin className="w-4 h-4" />
               <span>Uttar Pradesh</span>
               <ChevronDown className="w-4 h-4 ml-1" />
             </div>
             
             <div className="relative cursor-pointer">
               <Bell className="w-5 h-5 text-gray-600" />
               <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full flex items-center justify-center text-[10px] text-white font-bold">5</span>
             </div>
             
             <div className="flex items-center gap-3 cursor-pointer" onClick={logout}>
               <div className="w-8 h-8 rounded-full bg-pg-navy flex items-center justify-center text-white font-bold text-sm">
                 {user.name.split(' ').map(n => n[0]).join('')}
               </div>
               <div className="hidden md:block">
                 <p className="text-sm font-semibold text-gray-800 leading-tight">{user.name}</p>
                 <p className="text-xs text-gray-500 leading-tight">{user.role}</p>
               </div>
             </div>
          </div>
        </header>

        {/* Content Area */}
        <main className="flex-1 overflow-y-auto bg-pg-light p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
""")

# 2. Dashboard.tsx
with open(os.path.join(frontend_dir, "pages", "Dashboard.tsx"), "w", encoding="utf-8") as f:
    f.write("""import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import api from '../services/api';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer,
  PieChart, Pie, Cell, BarChart as RechartsBarChart, Bar
} from 'recharts';
import { 
  TrendingUp, AlertTriangle, FileText, ChevronRight, Calendar, 
  MapPin, Zap, AlertCircle, Link as LinkIcon, PieChart as PieChartIcon, Lightbulb
} from 'lucide-react';

export default function Dashboard() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  const [summary, setSummary] = useState<any>(null);
  const [riskTrend, setRiskTrend] = useState<any[]>([]);
  const [vendorConcentration, setVendorConcentration] = useState<any[]>([]);
  const [flaggedTxs, setFlaggedTxs] = useState<any[]>([]);
  const [highRiskVendors, setHighRiskVendors] = useState<any[]>([]);
  const [procurementByCategory, setProcurementByCategory] = useState<any[]>([]);
  const [insights, setInsights] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [sumRes, trendRes, vendorRes, txRes, hrVendorRes, catRes, insRes] = await Promise.all([
          api.get('/dashboard/summary'),
          api.get('/dashboard/risk-trend'),
          api.get('/dashboard/vendor-concentration'),
          api.get('/dashboard/flagged-transactions'),
          api.get('/dashboard/high-risk-vendors'),
          api.get('/dashboard/procurement-by-category'),
          api.get('/dashboard/insights'),
        ]);
        
        setSummary(sumRes.data);
        setRiskTrend(trendRes.data);
        setVendorConcentration(vendorRes.data);
        setFlaggedTxs(txRes.data);
        setHighRiskVendors(hrVendorRes.data);
        setProcurementByCategory(catRes.data);
        setInsights(insRes.data);
      } catch (err) {
        console.error(err);
        setError('Failed to load dashboard data. Please try again.');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const formatCurrency = (val: number) => {
    if (val >= 10000000) return `₹ ${(val / 10000000).toFixed(2)} Cr`;
    if (val >= 100000) return `₹ ${(val / 100000).toFixed(2)} L`;
    return `₹ ${val.toLocaleString()}`;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pg-navy"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 text-red-600 p-4 rounded-lg flex flex-col items-center justify-center">
        <AlertTriangle className="w-8 h-8 mb-2" />
        <p>{error}</p>
        <button onClick={() => window.location.reload()} className="mt-4 px-4 py-2 bg-red-100 rounded hover:bg-red-200 text-sm font-medium">Retry</button>
      </div>
    );
  }

  const COLORS = ['#0A2540', '#1E40AF', '#3B82F6', '#93C5FD', '#E5E7EB'];

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-10">
      
      {/* Header Section */}
      <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-1">Welcome back, {user?.name.split(' ')[0]}</h1>
          <p className="text-sm text-gray-500 max-w-2xl">Monitor procurement activities, detect anomalies and ensure transparent governance across all Gram Panchayats.</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 bg-white px-4 py-2 rounded-lg shadow-sm border border-gray-200 cursor-pointer">
            <Calendar className="w-4 h-4 text-gray-500" />
            <span className="text-sm font-medium text-gray-700">Jan 2024 - Dec 2024</span>
            <ChevronRight className="w-4 h-4 text-gray-400 rotate-90" />
          </div>
          <div className="text-right hidden lg:block">
             <p className="text-xs italic text-gray-500">"Accountable Panchayats<br/>Prosperous Villages"</p>
             <div className="flex gap-1 mt-1 justify-end">
               <div className="h-1 w-6 bg-orange-500 rounded"></div>
               <div className="h-1 w-6 bg-gray-300 rounded"></div>
               <div className="h-1 w-6 bg-green-500 rounded"></div>
             </div>
          </div>
        </div>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4 relative overflow-hidden">
          <div className="p-3 bg-blue-50 rounded-lg shrink-0">
            <TrendingUp className="w-8 h-8 text-pg-blue" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500 mb-1">Total Procurement</p>
            <h3 className="text-2xl font-bold text-gray-900">{formatCurrency(summary.total_procurement)}</h3>
            <p className="text-xs font-semibold text-green-600 mt-1 flex items-center gap-1">
              ↗ {summary.procurement_change} <span className="text-gray-400 font-normal">vs. previous year</span>
            </p>
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4 relative overflow-hidden">
          <div className="p-3 bg-blue-50 rounded-lg shrink-0">
            <FileText className="w-8 h-8 text-pg-blue" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500 mb-1">Transactions Analyzed</p>
            <h3 className="text-2xl font-bold text-gray-900">{summary.transactions_analyzed.toLocaleString()}</h3>
            <p className="text-xs font-semibold text-green-600 mt-1 flex items-center gap-1">
              ↗ {summary.transaction_change} <span className="text-gray-400 font-normal">vs. previous year</span>
            </p>
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl shadow-sm border border-red-100 flex items-center gap-4 relative overflow-hidden">
          <div className="p-3 bg-red-50 rounded-lg shrink-0">
            <AlertTriangle className="w-8 h-8 text-red-500" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500 mb-1">High Risk Alerts</p>
            <h3 className="text-2xl font-bold text-red-600">{summary.high_risk_alerts}</h3>
            <p className="text-xs font-semibold text-red-500 mt-1 flex items-center gap-1">
              ↗ {summary.alert_change} <span className="text-gray-400 font-normal">vs. previous month</span>
            </p>
          </div>
          {/* Subtle red indicator */}
          <div className="absolute top-0 right-0 w-16 h-16 bg-gradient-to-bl from-red-50 to-transparent"></div>
        </div>
      </div>

      {/* Main Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Line Chart */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 lg:col-span-2 flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-lg font-bold text-gray-800">Procurement Risk Trend</h3>
              <p className="text-sm text-gray-500">Average risk score based on analyzed transactions</p>
            </div>
            <div className="flex gap-2">
               <select className="text-xs border border-gray-200 rounded px-2 py-1 bg-gray-50 outline-none"><option>Monthly</option></select>
               <select className="text-xs border border-gray-200 rounded px-2 py-1 bg-gray-50 outline-none"><option>2024</option></select>
            </div>
          </div>
          <div className="flex-1 min-h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={riskTrend} margin={{ top: 20, right: 30, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                <XAxis dataKey="month" axisLine={false} tickLine={false} tick={{fill: '#6B7280', fontSize: 12}} dy={10} />
                <YAxis axisLine={false} tickLine={false} tick={{fill: '#6B7280', fontSize: 12}} />
                <RechartsTooltip 
                  contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                  formatter={(value: any) => [`${value}`, 'Risk Score']}
                />
                <Line type="monotone" dataKey="risk_score" stroke="#1E40AF" strokeWidth={3} dot={{r: 4, fill: '#1E40AF'}} activeDot={{r: 8, fill: '#EF4444', stroke: '#fff', strokeWidth: 2}} />
                {/* Reference line equivalent - hardcoded for visual flair as per design */}
                <Line type="step" dataKey={() => 70} stroke="#EF4444" strokeDasharray="5 5" strokeWidth={1} dot={false} activeDot={false} name="High Risk Threshold" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Doughnut Chart */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col">
          <h3 className="text-lg font-bold text-gray-800">Vendor Concentration</h3>
          <p className="text-sm text-gray-500 mb-4">Share of total procurement value</p>
          <div className="flex-1 relative min-h-[250px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={vendorConcentration}
                  cx="50%"
                  cy="50%"
                  innerRadius={70}
                  outerRadius={100}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {vendorConcentration.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <RechartsTooltip formatter={(val: number) => formatCurrency(val)} />
              </PieChart>
            </ResponsiveContainer>
            {/* Center text */}
            <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
               <span className="text-xl font-bold text-gray-800">{formatCurrency(summary.total_procurement)}</span>
               <span className="text-[10px] text-gray-500">Total Procurement</span>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-y-2 mt-4">
             {vendorConcentration.map((v, i) => (
                <div key={i} className="flex items-center gap-2">
                   <div className="w-3 h-3 rounded-full" style={{backgroundColor: COLORS[i % COLORS.length]}}></div>
                   <span className="text-xs text-gray-600 truncate" title={v.name}>{v.name}</span>
                </div>
             ))}
          </div>
        </div>
      </div>

      {/* Bottom Section */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        
        {/* Top High-Risk Vendors */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
             <div>
               <h3 className="text-lg font-bold text-gray-800">Top High-Risk Vendors</h3>
               <p className="text-sm text-gray-500">Based on risk score, transaction patterns and anomalies</p>
             </div>
             <a href="#" className="text-sm text-pg-blue font-medium hover:underline flex items-center">View All <ChevronRight className="w-4 h-4"/></a>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left text-gray-600">
              <thead className="text-xs text-gray-500 uppercase bg-gray-50 border-b border-gray-100">
                <tr>
                  <th className="px-4 py-3 font-semibold">#</th>
                  <th className="px-4 py-3 font-semibold">Vendor Name</th>
                  <th className="px-4 py-3 font-semibold">Total Value</th>
                  <th className="px-4 py-3 font-semibold">Transactions</th>
                  <th className="px-4 py-3 font-semibold">Risk Score</th>
                  <th className="px-4 py-3 font-semibold">Status</th>
                </tr>
              </thead>
              <tbody>
                {highRiskVendors.map((v, i) => (
                  <tr key={v.id} className="border-b border-gray-50 hover:bg-gray-50 transition-colors">
                    <td className="px-4 py-3">{i+1}</td>
                    <td className="px-4 py-3 font-medium text-gray-800">{v.vendor_name}</td>
                    <td className="px-4 py-3">{formatCurrency(v.total_value)}</td>
                    <td className="px-4 py-3 text-center">{v.transactions}</td>
                    <td className="px-4 py-3">
                       <span className={`font-bold ${v.risk_score >= 80 ? 'text-red-500' : 'text-orange-500'}`}>{v.risk_score}</span>
                    </td>
                    <td className="px-4 py-3">
                       <span className={`px-2 py-1 rounded text-xs font-semibold ${v.status === 'High Risk' ? 'bg-red-100 text-red-700' : v.status === 'Medium Risk' ? 'bg-orange-100 text-orange-700' : 'bg-green-100 text-green-700'}`}>
                         {v.status}
                       </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Procurement by Category */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
           <div className="flex items-center justify-between mb-4">
             <div>
               <h3 className="text-lg font-bold text-gray-800">Procurement by Category</h3>
               <p className="text-sm text-gray-500">Total value by procurement category</p>
             </div>
           </div>
           <div className="space-y-4">
             {procurementByCategory.map((c, i) => (
                <div key={i}>
                  <div className="flex justify-between items-end mb-1">
                    <div className="flex items-center gap-2">
                      <Zap className="w-4 h-4 text-gray-400" />
                      <span className="text-sm font-medium text-gray-700 truncate w-32" title={c.category}>{c.category}</span>
                    </div>
                    <div className="text-right">
                       <span className="text-xs text-gray-500 block">{formatCurrency(c.value)}</span>
                       <span className="text-xs font-bold text-gray-800">{c.percentage}%</span>
                    </div>
                  </div>
                  <div className="w-full bg-gray-100 rounded-full h-2">
                    <div className="bg-pg-blue h-2 rounded-full" style={{ width: `${c.percentage}%` }}></div>
                  </div>
                </div>
             ))}
           </div>
        </div>

        {/* Flagged Transactions / Insights */}
        <div className="space-y-6">
           <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col h-full">
             <div className="flex items-center justify-between mb-4">
               <h3 className="text-lg font-bold text-gray-800">Flagged Transactions</h3>
               <a href="#" className="text-sm text-pg-blue font-medium hover:underline flex items-center">View All <ChevronRight className="w-4 h-4"/></a>
             </div>
             <div className="flex-1 space-y-4">
                {flaggedTxs.map(tx => (
                  <div key={tx.id} className="flex gap-3 cursor-pointer hover:bg-gray-50 p-2 -mx-2 rounded transition-colors border-l-2 border-transparent hover:border-pg-blue">
                     <div className={`w-10 h-10 shrink-0 rounded flex items-center justify-center text-white font-bold text-sm ${tx.risk_score >= 80 ? 'bg-red-500' : 'bg-orange-500'}`}>
                       {tx.risk_score}
                     </div>
                     <div className="flex-1 min-w-0">
                       <h4 className="text-sm font-semibold text-gray-900 truncate" title={tx.description}>{tx.description}</h4>
                       <p className="text-xs text-gray-500 truncate">{tx.panchayat_name}</p>
                       <div className="flex items-center gap-2 mt-1">
                         <span className="text-xs text-gray-400">{tx.date}</span>
                         <span className={`text-[10px] px-1.5 py-0.5 rounded font-semibold ${tx.severity === 'High' ? 'bg-red-100 text-red-600' : 'bg-orange-100 text-orange-600'}`}>{tx.alert_type}</span>
                       </div>
                     </div>
                     <div className="text-right shrink-0">
                       <span className="text-sm font-bold text-gray-800 block">₹ {(tx.amount/100000).toFixed(1)} L</span>
                       <ChevronRight className="w-4 h-4 text-gray-300 ml-auto mt-1" />
                     </div>
                  </div>
                ))}
             </div>
           </div>
        </div>
      </div>

      {/* AI Insights Panel */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-blue-100 mt-6 relative overflow-hidden">
        <div className="absolute top-0 left-0 w-1 h-full bg-pg-blue"></div>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Brain className="w-5 h-5 text-pg-blue" />
            <h3 className="text-lg font-bold text-gray-800">AI Insights</h3>
          </div>
          <a href="#" className="text-sm text-pg-blue font-medium hover:underline flex items-center">View All <ChevronRight className="w-4 h-4"/></a>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {insights.map((ins, i) => (
             <div key={i} className="flex gap-3 items-start bg-blue-50/50 p-3 rounded-lg border border-blue-50 hover:border-blue-100 transition-colors cursor-pointer">
               <div className="p-1.5 bg-white rounded-full shrink-0 shadow-sm border border-blue-100">
                  {ins.icon === 'TrendingUp' && <TrendingUp className="w-4 h-4 text-blue-600" />}
                  {ins.icon === 'AlertCircle' && <AlertCircle className="w-4 h-4 text-blue-600" />}
                  {ins.icon === 'Link' && <LinkIcon className="w-4 h-4 text-blue-600" />}
                  {ins.icon === 'PieChart' && <PieChartIcon className="w-4 h-4 text-blue-600" />}
                  {ins.icon === 'Lightbulb' && <Lightbulb className="w-4 h-4 text-amber-500" />}
               </div>
               <p className="text-xs text-gray-700 leading-tight flex-1">{ins.text}</p>
               <ChevronRight className="w-4 h-4 text-gray-300 shrink-0" />
             </div>
          ))}
        </div>
      </div>
    </div>
  );
}
""")

print("Dashboard components updated successfully!")
