import os

frontend_dir = r"c:\Users\Dell\OneDrive\Desktop\PANCHAYATGUARD\panchayatguard\frontend\src"

# 1. Update App.tsx
app_tsx_path = os.path.join(frontend_dir, "App.tsx")
with open(app_tsx_path, "r", encoding="utf-8") as f:
    app_tsx = f.read()

app_tsx = app_tsx.replace(
    "import Dashboard from './pages/Dashboard';", 
    "import Dashboard from './pages/Dashboard';\nimport Procurement from './pages/Procurement';"
)
app_tsx = app_tsx.replace(
    "<Route path=\"/procurement\" element={<Placeholder />} />",
    "<Route path=\"/procurement\" element={<Procurement />} />"
)

with open(app_tsx_path, "w", encoding="utf-8") as f:
    f.write(app_tsx)


# 2. Procurement.tsx
procurement_tsx_path = os.path.join(frontend_dir, "pages", "Procurement.tsx")
with open(procurement_tsx_path, "w", encoding="utf-8") as f:
    f.write("""import React, { useState, useEffect } from 'react';
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
    if (val >= 10000000) return `₹ ${(val / 10000000).toFixed(2)} Cr`;
    if (val >= 100000) return `₹ ${(val / 100000).toFixed(2)} L`;
    return `₹ ${val.toLocaleString()}`;
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
           <div className="text-sm text-gray-500 mb-1">Dashboard > Procurement</div>
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
            <div className="p-3 bg-blue-50 rounded text-pg-blue"><span className="text-xl font-bold">₹</span></div>
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
                     <th className="px-4 py-3 font-semibold">Date ↓</th>
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
                        <td className="px-4 py-3">{new Date(tx.procurement_date).toLocaleDateString('en-GB', {day:'2-digit', month:'short', year:'numeric'})}</td>
                        <td className="px-4 py-3">{tx.panchayat_name}</td>
                        <td className="px-4 py-3">{tx.vendor_name}</td>
                        <td className="px-4 py-3">{tx.procurement_category}</td>
                        <td className="px-4 py-3 text-gray-900 font-medium">₹ {(tx.amount).toLocaleString()}</td>
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
""")

# 3. TransactionDrawer.tsx
drawer_tsx_path = os.path.join(frontend_dir, "components", "TransactionDrawer.tsx")
if not os.path.exists(os.path.dirname(drawer_tsx_path)): os.makedirs(os.path.dirname(drawer_tsx_path))

with open(drawer_tsx_path, "w", encoding="utf-8") as f:
    f.write("""import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { X, Save } from 'lucide-react';
import api from '../services/api';

const schema = z.object({
  transaction_id: z.string().min(3, "Transaction ID is required"),
  panchayat_id: z.coerce.number().min(1, "Select a Panchayat"),
  vendor_id: z.coerce.number().min(1, "Select a Vendor"),
  procurement_category: z.string().min(1, "Select Category"),
  description: z.string().min(5, "Description required"),
  amount: z.coerce.number().min(1, "Amount must be positive"),
  quantity: z.coerce.number().min(1, "Quantity must be positive"),
  unit_price: z.coerce.number().min(1, "Unit Price must be positive"),
  procurement_date: z.string().min(1, "Date required"),
  invoice_number: z.string().min(1, "Invoice Number required"),
  tender_number: z.string().optional(),
  procurement_method: z.string().min(1, "Method required"),
  payment_status: z.string().min(1, "Payment Status required"),
});

type FormValues = z.infer<typeof schema>;

export default function TransactionDrawer({ isOpen, onClose, dropdowns, editData, onSuccess }: any) {
  const { register, handleSubmit, formState: { errors }, reset, watch, setValue } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: editData ? {
      ...editData,
      procurement_date: new Date(editData.procurement_date).toISOString().split('T')[0]
    } : {
      amount: 0, quantity: 1, unit_price: 0
    }
  });

  const qty = watch('quantity') || 0;
  const price = watch('unit_price') || 0;
  
  useEffect(() => {
    setValue('amount', qty * price);
  }, [qty, price, setValue]);

  const onSubmit = async (data: FormValues) => {
    try {
      const payload = { ...data, procurement_date: new Date(data.procurement_date).toISOString() };
      if (editData) {
        await api.put(`/procurement/transactions/${editData.id}`, payload);
        alert('Transaction updated successfully');
      } else {
        await api.post('/procurement/transactions', payload);
        alert('Transaction created successfully. Risk and vendor statistics updated.');
      }
      onSuccess();
    } catch (e: any) {
      alert(e.response?.data?.detail || 'Error saving transaction');
    }
  };

  return (
    <>
      <div className="fixed inset-0 bg-black/30 z-40" onClick={onClose}></div>
      <div className="fixed top-0 right-0 h-full w-full max-w-md bg-white shadow-xl z-50 flex flex-col transform transition-transform overflow-hidden">
        <div className="p-4 border-b flex justify-between items-center bg-gray-50">
          <h2 className="text-lg font-bold text-gray-800">{editData ? 'Edit Transaction' : 'Add New Procurement Transaction'}</h2>
          <button onClick={onClose} className="p-1 text-gray-500 hover:bg-gray-200 rounded"><X className="w-5 h-5"/></button>
        </div>
        
        <div className="flex-1 overflow-y-auto p-5">
          <form id="tx-form" onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            
            <div>
              <h3 className="font-semibold text-gray-800 border-b pb-2 mb-4 text-sm uppercase tracking-wide">Basic Information</h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">Transaction ID *</label>
                  <input {...register('transaction_id')} disabled={!!editData} className="w-full text-sm border rounded p-2 focus:ring-1 focus:ring-pg-blue" />
                  {errors.transaction_id && <span className="text-xs text-red-500">{errors.transaction_id.message}</span>}
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">Procurement Date *</label>
                  <input type="date" {...register('procurement_date')} className="w-full text-sm border rounded p-2 focus:ring-1 focus:ring-pg-blue" />
                  {errors.procurement_date && <span className="text-xs text-red-500">{errors.procurement_date.message}</span>}
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">Panchayat *</label>
                  <select {...register('panchayat_id')} className="w-full text-sm border rounded p-2 focus:ring-1 focus:ring-pg-blue">
                    <option value="">Select Panchayat</option>
                    {dropdowns.panchayats.map((p:any) => <option key={p.id} value={p.id}>{p.name}</option>)}
                  </select>
                  {errors.panchayat_id && <span className="text-xs text-red-500">{errors.panchayat_id.message}</span>}
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">Vendor *</label>
                  <select {...register('vendor_id')} className="w-full text-sm border rounded p-2 focus:ring-1 focus:ring-pg-blue">
                    <option value="">Select Vendor</option>
                    {dropdowns.vendors.map((v:any) => <option key={v.id} value={v.id}>{v.name}</option>)}
                  </select>
                  {errors.vendor_id && <span className="text-xs text-red-500">{errors.vendor_id.message}</span>}
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">Category *</label>
                  <select {...register('procurement_category')} className="w-full text-sm border rounded p-2 focus:ring-1 focus:ring-pg-blue">
                    <option value="">Select Category</option>
                    {dropdowns.categories.map((c:string) => <option key={c} value={c}>{c}</option>)}
                  </select>
                  {errors.procurement_category && <span className="text-xs text-red-500">{errors.procurement_category.message}</span>}
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">Procurement Method *</label>
                  <select {...register('procurement_method')} className="w-full text-sm border rounded p-2 focus:ring-1 focus:ring-pg-blue">
                    <option value="">Select Method</option>
                    <option value="Tender">Tender</option>
                    <option value="Direct Purchase">Direct Purchase</option>
                    <option value="Quotation">Quotation</option>
                  </select>
                  {errors.procurement_method && <span className="text-xs text-red-500">{errors.procurement_method.message}</span>}
                </div>
                <div className="col-span-2">
                  <label className="block text-xs font-medium text-gray-700 mb-1">Description *</label>
                  <textarea {...register('description')} rows={3} className="w-full text-sm border rounded p-2 focus:ring-1 focus:ring-pg-blue" placeholder="Enter procurement description..."></textarea>
                  {errors.description && <span className="text-xs text-red-500">{errors.description.message}</span>}
                </div>
              </div>
            </div>

            <div>
              <h3 className="font-semibold text-gray-800 border-b pb-2 mb-4 text-sm uppercase tracking-wide">Financial Details</h3>
              <div className="grid grid-cols-3 gap-4 mb-4">
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">Quantity *</label>
                  <input type="number" {...register('quantity')} className="w-full text-sm border rounded p-2 focus:ring-1 focus:ring-pg-blue" />
                  {errors.quantity && <span className="text-xs text-red-500">{errors.quantity.message}</span>}
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">Unit Price (₹) *</label>
                  <input type="number" step="0.01" {...register('unit_price')} className="w-full text-sm border rounded p-2 focus:ring-1 focus:ring-pg-blue" />
                  {errors.unit_price && <span className="text-xs text-red-500">{errors.unit_price.message}</span>}
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">Total Amount (₹) *</label>
                  <input type="number" step="0.01" readOnly {...register('amount')} className="w-full text-sm border rounded p-2 bg-gray-50 focus:outline-none text-gray-600 font-bold" />
                  {errors.amount && <span className="text-xs text-red-500">{errors.amount.message}</span>}
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">Invoice Number *</label>
                  <input {...register('invoice_number')} className="w-full text-sm border rounded p-2 focus:ring-1 focus:ring-pg-blue" placeholder="Enter invoice number" />
                  {errors.invoice_number && <span className="text-xs text-red-500">{errors.invoice_number.message}</span>}
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">Tender Number</label>
                  <input {...register('tender_number')} className="w-full text-sm border rounded p-2 focus:ring-1 focus:ring-pg-blue" placeholder="Enter tender number" />
                </div>
                <div className="col-span-2">
                  <label className="block text-xs font-medium text-gray-700 mb-1">Payment Status *</label>
                  <select {...register('payment_status')} className="w-full text-sm border rounded p-2 focus:ring-1 focus:ring-pg-blue">
                    <option value="">Select Status</option>
                    <option value="Paid">Paid</option>
                    <option value="Pending">Pending</option>
                    <option value="Processing">Processing</option>
                  </select>
                  {errors.payment_status && <span className="text-xs text-red-500">{errors.payment_status.message}</span>}
                </div>
              </div>
            </div>

          </form>
        </div>
        
        <div className="p-4 border-t bg-gray-50 flex justify-end gap-3">
          <button onClick={onClose} className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-50">Cancel</button>
          <button form="tx-form" type="submit" className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-pg-navy rounded hover:bg-blue-900 shadow">
            <Save className="w-4 h-4"/> Save Transaction
          </button>
        </div>
      </div>
    </>
  );
}
""")

# 4. TransactionDetails.tsx
details_tsx_path = os.path.join(frontend_dir, "components", "TransactionDetails.tsx")
with open(details_tsx_path, "w", encoding="utf-8") as f:
    f.write("""import React, { useEffect, useState } from 'react';
import { X, CheckCircle, AlertTriangle, Info, MapPin, Receipt, Calendar, User } from 'lucide-react';
import api from '../services/api';

export default function TransactionDetails({ isOpen, txId, onClose }: any) {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDetails = async () => {
      try {
        const res = await api.get(`/procurement/transactions/${txId}`);
        setData(res.data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    if (txId) fetchDetails();
  }, [txId]);

  if (!isOpen) return null;

  return (
    <>
      <div className="fixed inset-0 bg-black/40 z-40" onClick={onClose}></div>
      <div className="fixed inset-0 m-auto w-full max-w-4xl h-[90vh] bg-gray-50 rounded-xl shadow-2xl z-50 flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        
        {loading ? (
          <div className="flex items-center justify-center h-full">Loading...</div>
        ) : !data ? (
          <div className="flex items-center justify-center h-full text-red-500">Failed to load details</div>
        ) : (
          <>
            <div className="p-6 bg-white border-b flex justify-between items-start shrink-0">
              <div>
                <div className="flex items-center gap-3 mb-1">
                  <h2 className="text-2xl font-bold text-gray-900">{data.transaction_id}</h2>
                  <span className={`px-2.5 py-1 text-xs font-semibold rounded-full ${data.payment_status === 'Paid' ? 'bg-green-100 text-green-700' : 'bg-orange-100 text-orange-700'}`}>
                    {data.payment_status}
                  </span>
                </div>
                <p className="text-sm text-gray-500">{data.description}</p>
              </div>
              <button onClick={onClose} className="p-1.5 text-gray-500 hover:bg-gray-100 rounded-full transition-colors"><X className="w-5 h-5"/></button>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-6">
              
              {/* Top Summary Cards */}
              <div className="grid grid-cols-4 gap-4">
                <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
                  <div className="text-xs text-gray-500 font-medium mb-1">Total Amount</div>
                  <div className="text-xl font-bold text-gray-900">₹ {data.amount.toLocaleString()}</div>
                </div>
                <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
                  <div className="text-xs text-gray-500 font-medium mb-1">Risk Score</div>
                  <div className={`text-xl font-bold ${data.risk_score >= 80 ? 'text-red-600' : data.risk_score >= 60 ? 'text-orange-500' : 'text-green-600'}`}>
                    {data.risk_score} / 100
                  </div>
                </div>
                <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
                  <div className="text-xs text-gray-500 font-medium mb-1">Date</div>
                  <div className="text-xl font-bold text-gray-900">{new Date(data.procurement_date).toLocaleDateString()}</div>
                </div>
                <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
                  <div className="text-xs text-gray-500 font-medium mb-1">Method</div>
                  <div className="text-xl font-bold text-gray-900">{data.procurement_method}</div>
                </div>
              </div>

              {/* Two Column Layout for Details */}
              <div className="grid grid-cols-3 gap-6">
                
                {/* Left Col: Info */}
                <div className="col-span-2 space-y-6">
                  
                  <div className="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden">
                    <div className="bg-gray-50 px-4 py-3 border-b font-semibold text-gray-700 flex items-center gap-2">
                      <Receipt className="w-4 h-4"/> Transaction Details
                    </div>
                    <div className="p-4 grid grid-cols-2 gap-y-4 gap-x-8">
                      <div><div className="text-xs text-gray-500">Category</div><div className="font-medium text-gray-900">{data.procurement_category}</div></div>
                      <div><div className="text-xs text-gray-500">Invoice Number</div><div className="font-medium text-gray-900">{data.invoice_number}</div></div>
                      <div><div className="text-xs text-gray-500">Quantity</div><div className="font-medium text-gray-900">{data.quantity}</div></div>
                      <div><div className="text-xs text-gray-500">Unit Price</div><div className="font-medium text-gray-900">₹ {data.unit_price.toLocaleString()}</div></div>
                      {data.tender_number && (
                         <div className="col-span-2"><div className="text-xs text-gray-500">Tender Reference</div><div className="font-medium text-gray-900">{data.tender_number}</div></div>
                      )}
                    </div>
                  </div>

                  <div className="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden">
                    <div className="bg-gray-50 px-4 py-3 border-b font-semibold text-gray-700 flex items-center gap-2">
                      <MapPin className="w-4 h-4"/> Involved Entities
                    </div>
                    <div className="p-4 grid grid-cols-2 gap-4">
                      <div className="border rounded p-3 bg-gray-50/50">
                        <div className="text-xs text-gray-500 mb-1">Panchayat</div>
                        <div className="font-bold text-pg-blue">{data.panchayat_name}</div>
                      </div>
                      <div className="border rounded p-3 bg-gray-50/50">
                        <div className="text-xs text-gray-500 mb-1">Vendor</div>
                        <div className="font-bold text-pg-blue">{data.vendor_name}</div>
                      </div>
                    </div>
                  </div>

                </div>

                {/* Right Col: Alerts & Audit */}
                <div className="col-span-1 space-y-6">
                  
                  <div className="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden">
                    <div className="bg-gray-50 px-4 py-3 border-b font-semibold text-gray-700 flex items-center gap-2">
                      <AlertTriangle className="w-4 h-4"/> Risk & Alerts
                    </div>
                    <div className="p-4 space-y-3">
                      {data.alerts && data.alerts.length > 0 ? (
                        data.alerts.map((a: any, i: number) => (
                          <div key={i} className={`p-3 rounded border text-sm ${a.severity === 'High' ? 'bg-red-50 border-red-200' : 'bg-orange-50 border-orange-200'}`}>
                            <div className="font-bold mb-1 flex items-center gap-1">
                              <AlertTriangle className={`w-4 h-4 ${a.severity === 'High' ? 'text-red-500' : 'text-orange-500'}`}/>
                              {a.type}
                            </div>
                            <div className="text-gray-700 text-xs">{a.description}</div>
                            <div className="text-[10px] text-gray-400 mt-2">{new Date(a.date).toLocaleString()}</div>
                          </div>
                        ))
                      ) : (
                        <div className="text-sm text-green-600 flex items-center gap-2 bg-green-50 p-3 rounded border border-green-200">
                          <CheckCircle className="w-5 h-5"/> No risk alerts active.
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden">
                    <div className="bg-gray-50 px-4 py-3 border-b font-semibold text-gray-700 flex items-center gap-2">
                      <Info className="w-4 h-4"/> Audit History
                    </div>
                    <div className="p-4 space-y-4">
                      {data.audit_history && data.audit_history.length > 0 ? (
                         <div className="relative border-l-2 border-gray-200 ml-2 space-y-4 pl-4">
                            {data.audit_history.map((log: any, i: number) => (
                              <div key={i} className="relative">
                                <div className="absolute -left-[21px] top-1 w-2.5 h-2.5 bg-gray-300 rounded-full border-2 border-white"></div>
                                <div className="text-xs font-bold text-gray-800">{log.action}</div>
                                <div className="text-xs text-gray-500">{log.details}</div>
                                <div className="text-[10px] text-gray-400 mt-0.5">{new Date(log.date).toLocaleString()}</div>
                              </div>
                            ))}
                         </div>
                      ) : (
                         <div className="text-sm text-gray-500">No audit logs found.</div>
                      )}
                    </div>
                  </div>

                </div>
              </div>

            </div>
          </>
        )}
      </div>
    </>
  );
}
""")

print("Phase 3 Frontend components generated successfully!")
