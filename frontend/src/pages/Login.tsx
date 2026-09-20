import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useNavigate } from 'react-router-dom';
import { ShieldCheck, Eye, EyeOff } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import api from '../services/api';

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(1, 'Password is required'),
});

type LoginForm = z.infer<typeof loginSchema>;

export default function Login() {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema)
  });
  const [showPassword, setShowPassword] = useState(false);
  const [authError, setAuthError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const onSubmit = async (data: LoginForm) => {
    try {
      setAuthError('');
      const formData = new URLSearchParams();
      formData.append('username', data.email);
      formData.append('password', data.password);
      
      const response = await api.post('/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      
      await login(response.data.access_token);
      navigate('/');
    } catch (error: any) {
      setAuthError(error.response?.data?.detail || 'Authentication failed');
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Left Pane */}
      <div className="hidden lg:flex lg:w-1/2 bg-pg-navy text-white p-12 flex-col justify-between" style={{
        backgroundImage: "linear-gradient(rgba(10, 37, 64, 0.8), rgba(10, 37, 64, 0.95)), url('https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80')",
        backgroundSize: 'cover',
        backgroundPosition: 'center'
      }}>
        <div>
          <div className="flex items-center gap-3 mb-16">
            <div className="bg-white p-2 rounded-lg">
              <ShieldCheck className="w-8 h-8 text-pg-green" />
            </div>
            <div>
              <h1 className="text-2xl font-bold">PanchayatGuard</h1>
              <p className="text-sm text-gray-300">Transparent Panchayat. Stronger Bharat.</p>
            </div>
          </div>
          <h2 className="text-5xl font-light leading-tight mb-4">
            Empowering <br />
            <span className="font-bold">Transparent Governance</span><br />
            Across Rural India
          </h2>
          <div className="flex items-center gap-2 mb-12">
            <div className="h-1 w-12 bg-orange-500 rounded-full"></div>
            <div className="h-1 w-12 bg-white rounded-full"></div>
            <div className="h-1 w-12 bg-green-500 rounded-full"></div>
          </div>
          <p className="text-xl text-gray-300">Monitor. Detect. Prevent. Build Trust.</p>
        </div>
      </div>

      {/* Right Pane */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-pg-light">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8">
          <div className="mb-8">
            <p className="text-gray-500 mb-2">Welcome to</p>
            <h2 className="text-3xl font-bold text-pg-navy mb-2">PanchayatGuard</h2>
            <p className="text-sm text-gray-500">Sign in to access the procurement intelligence platform</p>
          </div>

          {authError && (
            <div className="bg-red-50 text-red-600 p-3 rounded-md mb-6 text-sm border border-red-200">
              {authError}
            </div>
          )}

                              <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
              <input 
                {...register('email')}
                type="email"
                defaultValue="admin@panchayatguard.gov.in"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pg-blue focus:border-pg-blue outline-none"
              />
              {errors.email && <p className="text-red-500 text-xs mt-1">{errors.email.message}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
              <div className="relative">
                <input 
                  {...register('password')}
                  type={showPassword ? 'text' : 'password'}
                  defaultValue="SecurePassword123!"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pg-blue focus:border-pg-blue outline-none"
                />
                <button 
                  type="button" 
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
              {errors.password && <p className="text-red-500 text-xs mt-1">{errors.password.message}</p>}
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" className="rounded text-pg-blue focus:ring-pg-blue" defaultChecked />
                <span className="text-sm text-gray-600">Remember me</span>
              </label>
            </div>

            <button 
              type="submit"
              className="w-full bg-pg-navy text-white py-3 rounded-lg font-bold hover:bg-opacity-90 transition-colors flex items-center justify-center gap-2"
            >
              Sign In to Dashboard
            </button>
            
            <div className="mt-4 pt-4 border-t border-gray-200">
               <p className="text-xs text-center text-gray-500 mb-3 font-semibold uppercase tracking-wider">Hackathon Jury Quick Access</p>
               <div className="grid grid-cols-2 gap-2">
                 <button type="button" onClick={() => onSubmit({email: 'admin@panchayatguard.gov.in', password: 'SecurePassword123!'})} className="text-xs py-2 bg-blue-50 text-pg-blue font-bold rounded border border-blue-100 hover:bg-blue-100 transition-colors">
                   Login as Admin
                 </button>
                 <button type="button" onClick={() => onSubmit({email: 'dm.vikram@gov.in', password: 'SecurePassword123!'})} className="text-xs py-2 bg-green-50 text-green-700 font-bold rounded border border-green-100 hover:bg-green-100 transition-colors">
                   Login as Official
                 </button>
               </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}