import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { Filter, Building2, MapPin, AlertTriangle, ShieldCheck, Download, IndianRupee } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

export default function GeographicView() {
  const [summary, setSummary] = useState<any>(null);
  const [panchayats, setPanchayats] = useState<any[]>([]);
  
  const [district, setDistrict] = useState('All Districts');
  const [riskLevel, setRiskLevel] = useState('All Risk Levels');
  
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [sumRes, pRes] = await Promise.all([
          api.get('/geo/summary'),
          api.get('/geo/panchayats', {
             params: {
                district: district !== 'All Districts' ? district : undefined,
                risk_level: riskLevel
             }
          })
        ]);
        setSummary(sumRes.data);
        setPanchayats(pRes.data);
      } catch(e) { console.error(e); } finally { setLoading(false); }
    };
    fetchData();
  }, [district, riskLevel]);

  const COLORS = ['#10b981', '#f59e0b', '#ef4444'];
  const getMarkerColor = (level: string) => {
    if (level === 'Critical' || level === 'High') return '#ef4444';
    if (level === 'Medium') return '#f59e0b';
    return '#10b981';
  };

  if (!summary) return <div className="p-8">Loading geographic data...</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
           <div className="text-sm text-gray-500 mb-1">Dashboard &gt; Geographic View</div>
           <h1 className="text-2xl font-bold text-gray-900">Geographic View</h1>
           <p className="text-sm text-gray-500">Visualize procurement activities and risk levels across Gram Panchayats</p>
        </div>
        <div className="text-right text-pg-blue italic text-sm font-medium">
           "Stronger Panchayats<br/>Stronger Communities"
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
         <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex items-center gap-4">
            <div className="p-3 bg-blue-50 rounded text-pg-blue"><Building2 className="w-6 h-6"/></div>
            <div>
               <div className="text-xs text-gray-500 font-medium">Total Panchayats</div>
               <div className="text-xl font-bold text-gray-900">{summary.total_panchayats.toLocaleString()}</div>
            </div>
         </div>
         <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex items-center gap-4">
            <div className="p-3 bg-blue-50 rounded text-pg-blue"><IndianRupee className="w-6 h-6"/></div>
            <div>
               <div className="text-xs text-gray-500 font-medium">Total Procurement</div>
               <div className="text-xl font-bold text-gray-900">₹ {(summary.total_procurement/10000000).toFixed(2)} Cr</div>
            </div>
         </div>
         <div className="bg-white p-4 rounded-xl border border-red-100 shadow-sm flex items-center gap-4">
            <div className="p-3 bg-red-50 rounded text-red-500"><AlertTriangle className="w-6 h-6"/></div>
            <div>
               <div className="text-xs text-red-500 font-medium">High Risk Panchayats</div>
               <div className="text-xl font-bold text-red-600">{summary.high_risk_panchayats}</div>
            </div>
         </div>
         <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex items-center gap-4">
            <div className="p-3 bg-blue-50 rounded text-pg-blue"><MapPin className="w-6 h-6"/></div>
            <div>
               <div className="text-xs text-gray-500 font-medium">Districts Covered</div>
               <div className="text-xl font-bold text-gray-900">{summary.districts_covered} / {summary.total_districts}</div>
            </div>
         </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
         {/* Map */}
         <div className="col-span-3 bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden flex flex-col h-[500px]">
            <div className="p-4 border-b flex justify-between items-center bg-gray-50">
               <h3 className="font-bold text-gray-800">Panchayat Procurement Map</h3>
               <div className="flex gap-4 text-xs font-semibold">
                  <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-green-500"></span> Low Risk</span>
                  <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-orange-500"></span> Medium Risk</span>
                  <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-red-500"></span> High/Critical Risk</span>
               </div>
            </div>
            <div className="flex-1 w-full bg-gray-100 relative z-0">
               {!loading && (
                 <MapContainer center={[26.8, 80.9]} zoom={6} className="w-full h-full z-0">
                   <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution='&copy; OpenStreetMap' />
                   {panchayats.map(p => (
                      <CircleMarker 
                         key={p.id} 
                         center={[p.lat, p.lng]} 
                         radius={6} 
                         fillOpacity={0.7} 
                         color="white" 
                         weight={1} 
                         fillColor={getMarkerColor(p.risk_level)}>
                         <Popup>
                            <div className="font-bold text-pg-blue mb-1">{p.name} Gram Panchayat</div>
                            <div className="text-xs text-gray-600">District: {p.district}</div>
                            <div className="text-xs text-gray-600">Total Procurement: ₹ {(p.total_procurement/10000000).toFixed(2)} Cr</div>
                            <div className="text-xs text-gray-600">Transactions: {p.transaction_count}</div>
                            <div className="text-xs text-gray-600">Top Vendor: {p.top_vendor}</div>
                            <div className={`text-xs font-bold mt-1 ${p.risk_score >= 70 ? 'text-red-500' : p.risk_score >= 40 ? 'text-orange-500' : 'text-green-500'}`}>Risk Score: {p.risk_score} ({p.risk_level})</div>
                         </Popup>
                      </CircleMarker>
                   ))}
                 </MapContainer>
               )}
            </div>
         </div>

         {/* Filters & Summary List */}
         <div className="space-y-6">
            <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
               <div className="flex justify-between items-center mb-4">
                  <h3 className="font-bold text-gray-800">Filters</h3>
                  <button onClick={()=>{setDistrict('All Districts'); setRiskLevel('All Risk Levels');}} className="text-xs text-pg-blue font-semibold hover:underline">Reset All</button>
               </div>
               <div className="space-y-4">
                  <div>
                     <label className="block text-xs font-medium text-gray-500 mb-1">State</label>
                     <select className="w-full text-sm border rounded p-2 focus:ring-1 focus:ring-pg-blue bg-gray-50" disabled><option>Uttar Pradesh</option></select>
                  </div>
                  <div>
                     <label className="block text-xs font-medium text-gray-500 mb-1">District</label>
                     <select className="w-full text-sm border rounded p-2 focus:ring-1 focus:ring-pg-blue" value={district} onChange={e=>setDistrict(e.target.value)}>
                        <option>All Districts</option>
                        <option>Kanpur</option>
                        <option>Lucknow</option>
                        <option>Varanasi</option>
                        <option>Agra</option>
                        <option>Prayagraj</option>
                        <option>Gorakhpur</option>
                        <option>Meerut</option>
                     </select>
                  </div>
                  <div>
                     <label className="block text-xs font-medium text-gray-500 mb-1">Risk Level</label>
                     <select className="w-full text-sm border rounded p-2 focus:ring-1 focus:ring-pg-blue" value={riskLevel} onChange={e=>setRiskLevel(e.target.value)}>
                        <option>All Risk Levels</option>
                        <option>High Risk</option>
                        <option>Medium Risk</option>
                        <option>Low Risk</option>
                     </select>
                  </div>
               </div>
            </div>

            <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
               <div className="bg-gray-50 px-4 py-3 border-b font-bold text-gray-800 flex items-center gap-2"><MapPin className="w-4 h-4"/> Top Panchayats</div>
               <div className="p-4 space-y-3">
                  {panchayats.sort((a,b) => b.total_procurement - a.total_procurement).slice(0,5).map((p, i) => (
                     <div key={p.id} className="flex items-center justify-between">
                        <div className="flex items-center gap-2 text-sm">
                           <span className="w-5 h-5 rounded-full bg-gray-100 text-xs flex items-center justify-center font-bold text-gray-500">{i+1}</span>
                           <span className="font-medium text-gray-900">{p.name} <span className="text-gray-400 text-xs">({p.district})</span></span>
                        </div>
                        <div className="text-sm font-bold text-gray-900">₹ {(p.total_procurement/10000000).toFixed(2)} Cr</div>
                     </div>
                  ))}
               </div>
            </div>
         </div>
      </div>
    </div>
  );
}
