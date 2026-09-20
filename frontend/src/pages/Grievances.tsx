import React, { useEffect, useState } from 'react';
import api from '../services/api';
import GrievanceModal from '../components/GrievanceModal';
import { MessageSquare, Plus, Search, Filter } from 'lucide-react';

export default function Grievances() {
  const [grievances, setGrievances] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editData, setEditData] = useState<any>(null);
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('All');

  const fetchGrievances = async () => {
     setLoading(true);
     setError(null);
     try {
       const params = new URLSearchParams();
       if (search) params.append('search', search);
       if (status) params.append('status', status);
       const res = await api.get(`/grievances/?${params.toString()}`);
       setGrievances(res.data);
     } catch (e: any) { 
       console.error(e); 
       setError(e.message);
     } finally { 
       setLoading(false); 
     }
  };

  useEffect(() => {
    fetchGrievances();
  }, [status]); 

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
           <div className="text-sm text-gray-500 mb-1">Dashboard &gt; Grievances</div>
           <h1 className="text-2xl font-bold text-gray-900">Grievance Redressal</h1>
           <p className="text-sm text-gray-500">Manage and track public and internal grievances related to procurement.</p>
        </div>
        <button onClick={() => { setEditData(null); setIsModalOpen(true); }} className="bg-pg-blue text-white px-4 py-2 rounded font-bold flex items-center gap-2 hover:bg-blue-700 transition-colors">
            <Plus className="w-4 h-4"/> New Grievance
          </button>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
         <div className="p-4 border-b flex justify-between items-center bg-gray-50">
            <div className="flex gap-4 w-1/2">
               <div className="relative flex-1">
                  <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"/>
                  <input type="text" placeholder="Search ID or subject..." className="w-full pl-9 pr-4 py-2 text-sm border rounded bg-white focus:ring-1 focus:ring-pg-blue" value={search} onChange={e=>setSearch(e.target.value)} onKeyDown={e=>e.key==='Enter' && fetchGrievances()}/>
               </div>
               <select className="border rounded text-sm px-3 py-2 bg-white" value={status} onChange={e=>setStatus(e.target.value)}>
                  <option>All</option>
                  <option>Open</option>
                  <option>Under Review</option>
                  <option>Resolved</option>
                  <option>Rejected</option>
               </select>
            </div>
         </div>
         {error && <div className="p-4 bg-red-50 text-red-600 border-b border-red-200">Error: {error}</div>}
         <table className="w-full text-left text-sm">
            <thead className="bg-gray-50 text-gray-600 font-medium border-b">
               <tr>
                  <th className="px-6 py-3">ID</th>
                  <th className="px-6 py-3">Subject</th>
                  <th className="px-6 py-3">Panchayat</th>
                  <th className="px-6 py-3">Submitted By</th>
                  <th className="px-6 py-3">Date</th>
                  <th className="px-6 py-3">Priority</th>
                  <th className="px-6 py-3">Status</th>
                  <th className="px-6 py-3">Actions</th>
               </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
               {loading ? <tr><td colSpan={8} className="p-8 text-center text-gray-500">Loading...</td></tr> : 
                grievances.length === 0 ? <tr><td colSpan={8} className="p-8 text-center text-gray-500">No grievances found.</td></tr> :
                grievances.map(g => (
                  <tr key={g.id} className="hover:bg-gray-50">
                     <td className="px-6 py-4 font-bold text-pg-blue">{g.grievance_id}</td>
                     <td className="px-6 py-4 text-gray-900 font-medium max-w-xs truncate" title={g.description}>{g.subject}</td>
                     <td className="px-6 py-4 text-gray-600">{g.panchayat_name}</td>
                     <td className="px-6 py-4 text-gray-600">{g.submitted_by}</td>
                     <td className="px-6 py-4 text-gray-600">{g.date ? new Date(g.date).toLocaleDateString() : 'Unknown'}</td>
                     <td className="px-6 py-4">
                        <span className={`px-2 py-1 rounded text-xs font-bold ${g.priority==='High' || g.priority==='Critical'?'bg-red-100 text-red-700':g.priority==='Medium'?'bg-orange-100 text-orange-700':'bg-green-100 text-green-700'}`}>{g.priority}</span>
                     </td>
                     <td className="px-6 py-4">
                        <span className={`px-2 py-1 rounded-full border text-xs font-bold ${g.status==='Open'?'bg-red-50 text-red-600 border-red-200':g.status==='Under Review'?'bg-yellow-50 text-yellow-600 border-yellow-200':g.status==='Resolved'?'bg-green-50 text-green-600 border-green-200':'bg-gray-100 text-gray-600 border-gray-300'}`}>{g.status}</span>
                     </td>
                     <td className="px-6 py-4">
                        <button onClick={() => { setEditData(g); setIsModalOpen(true); }} className="text-pg-blue font-semibold hover:underline">Update</button>
                     </td>
                  </tr>
               ))}
            </tbody>
         </table>
      </div>
      <GrievanceModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} editData={editData} onSuccess={() => { setIsModalOpen(false); fetchGrievances(); }} />
    </div>
  );
}
