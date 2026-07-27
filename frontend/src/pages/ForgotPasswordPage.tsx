import React from 'react';
import { useNavigate } from 'react-router-dom';
import { KeyRound } from 'lucide-react';
import Input from '../components/Input';
import Button from '../components/Button';

export default function ForgotPasswordPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-950 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white dark:bg-slate-900 p-8 sm:p-10 rounded-2xl shadow-xl border border-slate-200 dark:border-slate-800">
        <div className="text-center">
          <div className="mx-auto h-16 w-16 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-500 flex items-center justify-center rounded-full mb-4">
            <KeyRound className="h-10 w-10" />
          </div>
          <h2 className="text-3xl font-extrabold text-slate-900 dark:text-white">Reset Password</h2>
          <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
            Enter your email to receive a password reset link.
          </p>
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={(e) => e.preventDefault()}>
          <div className="space-y-4">
            <Input
              label="Email Address"
              type="email"
              placeholder="admin@pds.tn.gov.in"
              required
            />
          </div>

          <div className="flex gap-4">
            <Button
              type="button"
              variant="secondary"
              className="w-full"
              onClick={() => navigate('/login')}
            >
              Back to Login
            </Button>
            <Button
              type="submit"
              className="w-full"
            >
              Send Link
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
