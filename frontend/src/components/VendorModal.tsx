import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import api from '../services/api';
import { X } from 'lucide-react';

const vendorSchema = z.object({
  vendor_name: z.string().min(2, 'Name is required'),
  category: z.string().min(1, 'Category is required'),
  contact_email: z.string().email().optional().or(z.literal('')),
  contact_phone: z.string().optional().or(z.literal('')),
});

type VendorForm = z.infer<typeof vendorSchema>;

interface VendorModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export default function VendorModal({ isOpen, onClose, onSuccess }: VendorModalProps) {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<VendorForm>({
    resolver: zodResolver(vendorSchema) as any
  });
  const [errorMsg, setErrorMsg] = useState('');

  if (!isOpen) return null;

  const onSubmit = async (data: VendorForm) => {
    setErrorMsg('');
    try {
      await api.post('/vendors', data);
      onSuccess();
    } catch (e: any) {
      setErrorMsg(e.response?.data?.detail || 'Failed to add vendor');
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden">
        <div className="flex justify-between items-center p-4 border-b">
          <h2 className="text-lg font-bold">Add Vendor</h2>
          <button onClick={onClose} className="p-1 hover:bg-gray-100 rounded"><X className="w-5 h-5"/></button>
        </div>
        <form onSubmit={handleSubmit(onSubmit as any)} className="p-4 space-y-4">
          {errorMsg && <div className="text-red-500 text-sm bg-red-50 p-2 rounded">{errorMsg}</div>}
          
          <div>
            <label className="block text-sm font-medium mb-1">Vendor Name *</label>
            <input {...register('vendor_name')} className="w-full p-2 border rounded focus:ring-1 focus:ring-pg-blue" />
            {errors.vendor_name && <p className="text-red-500 text-xs mt-1">{errors.vendor_name.message}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Category *</label>
            <select {...register('category')} className="w-full p-2 border rounded focus:ring-1 focus:ring-pg-blue">
              <option value="">Select Category</option>
              <option value="Construction">Construction</option>
              <option value="IT Services">IT Services</option>
              <option value="Stationery">Stationery</option>
              <option value="Consulting">Consulting</option>
              <option value="Maintenance">Maintenance</option>
            </select>
            {errors.category && <p className="text-red-500 text-xs mt-1">{errors.category.message}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <input {...register('contact_email')} type="email" className="w-full p-2 border rounded focus:ring-1 focus:ring-pg-blue" />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Phone</label>
            <input {...register('contact_phone')} className="w-full p-2 border rounded focus:ring-1 focus:ring-pg-blue" />
          </div>

          <div className="flex justify-end gap-3 mt-6">
            <button type="button" onClick={onClose} className="px-4 py-2 border rounded text-gray-700 hover:bg-gray-50">Cancel</button>
            <button type="submit" disabled={isSubmitting} className="px-4 py-2 bg-pg-blue text-white rounded hover:bg-blue-700 disabled:opacity-50">
              {isSubmitting ? 'Saving...' : 'Save Vendor'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
