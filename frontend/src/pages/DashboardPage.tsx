import React from 'react';
import Card from '../components/Card';
import { useAuthStore } from '../store/useAuthStore';
import { ShieldCheck, MapPin, UserCheck, Key, Compass } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/Button';

export default function DashboardPage() {
  const { user } = useAuthStore();
  const navigate = useNavigate();

  if (!user) return null;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-50">Welcome back, {user.name}</h1>
          <p className="text-slate-500 dark:text-slate-400 mt-1">PDS Sentinel AI Executive Dashboard Placeholder</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card title="Your Profile Information" className="lg:col-span-2">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
            <div className="flex items-center gap-4 p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg border border-slate-200 dark:border-slate-700">
              <div className="p-3 bg-blue-100 dark:bg-blue-900/40 text-blue-600 dark:text-blue-400 rounded-full">
                <UserCheck className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm font-medium text-slate-500 dark:text-slate-400">Account Type</p>
                <p className="text-lg font-bold text-slate-900 dark:text-slate-100 capitalize">{user.role}</p>
              </div>
            </div>

            <div className="flex items-center gap-4 p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg border border-slate-200 dark:border-slate-700">
              <div className="p-3 bg-emerald-100 dark:bg-emerald-900/40 text-emerald-600 dark:text-emerald-400 rounded-full">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm font-medium text-slate-500 dark:text-slate-400">Security Clearance</p>
                <p className="text-sm font-bold text-slate-900 dark:text-slate-100">
                  {user.permissions.length} active permissions
                </p>
              </div>
            </div>

            <div className="flex items-center gap-4 p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg border border-slate-200 dark:border-slate-700">
              <div className="p-3 bg-purple-100 dark:bg-purple-900/40 text-purple-600 dark:text-purple-400 rounded-full">
                <MapPin className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm font-medium text-slate-500 dark:text-slate-400">Assigned Region</p>
                <p className="text-lg font-bold text-slate-900 dark:text-slate-100">{user.district || 'Statewide'}</p>
              </div>
            </div>
            
            <div className="flex items-center gap-4 p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg border border-slate-200 dark:border-slate-700">
              <div className="p-3 bg-amber-100 dark:bg-amber-900/40 text-amber-600 dark:text-amber-400 rounded-full">
                <Key className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm font-medium text-slate-500 dark:text-slate-400">Session ID</p>
                <p className="text-sm font-bold text-slate-900 dark:text-slate-100">{user.id}</p>
              </div>
            </div>
          </div>
        </Card>

        <Card title="Quick Navigation">
          <div className="mt-4 flex flex-col gap-3">
            <Button variant="secondary" className="w-full justify-start" onClick={() => navigate('/profile')}>
              <UserCheck className="w-4 h-4 mr-2" /> View My Profile
            </Button>
            <Button variant="secondary" className="w-full justify-start" onClick={() => navigate('/settings')}>
              <Compass className="w-4 h-4 mr-2" /> Platform Settings
            </Button>
            <Button variant="ghost" className="w-full justify-start text-red-600 hover:text-red-700 dark:text-red-400" onClick={() => navigate('/unauthorized')}>
              <ShieldCheck className="w-4 h-4 mr-2" /> Test 403 Page
            </Button>
          </div>
        </Card>
      </div>
    </div>
  );
}
