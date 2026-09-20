import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { 
  Search, Filter, Download, Plus, Edit, Eye, Trash2, 
  ChevronLeft, ChevronRight, AlertTriangle, FileText, Calendar
} from 'lucide-react';
import TransactionDrawer from '../components/TransactionDrawer';
import TransactionDetails from '../components/TransactionDetails';

export default function Procurement() {
  const [summary, setSummary] = useState<any>(null);
  const [transactions, setTransactions] = useState<any[]>([]);
  const [totalItems, setTotalItems] = useState(0);
  const [page, setPage] = useState(1);
  const pageSize = 10;
  
  const [search, setSearch] = useState('');
  const [district, setDistrict] = useState('');
  const [panchayatId, setPanchayatId] = useState('');
  const [vendorId, setVendorId] = useState('');
  const [category, setCategory] = useState('');
  const [riskLevel, setRiskLevel] = useState('');

  const [dropdowns, setDropdowns] = useState<any>({ panchayats: [], vendors: [], categories: [] });
  const [loading, setLoading] = useState(true);

  const [drawerOpen, setDrawerOpen] = useState(false);
  const [editingTx, setEditingTx] = useState<any>(null);

  const [detailsOpen, setDetailsOpen] = useState(false);
  const [viewingTxId, setViewingTxId] = useState<number | null>(null);

  const fetchDropdowns = async () => {
    try {
      const res = await api.get('/procurement/dropdowns');
      setDropdowns(res.data);
    } catch (e) { console.error(e); }
  };

  const fetchSummary = async () => {
    try {
      const res = await api.get('/procurement/summary');
      setSummary(res.data);
    } catch (e) { console.error(e); }
  };

  const fetchTransactions = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams({
        page: page.toString(),
        page_size: pageSize.toString(),
      });
      if (search) params.append('search', search);
      if (panchayatId) params.append('panchayat_id', panchayatId);
      if (vendorId) params.append('vendor_id', vendorId);
      if (category) params.append('category', category);
      
      const res = await api.get(`/procurement/transactions?${params.toString()}`);
      setTransactions(res.data.data);
      setTotalItems(res.data.total);
    } catch (e) { console.error(e); } finally { setLoading(false); }
  };

  useEffect(() => {
    fetchDropdowns();
    fetchSummary();
  }, []);

  useEffect(() => {
    const delay = setTimeout(() => { fetchTransactions(); }, 300);
    return () => clearTimeout(delay);
  }, [page, search, panchayatId, vendorId, category, riskLevel]);

  const handleExportCSV = async () => {
    try {
      const params = new URLSearchParams();
      if (search) params.append('search', search);
      if (panchayatId) params.append('panchayat_id', panchayatId);
      if (vendorId) params.append('vendor_id', vendorId);
      if (category) params.append('category', category);
      
      const res = await api.get(`/procurement/export?${params.toString()}`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'transactions.csv');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (e) { console.error(e); }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this transaction? This action will be logged.')) {
      try {
        await api.delete(`/procurement/transactions/${id}`);
        fetchTransactions();
        fetchSummary();
      } catch (e) { console.error(e); alert('Error deleting transaction'); }
    }
  };

  const formatCurrency = (val: number) => {
    if (val >= 10000000) return `? ${(val / 10000000).toFixed(2)} Cr`;
    if (val >= 100000) return `? ${(val / 100000).toFixed(2)} L`;
    return `? ${val.toLocaleString()}`;
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
           <div className="text-sm text-gray-500 mb-1">Dashboard &gt; Procurement</div>
           <h1 className="text-2xl font-bold text-gray-900">Procurement Management</h1>
           <p className="text-sm text-gray-500">Track, manage, and analyze procurement transactions across all Gram Panchayats.</p>
        </div>
        <div className="text-right text-pg-blue italic text-sm font-medium">
           "Better Procurement<br/>Brighter Communities"
        </div>
      </div>

      {/* KPI Stats */}
      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex items-center gap-4">
            <div className="p-3 bg-blue-50 rounded text-pg-blue"><FileText className="w-6 h-6" /></div>
            <div>
              <div className="text-xs text-gray-500 font-medium">Total Transactions</div>
              <div className="text-xl font-bold text-gray-900">{summary.total_transactions.toLocaleString()}</div>
            </div>
          </div>
          <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex items-center gap-4">
            <div className="p-3 bg-blue-50 rounded text-pg-blue"><span className="text-xl font-bold">?</span></div>
            <div>
              <div className="text-xs text-gray-500 font-medium">Total Value</div>
              <div className="text-xl font-bold text-gray-900">{formatCurrency(summary.total_value)}</div>
            </div>
          </div>
          <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex items-center gap-4">
            <div className="p-3 bg-blue-50 rounded text-pg-blue"><Calendar className="w-6 h-6" /></div>
            <div>
              <div className="text-xs text-gray-500 font-medium">This Month</div>
              <div className="text-xl font-bold text-gray-900">{summary.this_month}</div>
            </div>
          </div>
          <div className="bg-white p-4 rounded-xl border border-red-100 shadow-sm flex items-center gap-4 relative">
            <div className="absolute inset-y-0 right-0 w-12 bg-red-50 opacity-50 rounded-r-xl"></div>
            <div className="p-3 bg-red-50 rounded text-red-500"><AlertTriangle className="w-6 h-6" /></div>
            <div>
              <div className="text-xs text-red-500 font-medium">High Risk Transactions</div>
              <div className="text-xl font-bold text-red-600">{summary.high_risk_transactions}</div>
            </div>
          </div>
        </div>
      )}

      {/* Filters Area */}
      <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm space-y-4">
         <div className="grid grid-cols-2 md:grid-cols-6 gap-3">
            <div>
              <label className="block text-xs text-gray-500 mb-1">Date Range</label>
              <select className="w-full text-sm border border-gray-300 rounded p-1.5 focus:ring-1 focus:ring-pg-blue"><option>01 Jan 2024 - 31 Dec 2024</option></select>
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">District</label>
              <select className="w-full text-sm border border-gray-300 rounded p-1.5 focus:ring-1 focus:ring-pg-blue"><option value="">All Districts</option></select>
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Panchayat</label>
              <select className="w-full text-sm border border-gray-300 rounded p-1.5 focus:ring-1 focus:ring-pg-blue" value={panchayatId} onChange={e => setPanchayatId(e.target.value)}>
                 <option value="">All Panchayats</option>
                 {dropdowns.panchayats.map((p: any) => <option key={p.id} value={p.id}>{p.name}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Category</label>
              <select className="w-full text-sm border border-gray-300 rounded p-1.5 focus:ring-1 focus:ring-pg-blue" value={category} onChange={e => setCategory(e.target.value)}>
                 <option value="">All Categories</option>
                 {dropdowns.categories.map((c: string) => <option key={c} value={c}>{c}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Vendor</label>
              <select className="w-full text-sm border border-gray-300 rounded p-1.5 focus:ring-1 focus:ring-pg-blue" value={vendorId} onChange={e => setVendorId(e.target.value)}>
                 <option value="">All Vendors</option>
                 {dropdowns.vendors.map((v: any) => <option key={v.id} value={v.id}>{v.name}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Risk Level</label>
              <select className="w-full text-sm border border-gray-300 rounded p-1.5 focus:ring-1 focus:ring-pg-blue" value={riskLevel} onChange={e => setRiskLevel(e.target.value)}>
                 <option value="">All Levels</option>
                 <option value="High">High</option>
                 <option value="Medium">Medium</option>
                 <option value="Low">Low</option>
              </select>
            </div>
         </div>
         
         <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="relative w-full md:w-96">
               <Search className="absolute left-3 top-1.5 h-4 w-4 text-gray-400" />
               <input 
                 type="text" 
                 placeholder="Search by transaction ID, vendor, panchayat, description..." 
                 className="w-full pl-9 pr-3 py-1.5 text-sm border border-gray-300 rounded focus:ring-1 focus:ring-pg-blue outline-none"
                 value={search}
                 onChange={(e) => setSearch(e.target.value)}
               />
            </div>
            <div className="flex items-center gap-3 w-full md:w-auto">
               <button className="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-gray-600 bg-gray-50 border border-gray-200 rounded hover:bg-gray-100">
                  <Filter className="w-4 h-4" /> More Filters
               </button>
               <button onClick={() => {setSearch(''); setPanchayatId(''); setVendorId(''); setCategory(''); setRiskLevel('');}} className="px-3 py-1.5 text-sm font-medium text-gray-600 bg-gray-50 border border-gray-200 rounded hover:bg-gray-100">
                  Reset
               </button>
               <button onClick={handleExportCSV} className="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-50 ml-auto md:ml-0">
                  <Download className="w-4 h-4" /> Export CSV
               </button>
               <button onClick={() => { setEditingTx(null); setDrawerOpen(true); }} className="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-white bg-pg-blue rounded hover:bg-blue-700 shadow-sm">
                  <Plus className="w-4 h-4" /> Add Transaction
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
                     <th className="px-4 py-3"><input type="checkbox" className="rounded border-gray-300"/></th>
                     <th className="px-4 py-3 font-semibold">Transaction ID</th>
                     <th className="px-4 py-3 font-semibold">Date ?</th>
                     <th className="px-4 py-3 font-semibold">Panchayat</th>
                     <th className="px-4 py-3 font-semibold">Vendor</th>
                     <th className="px-4 py-3 font-semibold">Category</th>
                     <th className="px-4 py-3 font-semibold">Amount</th>
                     <th className="px-4 py-3 font-semibold">Method</th>
                     <th className="px-4 py-3 font-semibold">Risk Score</th>
                     <th className="px-4 py-3 font-semibold">Status</th>
                     <th className="px-4 py-3 font-semibold text-center">Actions</th>
                  </tr>
               </thead>
               <tbody>
                  {loading ? (
                     <tr><td colSpan={11} className="px-4 py-8 text-center text-gray-500">Loading...</td></tr>
                  ) : transactions.length === 0 ? (
                     <tr><td colSpan={11} className="px-4 py-8 text-center text-gray-500">No transactions found.</td></tr>
                  ) : transactions.map(tx => (
                     <tr key={tx.id} className="border-b border-gray-50 hover:bg-gray-50 transition-colors">
                        <td className="px-4 py-3"><input type="checkbox" className="rounded border-gray-300"/></td>
                        <td className="px-4 py-3 font-medium text-gray-900">{tx.transaction_id}</td>
                        <td className="px-4 py-3">{tx.procurement_date ? new Date(tx.procurement_date).toLocaleDateString('en-GB', {day:'2-digit', month:'short', year:'numeric'}) : 'Unknown'}</td>
                        <td className="px-4 py-3">{tx.panchayat_name}</td>
                        <td className="px-4 py-3">{tx.vendor_name}</td>
                        <td className="px-4 py-3">{tx.procurement_category}</td>
                        <td className="px-4 py-3 text-gray-900 font-medium">? {(tx.amount).toLocaleString()}</td>
                        <td className="px-4 py-3">{tx.procurement_method}</td>
                        <td className="px-4 py-3 text-center">
                           <span className={`font-bold ${tx.risk_score >= 80 ? 'text-red-600' : tx.risk_score >= 60 ? 'text-orange-500' : 'text-green-600'}`}>{tx.risk_score}</span>
                        </td>
                        <td className="px-4 py-3">
                           <span className={`px-2.5 py-1 rounded text-xs font-semibold ${tx.risk_level === 'High' ? 'bg-red-100 text-red-700' : tx.risk_level === 'Medium' ? 'bg-orange-100 text-orange-700' : 'bg-green-100 text-green-700'}`}>
                             {tx.risk_level}
                           </span>
                        </td>
                        <td className="px-4 py-3 flex items-center justify-center gap-2">
                           <button onClick={() => { setViewingTxId(tx.id); setDetailsOpen(true); }} className="p-1 text-pg-blue hover:bg-blue-50 rounded"><Eye className="w-4 h-4"/></button>
                           <button onClick={() => { setEditingTx(tx); setDrawerOpen(true); }} className="p-1 text-pg-blue hover:bg-blue-50 rounded"><Edit className="w-4 h-4"/></button>
                           <button onClick={() => handleDelete(tx.id)} className="p-1 text-red-500 hover:bg-red-50 rounded"><Trash2 className="w-4 h-4"/></button>
                        </td>
                     </tr>
                  ))}
               </tbody>
            </table>
         </div>
         
         <div className="p-4 border-t border-gray-200 flex items-center justify-between text-sm text-gray-500">
            <div>Showing {(page-1)*pageSize + 1}-{Math.min(page*pageSize, totalItems)} of {totalItems.toLocaleString()} transactions</div>
            <div className="flex items-center gap-2">
               <button disabled={page === 1} onClick={() => setPage(p => p-1)} className="p-1 border border-gray-200 rounded disabled:opacity-50"><ChevronLeft className="w-4 h-4"/></button>
               <span className="px-2 font-medium text-gray-900">{page}</span>
               <button disabled={page * pageSize >= totalItems} onClick={() => setPage(p => p+1)} className="p-1 border border-gray-200 rounded disabled:opacity-50"><ChevronRight className="w-4 h-4"/></button>
            </div>
         </div>
      </div>

      {drawerOpen && (
         <TransactionDrawer 
           isOpen={drawerOpen} 
           onClose={() => setDrawerOpen(false)} 
           dropdowns={dropdowns}
           editData={editingTx}
           onSuccess={() => { setDrawerOpen(false); fetchTransactions(); fetchSummary(); }}
         />
      )}
      
      {detailsOpen && viewingTxId && (
         <TransactionDetails 
           isOpen={detailsOpen}
           txId={viewingTxId}
           onClose={() => { setDetailsOpen(false); setViewingTxId(null); }}
         />
      )}
    </div>
  );
}

