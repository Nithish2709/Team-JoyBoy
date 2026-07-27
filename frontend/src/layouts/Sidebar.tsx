import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Map, 
  MapPin, 
  Store, 
  AlertTriangle, 
  TrendingUp, 
  Search, 
  ClipboardCheck, 
  FileText, 
  Settings 
} from 'lucide-react';

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'State Overview', href: '/state', icon: Map },
  { name: 'District Monitoring', href: '/districts', icon: MapPin },
  { name: 'FPS Monitoring', href: '/shops', icon: Store },
  { name: 'Complaint Analytics', href: '/complaints', icon: AlertTriangle },
  { name: 'Predictions', href: '/predictions', icon: TrendingUp },
  { name: 'Investigation Center', href: '/investigations', icon: Search },
  { name: 'Inspection Queue', href: '/inspections', icon: ClipboardCheck },
  { name: 'Reports', href: '/reports', icon: FileText },
];

export default function Sidebar() {
  const location = useLocation();

  return (
    <div className="flex h-full w-64 flex-col bg-slate-900 border-r border-slate-800">
      <div className="flex h-16 shrink-0 items-center px-6 bg-slate-950 border-b border-slate-800">
        <h1 className="text-xl font-bold text-blue-500 flex items-center gap-2">
          <ShieldIcon /> PDS Sentinel AI
        </h1>
      </div>
      <div className="flex flex-1 flex-col overflow-y-auto pt-4">
        <nav className="flex-1 space-y-1 px-3">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href || 
                             (item.href !== '/' && location.pathname.startsWith(item.href));
            
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`group flex items-center rounded-md px-3 py-2 text-sm font-medium ${
                  isActive
                    ? 'bg-blue-900/50 text-blue-400'
                    : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
                }`}
              >
                <item.icon
                  className={`mr-3 h-5 w-5 shrink-0 ${
                    isActive ? 'text-blue-400' : 'text-slate-500 group-hover:text-slate-300'
                  }`}
                  aria-hidden="true"
                />
                {item.name}
              </Link>
            );
          })}
        </nav>
        <div className="mt-auto px-3 pb-4">
           <Link
              to="/settings"
              className={`group flex items-center rounded-md px-3 py-2 text-sm font-medium ${
                location.pathname === '/settings'
                  ? 'bg-blue-900/50 text-blue-400'
                  : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
              }`}
            >
              <Settings className="mr-3 h-5 w-5 shrink-0 text-slate-500 group-hover:text-slate-300" />
              Settings
           </Link>
        </div>
      </div>
    </div>
  );
}

function ShieldIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-6 h-6 text-blue-500">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
    </svg>
  )
}
