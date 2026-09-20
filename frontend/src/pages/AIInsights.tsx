import React, { useEffect, useState } from 'react';
import api from '../services/api';
import TransactionDetails from '../components/TransactionDetails';
import { Brain, Activity, Users, Copy, Share2, Target, AlertTriangle } from 'lucide-react';

export default function AIInsights() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [viewingTxId, setViewingTxId] = useState<number | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await api.get('/ai-insights');
        setData(res.data);
      } catch (e) { console.error(e); } finally { setLoading(false); }
    };
    fetchData();
  }, []);

  if (!data) return <div className="p-8">Loading AI Insights...</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
           <div className="text-sm text-gray-500 mb-1">Dashboard &gt; AI Insights</div>
           <h1 className="text-2xl font-bold text-gray-900">AI Insights</h1>
           <p className="text-sm text-gray-500">Data-driven intelligence to detect anomalies, uncover risks and promote transparent governance.</p>
        </div>
        <div className="text-right text-pg-blue italic text-sm font-medium">
           "From Data to Integrity<br/>Towards a Corruption-Free Tomorrow"
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
         <div className="bg-white p-4 rounded-xl border border-blue-200 shadow-sm">
            <div className="flex items-center gap-2 text-blue-600 mb-2"><Activity className="w-5 h-5 font-bold"/><span className="font-semibold text-sm">Price Anomalies</span></div>
            <div className="text-2xl font-bold text-gray-900">{data.categories['Price Anomalies']}</div>
         </div>
         <div className="bg-white p-4 rounded-xl border border-indigo-200 shadow-sm">
            <div className="flex items-center gap-2 text-indigo-600 mb-2"><Users className="w-5 h-5 font-bold"/><span className="font-semibold text-sm">Vendor Anomalies</span></div>
            <div className="text-2xl font-bold text-gray-900">{data.categories['Vendor Anomalies']}</div>
         </div>
         <div className="bg-white p-4 rounded-xl border border-red-200 shadow-sm">
            <div className="flex items-center gap-2 text-red-600 mb-2"><Copy className="w-5 h-5 font-bold"/><span className="font-semibold text-sm">Duplicate Tx</span></div>
            <div className="text-2xl font-bold text-gray-900">{data.categories['Duplicate Transactions']}</div>
         </div>
         <div className="bg-white p-4 rounded-xl border border-purple-200 shadow-sm">
            <div className="flex items-center gap-2 text-purple-600 mb-2"><Share2 className="w-5 h-5 font-bold"/><span className="font-semibold text-sm">Tx Splitting</span></div>
            <div className="text-2xl font-bold text-gray-900">{data.categories['Transaction Splitting']}</div>
         </div>
         <div className="bg-white p-4 rounded-xl border border-orange-200 shadow-sm">
            <div className="flex items-center gap-2 text-orange-600 mb-2"><Target className="w-5 h-5 font-bold"/><span className="font-semibold text-sm">Concentration Risk</span></div>
            <div className="text-2xl font-bold text-gray-900">{data.categories['Concentration Risks']}</div>
         </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
         <div className="p-5 border-b bg-gray-50 flex justify-between items-center">
            <h3 className="font-bold text-gray-800 flex items-center gap-2"><Brain className="w-5 h-5 text-pg-blue"/> Active AI Insights & Alerts</h3>
         </div>
         <div className="divide-y divide-gray-100">
            {data.insights.map((insight: any) => (
               <div key={insight.id} className="p-5 hover:bg-gray-50 flex gap-4 transition-colors items-center justify-between">
                  <div className="flex gap-4 w-1/3">
                      <div className={`p-3 rounded-xl h-fit ${insight.severity==='Critical'||insight.severity==='CRITICAL' ? 'bg-red-100 text-red-600' : insight.severity==='High'||insight.severity==='HIGH' ? 'bg-orange-100 text-orange-600' : 'bg-yellow-100 text-yellow-600'}`}>
                         <AlertTriangle className="w-6 h-6"/>
                      </div>
                      <div>
                         <h4 className="font-bold text-gray-900">{insight.title}</h4>
                         <p className="text-sm text-gray-600 mt-1">{insight.description}</p>
                         <div className="mt-2 flex gap-2">
                             <span className="text-xs font-semibold px-2 py-1 rounded bg-gray-100 text-gray-600">{insight.category}</span>
                             <span className={`text-xs font-semibold px-2 py-1 rounded ${insight.severity==='Critical'||insight.severity==='CRITICAL'?'bg-red-100 text-red-700':insight.severity==='High'||insight.severity==='HIGH'?'bg-orange-100 text-orange-700':'bg-yellow-100 text-yellow-700'}`}>{insight.severity}</span>
                         </div>
                      </div>
                  </div>
                  
                  <div className="w-1/3 text-sm text-gray-600 space-y-1 border-l pl-4">
                     <div><span className="font-medium text-gray-800">Transaction:</span> <span className="text-pg-blue cursor-pointer hover:underline">{insight.transaction_id}</span></div>
                     <div><span className="font-medium text-gray-800">Vendor:</span> {insight.vendor}</div>
                     <div><span className="font-medium text-gray-800">Panchayat:</span> {insight.panchayat}</div>
                  </div>

                  <div className="w-1/6 text-sm text-gray-500 font-medium">
                     {new Date(insight.date).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })}
                  </div>
                  
                  <div className="w-1/6 text-right">
                     <button onClick={() => setViewingTxId(insight.tx_pk)} className="px-4 py-2 border border-gray-300 rounded text-sm font-semibold text-pg-blue hover:bg-blue-50 transition-colors">View Details</button>
                  </div>
               </div>
            ))}
            {data.insights.length === 0 && <div className="p-8 text-center text-gray-500">No active insights.</div>}
         </div>
      </div>
      {viewingTxId && <TransactionDetails isOpen={true} txId={viewingTxId} onClose={() => setViewingTxId(null)} />}
    </div>
  );
}
