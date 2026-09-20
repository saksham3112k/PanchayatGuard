import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShieldCheck, ArrowLeft, Home } from 'lucide-react';

export default function NotFound() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 px-4">
       <div className="bg-pg-navy p-4 rounded-full mb-6">
          <ShieldCheck className="w-16 h-16 text-pg-green" />
       </div>
       <h1 className="text-6xl font-extrabold text-pg-navy mb-2">404</h1>
       <h2 className="text-2xl font-bold text-gray-900 mb-4">Page not found</h2>
       <p className="text-gray-600 mb-8 max-w-md text-center">
          The page you are looking for doesn't exist or has been moved. Please check the URL or navigate back to the dashboard.
       </p>
       <div className="flex gap-4 w-full max-w-xs">
          <button onClick={() => navigate(-1)} className="flex-1 flex justify-center items-center gap-2 py-2.5 px-4 border border-gray-300 rounded-lg text-sm font-semibold text-gray-700 hover:bg-gray-100 transition-colors">
             <ArrowLeft className="w-4 h-4" /> Go Back
          </button>
          <Link to="/" className="flex-1 flex justify-center items-center gap-2 py-2.5 px-4 bg-pg-blue rounded-lg text-sm font-bold text-white hover:bg-blue-700 shadow transition-colors">
             <Home className="w-4 h-4" /> Dashboard
          </Link>
       </div>
    </div>
  );
}
