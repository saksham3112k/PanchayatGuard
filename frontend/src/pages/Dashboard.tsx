import React, { useEffect, useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import api from '../services/api';
import { IndianRupee, ShieldAlert, BarChart3, AlertTriangle, Lightbulb } from 'lucide-react';
import { BarChart as RechartsBarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
  const { user } = useAuth();
  const [summary, setSummary] = useState<any>(null);
  const [flagged, setFlagged] = useState<any[]>([]);
  const [insights, setInsights] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.get('/dashboard/summary'),
      api.get('/dashboard/flagged-transactions'),
      api.get('/dashboard/insights')
    ]).then(([sumRes, flagRes, insRes]) => {
      setSummary(sumRes.data);
      setFlagged(flagRes.data);
      setInsights(insRes.data);
      setLoading(false);
    }).catch(e => {
      console.error(e);
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="p-6">Loading dashboard...</div>;
  if (!summary) return <div className="p-6 text-red-500">Failed to load dashboard data.</div>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Welcome back, {user?.name}</h1>
        <p className="text-gray-500">Monitor procurement activities, detect anomalies and ensure transparent governance across all Gram Panchayats.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex items-start justify-between">
          <div>
            <p className="text-sm font-semibold text-gray-500 mb-1">Total Procurement</p>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">₹{((summary.total_procurement || 0) / 10000000).toFixed(2)} Cr</h2>
            <p className="text-sm text-green-600 font-medium">{summary.procurement_change} from last month</p>
          </div>
          <div className="p-3 bg-blue-50 text-blue-600 rounded-lg"><IndianRupee className="w-6 h-6" /></div>
        </div>
        
        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex items-start justify-between">
          <div>
            <p className="text-sm font-semibold text-gray-500 mb-1">Transactions Analyzed</p>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">{(summary.transactions_analyzed || 0).toLocaleString()}</h2>
            <p className="text-sm text-green-600 font-medium">Real-time monitoring active</p>
          </div>
          <div className="p-3 bg-green-50 text-green-600 rounded-lg"><BarChart3 className="w-6 h-6" /></div>
        </div>

        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex items-start justify-between">
          <div>
            <p className="text-sm font-semibold text-gray-500 mb-1">High-Risk Alerts</p>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">{summary.high_risk_alerts || 0}</h2>
            <p className="text-sm text-red-600 font-medium">Requires immediate attention</p>
          </div>
          <div className="p-3 bg-red-50 text-red-600 rounded-lg"><ShieldAlert className="w-6 h-6" /></div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <h3 className="text-lg font-bold text-gray-900 mb-6">Recent Insights</h3>
          <div className="space-y-4">
            {insights.map((insight: any, idx: number) => (
              <div key={idx} className="flex items-start gap-3 p-3 rounded-lg border border-gray-100 bg-gray-50">
                <Lightbulb className="w-5 h-5 text-pg-blue mt-0.5" />
                <p className="text-sm text-gray-700">{insight.text}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <h3 className="text-lg font-bold text-gray-900 mb-6">Flagged Transactions</h3>
          <div className="space-y-4">
            {flagged.map((alert: any) => (
              <div key={alert.id} className="flex items-start gap-4 p-4 rounded-lg bg-red-50 border border-red-100">
                <AlertTriangle className="w-5 h-5 text-red-600 mt-0.5" />
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-bold text-gray-900">{alert.panchayat_name}</span>
                    <span className="text-xs px-2 py-0.5 rounded-full bg-red-100 text-red-800 font-bold border border-red-200">{alert.severity}</span>
                  </div>
                  <p className="text-sm text-gray-700 mb-2">{alert.description}</p>
                  <p className="text-xs text-gray-500 font-medium">{alert.date} • ₹{(alert.amount || 0).toLocaleString()}</p>
                </div>
              </div>
            ))}
            {flagged.length === 0 && <p className="text-sm text-gray-500">No critical alerts found.</p>}
          </div>
        </div>
      </div>
    </div>
  );
}
