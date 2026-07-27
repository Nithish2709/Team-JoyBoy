import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Clock } from 'lucide-react';
import Button from '../components/Button';

export default function SessionExpiredPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-950 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full text-center space-y-6 bg-white dark:bg-slate-900 p-10 rounded-2xl shadow-xl border border-slate-200 dark:border-slate-800">
        <div className="mx-auto h-20 w-20 bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-500 flex items-center justify-center rounded-full">
          <Clock className="h-12 w-12" />
        </div>
        
        <div>
          <h2 className="text-3xl font-extrabold text-slate-900 dark:text-white mb-2">Session Expired</h2>
          <p className="text-slate-500 dark:text-slate-400">
            Your secure session has expired due to inactivity or invalid credentials. Please sign in again to continue.
          </p>
        </div>
        
        <div className="pt-4">
          <Button onClick={() => navigate('/login')} size="lg" className="w-full">
            Sign In Again
          </Button>
        </div>
      </div>
    </div>
  );
}
