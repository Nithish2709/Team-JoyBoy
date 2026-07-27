import React from 'react';
import { useParams } from 'react-router-dom';
import { useFPSData } from '../hooks/useFPSData';
import Card from '../components/Card';
import Badge from '../components/Badge';
import DataTable, { type Column } from '../components/DataTable';
import { User, Store, Activity, AlertCircle } from 'lucide-react';

export default function FPSMonitoringPage() {
  const { id } = useParams<{ id: string }>();
  const shopId = id || 'FPS-034';
  
  const { data, isLoading, isError } = useFPSData(shopId);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 dark:border-blue-400"></div>
        <p className="mt-4 text-slate-500 dark:text-slate-400">Loading shop intelligence...</p>
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="p-6 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-lg flex items-center gap-3">
        <AlertCircle />
        <span>Failed to load data for Shop {shopId}.</span>
      </div>
    );
  }

  const inventoryColumns: Column<typeof data.inventory[0]>[] = [
    { header: 'Commodity', accessor: 'item', className: 'font-semibold' },
    { header: 'Allocated (Kg)', accessor: 'allocated' },
    { header: 'Lifted (Kg)', accessor: 'lifted' },
    { 
      header: 'Variance', 
      accessor: (row) => (
        <span className={row.variance > 100 ? 'text-red-500 font-bold flex items-center gap-1' : ''}>
          {row.variance > 100 && <AlertCircle className="w-4 h-4" />}
          {row.variance}
        </span>
      )
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header Profile */}
      <div className="bg-white dark:bg-slate-900 rounded-xl p-6 shadow-sm border border-slate-200 dark:border-slate-800">
        <div className="flex flex-col md:flex-row justify-between md:items-center gap-4">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-50">{data.name}</h1>
              <Badge variant={data.status === 'online' ? 'success' : 'danger'}>
                {data.status === 'online' ? 'POS ONLINE' : 'POS OFFLINE'}
              </Badge>
            </div>
            <div className="flex items-center gap-4 text-sm text-slate-500 dark:text-slate-400">
              <span className="flex items-center gap-1"><Store className="w-4 h-4" /> District: {data.district}</span>
              <span className="flex items-center gap-1"><User className="w-4 h-4" /> Agent: {data.agentName}</span>
              <span className="flex items-center gap-1"><Activity className="w-4 h-4" /> Last Sync: {new Date(data.lastSync).toLocaleTimeString()}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Inventory Table */}
        <div className="lg:col-span-2">
          <Card title="Current Inventory & Variance">
            <DataTable 
              data={data.inventory}
              columns={inventoryColumns}
              keyExtractor={(row) => row.item}
            />
          </Card>
        </div>

        {/* Anomalies Panel */}
        <div>
          <Card title="Active System Flags">
            {data.activeAnomalies.length === 0 ? (
              <p className="text-slate-500 text-sm">No active anomalies detected.</p>
            ) : (
              <div className="space-y-4 mt-2">
                {data.activeAnomalies.map(anomaly => (
                  <div key={anomaly.id} className="p-4 bg-red-50 dark:bg-red-500/10 border border-red-200 dark:border-red-500/30 rounded-lg">
                    <div className="flex justify-between items-start mb-2">
                      <Badge variant="danger">{anomaly.severity.toUpperCase()}</Badge>
                      <span className="text-xs text-red-400">{new Date(anomaly.date).toLocaleTimeString()}</span>
                    </div>
                    <p className="font-medium text-red-800 dark:text-red-300 text-sm">{anomaly.type}</p>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </div>

      </div>
    </div>
  );
}
