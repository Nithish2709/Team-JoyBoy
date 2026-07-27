export type FPSDetails = {
  id: string;
  name: string;
  agentName: string;
  district: string;
  status: 'online' | 'offline';
  lastSync: string;
  inventory: {
    item: string;
    allocated: number;
    lifted: number;
    variance: number;
  }[];
  activeAnomalies: { id: string; type: string; severity: 'critical' | 'high' | 'medium'; date: string }[];
};

// Mocking a backend fetch delay
export const fetchFPSDetails = async (shopId: string): Promise<FPSDetails> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        id: shopId || 'FPS-034',
        name: 'FPS 034 - Anna Nagar',
        agentName: 'M. Ramesh',
        district: 'Chennai',
        status: 'online',
        lastSync: new Date(Date.now() - 15 * 60000).toISOString(),
        inventory: [
          { item: 'Rice', allocated: 2500, lifted: 2100, variance: 400 },
          { item: 'Wheat', allocated: 1200, lifted: 1150, variance: 50 },
          { item: 'Sugar', allocated: 800, lifted: 300, variance: 500 }, // Huge variance
        ],
        activeAnomalies: [
          { id: 'A-901', type: 'Critical Stock Variance - Sugar', severity: 'critical', date: new Date().toISOString() },
        ]
      });
    }, 1500); // 1.5 second artificial delay
  });
};
