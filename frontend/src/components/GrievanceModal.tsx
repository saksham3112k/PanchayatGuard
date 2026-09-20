import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import api from '../services/api';
import { X } from 'lucide-react';

interface GrievanceModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  editData?: any;
}

export default function GrievanceModal({ isOpen, onClose, onSuccess, editData }: GrievanceModalProps) {
  const { register, handleSubmit, reset } = useForm();
  const [errorMsg, setErrorMsg] = useState('');
  const [panchayats, setPanchayats] = useState<any[]>([]);

  useEffect(() => {
    if (isOpen) {
      api.get('/procurement/dropdowns').then(res => setPanchayats(res.data.panchayats)).catch(console.error);
      if (editData) {
        reset({ status: editData.status });
      } else {
        reset({});
      }
    }
  }, [isOpen, editData, reset]);

  if (!isOpen) return null;

  const onSubmit = async (data: any) => {
    setErrorMsg('');
    try {
      if (editData) {
        await api.put(`/grievances/${editData.id}`, { status: data.status });
      } else {
        data.grievance_id = `GRV-${Math.floor(1000 + Math.random() * 9000)}`;
        data.panchayat_id = parseInt(data.panchayat_id);
        await api.post('/grievances/', data);
      }
      onSuccess();
    } catch (e: any) {
      setErrorMsg(e.response?.data?.detail || 'Failed to save grievance');
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden">
        <div className="flex justify-between items-center p-4 border-b">
          <h2 className="text-lg font-bold">{editData ? 'Update Grievance' : 'New Grievance'}</h2>
          <button onClick={onClose} className="p-1 hover:bg-gray-100 rounded"><X className="w-5 h-5"/></button>
        </div>
        <form onSubmit={handleSubmit(onSubmit)} className="p-4 space-y-4">
          {errorMsg && <div className="text-red-500 text-sm bg-red-50 p-2 rounded">{errorMsg}</div>}
          
          {editData ? (
            <div>
              <label className="block text-sm font-medium mb-1">Status</label>
              <select {...register('status')} className="w-full p-2 border rounded">
                <option value="Open">Open</option>
                <option value="Under Review">Under Review</option>
                <option value="Resolved">Resolved</option>
                <option value="Rejected">Rejected</option>
              </select>
            </div>
          ) : (
                          <>
                <div>
                  <label className="block text-sm font-medium mb-1 text-gray-700">Subject</label>
                  <input required {...register('subject')} placeholder='e.g. Payment Delay for Solar Panels' className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-pg-blue outline-none" />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1 text-gray-700">Description</label>
                  <textarea required {...register('description')} placeholder='Provide detailed explanation...' className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-pg-blue outline-none" rows={3}></textarea>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1 text-gray-700">Panchayat</label>
                  <select required {...register('panchayat_id')} className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-pg-blue outline-none">
                    <option value="">-- Select Panchayat --</option>
                    {panchayats.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
                  </select>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1 text-gray-700">Category</label>
                    <select required {...register('category')} className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-pg-blue outline-none">
                      <option value="Corruption">Corruption</option>
                      <option value="Delay">Delay</option>
                      <option value="Quality Issue">Quality Issue</option>
                      <option value="Missing Goods">Missing Goods</option>
                      <option value="Overpricing">Overpricing</option>
                      <option value="Contract Violation">Contract Violation</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1 text-gray-700">Priority</label>
                    <select required {...register('priority')} className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-pg-blue outline-none">
                      <option value="Low">Low</option>
                      <option value="Medium">Medium</option>
                      <option value="High">High</option>
                      <option value="Critical">Critical</option>
                    </select>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1 text-gray-700">Submitted By</label>
                  <input required {...register('submitted_by')} placeholder='Your Email or Name' className="w-full p-2 border border-gray-300 rounded focus:ring-1 focus:ring-pg-blue outline-none" />
                </div>
              </>
          )}

          <div className="flex justify-end gap-3 mt-6">
            <button type="button" onClick={onClose} className="px-4 py-2 border rounded hover:bg-gray-50">Cancel</button>
            <button type="submit" className="px-4 py-2 bg-pg-blue text-white rounded hover:bg-blue-700">
              {editData ? 'Update' : 'Submit'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
