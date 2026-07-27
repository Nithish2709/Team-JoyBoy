import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldAlert } from 'lucide-react';
import Button from '../components/Button';

export default function UnauthorizedPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-950 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full text-center space-y-6 bg-white dark:bg-slate-900 p-10 rounded-2xl shadow-xl border border-slate-200 dark:border-slate-800">
        <div className="mx-auto h-20 w-20 bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-500 flex items-center justify-center rounded-full">
          <ShieldAlert className="h-12 w-12" />
        </div>
        
        <div>
          <h2 className="text-3xl font-extrabold text-slate-900 dark:text-white mb-2">Access Denied</h2>
          <p className="text-slate-500 dark:text-slate-400">
            You do not have the required permissions to view this page. If you believe this is an error, please contact your system administrator.
          </p>
        </div>
        
        <div className="pt-4">
          <Button onClick={() => navigate('/dashboard')} size="lg" className="w-full">
            Return to Dashboard
          </Button>
        </div>
      </div>
    </div>
  );
}
