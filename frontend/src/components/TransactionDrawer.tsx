import React, { useEffect } from 'react';
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
    resolver: zodResolver(schema) as any,
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
          <form id="tx-form" onSubmit={handleSubmit(onSubmit as any)} className="space-y-6">
            
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
