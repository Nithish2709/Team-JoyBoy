import React from 'react';
import StatCard from '../components/StatCard';
import Card from '../components/Card';
import Badge from '../components/Badge';
import Button from '../components/Button';
import { Package, AlertOctagon, ClipboardList, CheckCircle } from 'lucide-react';
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  BarChart, Bar, Legend, Cell
} from 'recharts';
import MapWidget from '../components/MapWidget';

// Mock Data
const stockData = [
  { month: 'Jan', allocated: 4000, lifted: 3800 },
  { month: 'Feb', allocated: 4200, lifted: 3900 },
  { month: 'Mar', allocated: 4100, lifted: 4050 },
  { month: 'Apr', allocated: 4500, lifted: 4200 },
  { month: 'May', allocated: 4300, lifted: 4150 },
  { month: 'Jun', allocated: 4600, lifted: 4400 },
];

const anomalyData = [
  { name: 'Stock Mismatch', count: 120, color: '#EF4444' },
  { name: 'POS Offline', count: 85, color: '#F59E0B' },
  { name: 'Ghost Lifting', count: 40, color: '#8B5CF6' },
  { name: 'Shop Closed', count: 65, color: '#3B82F6' },
];

const recentAlerts = [
  { id: 1, shop: 'FPS 034 - Anna Nagar', issue: 'Critical Stock Variance', severity: 'danger', time: '10 mins ago' },
  { id: 2, shop: 'FPS 102 - T. Nagar', issue: 'POS Device Offline (>24h)', severity: 'warning', time: '1 hour ago' },
  { id: 3, shop: 'FPS 088 - Mylapore', issue: 'Multiple Ghost Lifting Flags', severity: 'danger', time: '3 hours ago' },
  { id: 4, shop: 'FPS 214 - Velachery', issue: 'Unscheduled Closure', severity: 'info', time: '5 hours ago' },
];

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-50">State Executive Dashboard</h1>
          <p className="text-slate-500 dark:text-slate-400 mt-1">Real-time monitoring of Tamil Nadu PDS operations.</p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="secondary">Generate Report</Button>
          <Button variant="primary">Refresh Data</Button>
        </div>
      </div>

      {/* KPI Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard 
          title="Total Lifted vs Allocated" 
          value="94.2%" 
          trend={1.2} 
          icon={Package} 
        />
        <StatCard 
          title="Active Critical Anomalies" 
          value="156" 
          trend={-5.4} 
          icon={AlertOctagon} 
        />
        <StatCard 
          title="Pending Inspections" 
          value="84" 
          trend={12.5} 
          icon={ClipboardList} 
        />
        <StatCard 
          title="Grievance Resolution Rate" 
          value="88.7%" 
          trend={3.1} 
          icon={CheckCircle} 
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card title="Statewide Stock Allocation vs Lifting (MT)" className="lg:col-span-2">
          <div className="h-80 w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={stockData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorAllocated" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#94a3b8" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#94a3b8" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorLifted" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#2563eb" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#2563eb" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#334155" opacity={0.2} />
                <XAxis dataKey="month" axisLine={false} tickLine={false} tick={{fill: '#64748b'}} dy={10} />
                <YAxis axisLine={false} tickLine={false} tick={{fill: '#64748b'}} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#f8fafc' }}
                  itemStyle={{ color: '#e2e8f0' }}
                />
                <Area type="monotone" dataKey="allocated" name="Allocated" stroke="#94a3b8" fillOpacity={1} fill="url(#colorAllocated)" />
                <Area type="monotone" dataKey="lifted" name="Lifted" stroke="#2563eb" fillOpacity={1} fill="url(#colorLifted)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card title="Anomaly Distribution">
          <div className="h-80 w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={anomalyData} layout="vertical" margin={{ top: 0, right: 30, left: 20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#334155" opacity={0.2} />
                <XAxis type="number" axisLine={false} tickLine={false} tick={{fill: '#64748b'}} />
                <YAxis dataKey="name" type="category" axisLine={false} tickLine={false} tick={{fill: '#64748b'}} width={100} />
                <Tooltip 
                  cursor={{fill: 'transparent'}}
                  contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#f8fafc' }}
                />
                <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                  {anomalyData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      {/* Actionable Intelligence Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card 
          title="Recent Critical Alerts" 
          action={<Button variant="ghost" size="sm">View All</Button>}
        >
          <div className="divide-y divide-slate-200 dark:divide-slate-800 mt-2">
            {recentAlerts.map((alert) => (
              <div key={alert.id} className="py-4 flex justify-between items-center group">
                <div>
                  <p className="text-sm font-medium text-slate-900 dark:text-slate-100 group-hover:text-blue-500 transition-colors cursor-pointer">{alert.shop}</p>
                  <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">{alert.issue}</p>
                </div>
                <div className="flex flex-col items-end">
                  <Badge variant={alert.severity as any}>{alert.severity.toUpperCase()}</Badge>
                  <span className="text-xs text-slate-400 mt-2">{alert.time}</span>
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card 
          title="Statewide Risk Hotspots"
          action={<Button variant="ghost" size="sm">Full Map</Button>}
        >
          <div className="h-64 w-full mt-2">
            <MapWidget />
          </div>
        </Card>
      </div>
    </div>
  );
}
