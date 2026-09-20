import React, { useEffect, useState } from 'react';
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
