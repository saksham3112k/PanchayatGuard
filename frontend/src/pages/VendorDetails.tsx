import React, { useEffect, useState } from 'react';
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
                           <Tooltip cursor={{fill: '#f3f4f6'}} contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}} formatter={(val: any) => [`₹ ${(val/100000).toFixed(1)}L`, 'Amount']} />
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
                           <Tooltip formatter={(val: any) => `₹ ${(val/100000).toFixed(2)}L`} />
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
