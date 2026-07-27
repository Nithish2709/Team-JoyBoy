import React from 'react';
import Card from '../components/Card';
import StatCard from '../components/StatCard';
import Badge from '../components/Badge';
import Button from '../components/Button';
import DataTable, { type Column } from '../components/DataTable';
import { MapPin, AlertTriangle, ShieldCheck } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

type DistrictData = {
  id: string;
  name: string;
  totalFPS: number;
  allocationVsLifted: number;
  activeAnomalies: number;
  status: 'safe' | 'warning' | 'critical';
};

const mockDistricts: DistrictData[] = [
  { id: 'CHN', name: 'Chennai', totalFPS: 450, allocationVsLifted: 98.2, activeAnomalies: 12, status: 'warning' },
  { id: 'MDU', name: 'Madurai', totalFPS: 320, allocationVsLifted: 95.5, activeAnomalies: 4, status: 'safe' },
  { id: 'CBE', name: 'Coimbatore', totalFPS: 380, allocationVsLifted: 96.1, activeAnomalies: 5, status: 'safe' },
  { id: 'TVL', name: 'Tirunelveli', totalFPS: 280, allocationVsLifted: 88.4, activeAnomalies: 28, status: 'critical' },
  { id: 'TRY', name: 'Tiruchirappalli', totalFPS: 290, allocationVsLifted: 94.0, activeAnomalies: 9, status: 'warning' },
  { id: 'VLR', name: 'Vellore', totalFPS: 210, allocationVsLifted: 97.8, activeAnomalies: 2, status: 'safe' },
];

export default function DistrictMonitoringPage() {
  const navigate = useNavigate();

  const columns: Column<DistrictData>[] = [
    { header: 'District', accessor: 'name', className: 'font-semibold' },
    { header: 'Total FPS', accessor: 'totalFPS' },
    { 
      header: 'Allocated vs Lifted', 
      accessor: (row) => (
        <span className={row.allocationVsLifted < 90 ? 'text-red-500 font-medium' : ''}>
          {row.allocationVsLifted}%
        </span>
      ) 
    },
    { header: 'Active Anomalies', accessor: 'activeAnomalies' },
    { 
      header: 'Status', 
      accessor: (row) => {
        const variantMap = { safe: 'success', warning: 'warning', critical: 'danger' } as const;
        return <Badge variant={variantMap[row.status]}>{row.status.toUpperCase()}</Badge>;
      } 
    },
    { 
      header: 'Action', 
      accessor: (row) => (
        <Button size="sm" variant="secondary" onClick={() => navigate(`/districts/${row.id}`)}>
          View details
        </Button>
      ) 
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-50">District Monitoring</h1>
          <p className="text-slate-500 dark:text-slate-400 mt-1">Overview of all 38 districts in Tamil Nadu.</p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="secondary">Export CSV</Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard title="Total Districts" value="38" icon={MapPin} />
        <StatCard title="Critical Districts" value="3" icon={AlertTriangle} trend={1} trendLabel="since yesterday" />
        <StatCard title="Safe Districts" value="24" icon={ShieldCheck} trend={-2} trendLabel="since yesterday" />
      </div>

      <Card title="District Performance">
        <DataTable 
          data={mockDistricts} 
          columns={columns} 
          keyExtractor={(row) => row.id} 
        />
      </Card>
    </div>
  );
}
