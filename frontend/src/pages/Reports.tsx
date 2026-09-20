import React, { useState } from 'react';
import api from '../services/api';
import { FileText, Download, Filter, Printer, FileSpreadsheet, Eye, RefreshCw } from 'lucide-react';
import jsPDF from 'jspdf';
import 'jspdf-autotable';

export default function Reports() {
  const [reportType, setReportType] = useState('Procurement Report');
  const [district, setDistrict] = useState('');
  const [dateRange, setDateRange] = useState('');
  const [riskLevel, setRiskLevel] = useState('');
  
  const [loading, setLoading] = useState(false);
  const [previewData, setPreviewData] = useState<any>(null);

  const handleGenerate = async () => {
     setLoading(true);
     try {
        const params = new URLSearchParams({ type: reportType });
        if (district) params.append('district', district);
        if (riskLevel) params.append('risk_level', riskLevel);
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
        if (riskLevel) params.append('risk_level', riskLevel);
        
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
     if (riskLevel) doc.text(`Filter: Risk Level = ${riskLevel}`, 14, 58);
     
     // Summary
     doc.setFontSize(11);
     doc.text(`Total Records: ${previewData.count}`, 14, 68);
     doc.text(`Total Value: Rs. ${previewData.total_value.toLocaleString()}`, 14, 74);

     // Table
     const tableColumn = ["ID", "Date", "Vendor", "Panchayat", "Category", "Amount", "Risk"];
     const tableRows: any[] = [];

     previewData.data.forEach((row: any) => {
        tableRows.push([
           row["Transaction ID"],
           row["Date"],
           row["Vendor"],
           row["Panchayat"],
           row["Category"],
           row["Amount"].toLocaleString(),
           row["Risk"]
        ]);
     });

     (doc as any).autoTable({
        startY: 80,
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
           <div className="text-sm text-gray-500 mb-1">Dashboard &gt; Reports & Exports</div>
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

            <div>
               <label className="block text-sm font-medium text-gray-700 mb-1">Risk Level</label>
               <select className="w-full text-sm border rounded p-2 focus:ring-1 focus:ring-pg-blue" value={riskLevel} onChange={e=>setRiskLevel(e.target.value)}>
                  <option value="">All Risks</option>
                  <option>Critical Risk</option>
                  <option>High Risk</option>
                  <option>Medium Risk</option>
                  <option>Low Risk</option>
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
                              <th className="px-3 py-2">Risk</th>
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
                                 <td className="px-3 py-2 text-gray-600">{row["Risk"]}</td>
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
