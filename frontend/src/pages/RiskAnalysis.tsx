import React, { useEffect, useState } from 'react';
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
           <div className="text-sm text-gray-500 mb-1">Dashboard &gt; Risk Analysis</div>
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
