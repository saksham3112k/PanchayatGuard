import os

frontend_dir = r"c:\Users\Dell\OneDrive\Desktop\PANCHAYATGUARD\panchayatguard\frontend\src"

# 1. Update App.tsx
app_tsx_path = os.path.join(frontend_dir, "App.tsx")
with open(app_tsx_path, "r", encoding="utf-8") as f:
    app_tsx = f.read()

if "import GeographicView" not in app_tsx:
    app_tsx = app_tsx.replace(
        "import RiskAnalysis from './pages/RiskAnalysis';",
        "import RiskAnalysis from './pages/RiskAnalysis';\nimport GeographicView from './pages/GeographicView';\nimport Reports from './pages/Reports';"
    )
    app_tsx = app_tsx.replace(
        "<Route path=\"/geo\" element={<Placeholder />} />",
        "<Route path=\"/geo\" element={<GeographicView />} />"
    )
    app_tsx = app_tsx.replace(
        "<Route path=\"/reports\" element={<Placeholder />} />",
        "<Route path=\"/reports\" element={<Reports />} />"
    )
    with open(app_tsx_path, "w", encoding="utf-8") as f:
        f.write(app_tsx)

# 2. GeographicView.tsx
geo_tsx_path = os.path.join(frontend_dir, "pages", "GeographicView.tsx")
with open(geo_tsx_path, "w", encoding="utf-8") as f:
    f.write("""import React, { useEffect, useState } from 'react';
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
           <div className="text-sm text-gray-500 mb-1">Dashboard > Geographic View</div>
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
                            <div className={`text-xs font-bold mt-1 ${p.risk_score >= 80 ? 'text-red-500' : 'text-green-500'}`}>Risk Score: {p.risk_score} ({p.risk_level})</div>
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
""")

# 3. Reports.tsx
reports_tsx_path = os.path.join(frontend_dir, "pages", "Reports.tsx")
with open(reports_tsx_path, "w", encoding="utf-8") as f:
    f.write("""import React, { useState } from 'react';
import api from '../services/api';
import { FileText, Download, Filter, Printer, FileSpreadsheet, Eye, RefreshCw } from 'lucide-react';
import jsPDF from 'jspdf';
import 'jspdf-autotable';

export default function Reports() {
  const [reportType, setReportType] = useState('Procurement Report');
  const [district, setDistrict] = useState('');
  const [dateRange, setDateRange] = useState('');
  
  const [loading, setLoading] = useState(false);
  const [previewData, setPreviewData] = useState<any>(null);

  const handleGenerate = async () => {
     setLoading(true);
     try {
        const params = new URLSearchParams({ type: reportType });
        if (district) params.append('district', district);
        const res = await api.get(`/reports/generate?${params.toString()}`);
        setPreviewData(res.data);
     } catch (e) {
        console.error(e);
        alert("Failed to generate report.");
     } finally {
        setLoading(false);
     }
  };

  const handleDownloadCSV = async () => {
     try {
        const params = new URLSearchParams({ type: reportType });
        if (district) params.append('district', district);
        
        const res = await api.get(`/reports/export/csv?${params.toString()}`, { responseType: 'blob' });
        const url = window.URL.createObjectURL(new Blob([res.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `PanchayatGuard_${reportType.replace(' ', '_')}.csv`);
        document.body.appendChild(link);
        link.click();
        link.remove();
     } catch(e) { console.error(e); }
  };

  const handleDownloadPDF = () => {
     if (!previewData || !previewData.data || previewData.data.length === 0) {
        alert("Please generate a report first."); return;
     }
     
     const doc = new jsPDF();
     
     // Branding
     doc.setFontSize(22);
     doc.setTextColor(30, 64, 175); // pg-navy
     doc.text("PanchayatGuard", 14, 22);
     
     doc.setFontSize(10);
     doc.setTextColor(100);
     doc.text("Transparent Panchayat. Stronger Bharat.", 14, 28);
     
     doc.setFontSize(16);
     doc.setTextColor(20);
     doc.text(previewData.report_type, 14, 40);
     
     doc.setFontSize(10);
     doc.text(`Generated on: ${new Date().toLocaleString()}`, 14, 46);
     if (district) doc.text(`Filter: District = ${district}`, 14, 52);
     
     // Summary
     doc.setFontSize(11);
     doc.text(`Total Records: ${previewData.count}`, 14, 62);
     doc.text(`Total Value: Rs. ${previewData.total_value.toLocaleString()}`, 14, 68);

     // Table
     const tableColumn = ["ID", "Date", "Vendor", "Panchayat", "Category", "Amount", "Status"];
     const tableRows: any[] = [];

     previewData.data.forEach((row: any) => {
        tableRows.push([
           row["Transaction ID"],
           row["Date"],
           row["Vendor"],
           row["Panchayat"],
           row["Category"],
           row["Amount"].toLocaleString(),
           row["Status"]
        ]);
     });

     (doc as any).autoTable({
        startY: 75,
        head: [tableColumn],
        body: tableRows,
        theme: 'grid',
        headStyles: { fillColor: [30, 64, 175] },
        styles: { fontSize: 8 }
     });

     doc.save(`PanchayatGuard_${reportType.replace(' ', '_')}.pdf`);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
           <div className="text-sm text-gray-500 mb-1">Dashboard > Reports & Exports</div>
           <h1 className="text-2xl font-bold text-gray-900">Custom Reports</h1>
           <p className="text-sm text-gray-500">Generate, preview, and export professional compliance reports.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
         {/* Configuration Panel */}
         <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-5 space-y-5 h-fit">
            <h3 className="font-bold text-gray-800 border-b pb-2">Report Configuration</h3>
            
            <div>
               <label className="block text-sm font-medium text-gray-700 mb-1">Report Type</label>
               <select className="w-full text-sm border rounded p-2 focus:ring-1 focus:ring-pg-blue" value={reportType} onChange={e=>setReportType(e.target.value)}>
                  <option>Procurement Report</option>
                  <option>Risk Report</option>
                  <option>Vendor Report</option>
                  <option>Panchayat Report</option>
                  <option>Audit Report</option>
               </select>
            </div>

            <div>
               <label className="block text-sm font-medium text-gray-700 mb-1">Date Range</label>
               <select className="w-full text-sm border rounded p-2 focus:ring-1 focus:ring-pg-blue">
                  <option>All Time</option>
                  <option>This Month</option>
                  <option>Last 3 Months</option>
                  <option>This Year</option>
               </select>
            </div>

            <div>
               <label className="block text-sm font-medium text-gray-700 mb-1">District</label>
               <select className="w-full text-sm border rounded p-2 focus:ring-1 focus:ring-pg-blue" value={district} onChange={e=>setDistrict(e.target.value)}>
                  <option value="">All Districts</option>
                  <option>Kanpur</option>
                  <option>Lucknow</option>
                  <option>Varanasi</option>
                  <option>Agra</option>
               </select>
            </div>

            <button onClick={handleGenerate} className="w-full flex items-center justify-center gap-2 px-4 py-2 text-sm font-bold text-white bg-pg-blue rounded hover:bg-blue-700 shadow transition-colors">
               {loading ? <RefreshCw className="w-4 h-4 animate-spin"/> : <TargetIcon />} Generate Report
            </button>
         </div>

         {/* Preview Panel */}
         <div className="col-span-3 bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden flex flex-col min-h-[500px]">
            <div className="p-4 border-b flex justify-between items-center bg-gray-50">
               <h3 className="font-bold text-gray-800 flex items-center gap-2"><Eye className="w-4 h-4"/> Report Preview</h3>
               <div className="flex items-center gap-3">
                  <button onClick={handleDownloadCSV} disabled={!previewData} className="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-green-700 bg-green-50 border border-green-200 rounded hover:bg-green-100 disabled:opacity-50">
                     <FileSpreadsheet className="w-4 h-4"/> CSV
                  </button>
                  <button onClick={handleDownloadPDF} disabled={!previewData} className="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-red-700 bg-red-50 border border-red-200 rounded hover:bg-red-100 disabled:opacity-50">
                     <Download className="w-4 h-4"/> Export PDF
                  </button>
               </div>
            </div>

            <div className="flex-1 p-6 bg-gray-100/50">
               {previewData ? (
                  <div className="bg-white p-8 border shadow-sm mx-auto max-w-4xl min-h-[600px]">
                     {/* Print Style Header */}
                     <div className="border-b-2 border-pg-navy pb-4 mb-6">
                        <div className="text-3xl font-extrabold text-pg-navy">PanchayatGuard</div>
                        <div className="text-gray-500 font-medium text-sm mt-1">Government Technology Procurement Intelligence</div>
                        <div className="mt-6 flex justify-between items-end">
                           <div>
                              <h2 className="text-xl font-bold text-gray-800">{previewData.report_type}</h2>
                              <div className="text-sm text-gray-500 mt-1">Generated: {new Date().toLocaleString()}</div>
                           </div>
                           <div className="text-right text-sm">
                              <div><span className="font-semibold">Total Records:</span> {previewData.count}</div>
                              <div><span className="font-semibold">Total Value:</span> ₹ {(previewData.total_value).toLocaleString()}</div>
                           </div>
                        </div>
                     </div>

                     {/* Data Table */}
                     <table className="w-full text-xs text-left">
                        <thead className="bg-pg-navy text-white">
                           <tr>
                              <th className="px-3 py-2">ID</th>
                              <th className="px-3 py-2">Date</th>
                              <th className="px-3 py-2">Vendor</th>
                              <th className="px-3 py-2">Panchayat</th>
                              <th className="px-3 py-2">Amount</th>
                           </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                           {previewData.data.slice(0, 15).map((row: any, i: number) => (
                              <tr key={i}>
                                 <td className="px-3 py-2 font-medium">{row["Transaction ID"]}</td>
                                 <td className="px-3 py-2 text-gray-600">{row["Date"]}</td>
                                 <td className="px-3 py-2 text-gray-900">{row["Vendor"]}</td>
                                 <td className="px-3 py-2 text-gray-900">{row["Panchayat"]}</td>
                                 <td className="px-3 py-2 font-medium text-gray-900">₹ {(row["Amount"]).toLocaleString()}</td>
                              </tr>
                           ))}
                        </tbody>
                     </table>
                     {previewData.data.length > 15 && (
                        <div className="mt-4 text-center text-xs text-gray-500 italic">Showing 15 of {previewData.count} records. Download PDF/CSV for full report.</div>
                     )}
                  </div>
               ) : (
                  <div className="flex flex-col items-center justify-center h-full text-gray-400">
                     <FileText className="w-16 h-16 mb-4 text-gray-300"/>
                     <p className="font-medium">Configure and generate a report to see preview</p>
                  </div>
               )}
            </div>
         </div>
      </div>
    </div>
  );
}

const TargetIcon = () => <FileText className="w-4 h-4"/>;
""")

print("Phase 5 Frontend components generated successfully!")
