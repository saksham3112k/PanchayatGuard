import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import VendorModal from '../components/VendorModal';
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
  const [isModalOpen, setIsModalOpen] = useState(false);

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
           <div className="text-sm text-gray-500 mb-1">Dashboard &gt; Vendors</div>
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
               <button onClick={() => setIsModalOpen(true)} className="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-white bg-pg-blue rounded hover:bg-blue-700 shadow-sm">
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
      <VendorModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} onSuccess={() => { setIsModalOpen(false); fetchVendors(); }} />
    </div>
  );
}
