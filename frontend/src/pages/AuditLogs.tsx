import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { ShieldAlert } from 'lucide-react';

export default function AuditLogs() {
  const [logs, setLogs] = useState<any[]>([]);

  useEffect(() => {
    api.get('/audit-logs').then(res => setLogs(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
           <div className="text-sm text-gray-500 mb-1">Dashboard &gt; Audit Logs</div>
           <h1 className="text-2xl font-bold text-gray-900">System Audit Logs</h1>
           <p className="text-sm text-gray-500">Immutable record of all system modifications and user activities.</p>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
         <div className="p-4 border-b bg-gray-50">
            <h3 className="font-bold text-gray-800 flex items-center gap-2"><ShieldAlert className="w-5 h-5 text-pg-navy"/> Recent Activity</h3>
         </div>
         <table className="w-full text-left text-sm">
            <thead className="bg-gray-50 text-gray-600 font-medium border-b">
               <tr>
                  <th className="px-6 py-3">Timestamp</th>
                  <th className="px-6 py-3">User</th>
                  <th className="px-6 py-3">Action</th>
                  <th className="px-6 py-3">Entity Type</th>
                  <th className="px-6 py-3">Entity ID</th>
                  <th className="px-6 py-3">Details</th>
               </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
               {logs.map(log => (
                  <tr key={log.id} className="hover:bg-gray-50">
                     <td className="px-6 py-3 text-gray-600">{new Date(log.timestamp).toLocaleString()}</td>
                     <td className="px-6 py-3 font-semibold text-gray-900">{log.user}</td>
                     <td className="px-6 py-3">
                        <span className={`px-2 py-1 rounded text-xs font-bold ${log.action==='CREATE'?'bg-green-100 text-green-700':log.action==='UPDATE'?'bg-blue-100 text-blue-700':log.action==='DELETE'?'bg-red-100 text-red-700':'bg-gray-100 text-gray-700'}`}>{log.action}</span>
                     </td>
                     <td className="px-6 py-3 text-gray-600">{log.entity_type}</td>
                     <td className="px-6 py-3 text-gray-600 font-mono text-xs">{log.entity_id}</td>
                     <td className="px-6 py-3 text-gray-600 max-w-sm truncate" title={log.details}>{log.details}</td>
                  </tr>
               ))}
            </tbody>
         </table>
      </div>
    </div>
  );
}
