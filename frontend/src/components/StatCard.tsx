import React from 'react';
import Card from './Card';
import { TrendingUp, TrendingDown } from 'lucide-react';

type StatCardProps = {
  title: string;
  value: string | number;
  trend?: number;
  trendLabel?: string;
  icon: React.ElementType;
};

export default function StatCard({ title, value, trend, trendLabel, icon: Icon }: StatCardProps) {
  const isPositive = trend && trend > 0;
  const isNegative = trend && trend < 0;

  return (
    <Card className="flex flex-col">
      <div className="flex justify-between items-start">
        <div>
          <p className="text-sm font-medium text-slate-500 dark:text-slate-400">{title}</p>
          <p className="mt-2 text-3xl font-bold text-slate-900 dark:text-slate-50">{value}</p>
        </div>
        <div className="p-3 bg-blue-50 dark:bg-blue-900/30 rounded-lg">
          <Icon className="w-6 h-6 text-blue-600 dark:text-blue-400" />
        </div>
      </div>
      
      {trend !== undefined && (
        <div className="mt-4 flex items-center text-sm">
          <span className={`flex items-center font-medium ${isPositive ? 'text-emerald-600 dark:text-emerald-400' : isNegative ? 'text-red-600 dark:text-red-400' : 'text-slate-600 dark:text-slate-400'}`}>
            {isPositive ? <TrendingUp className="w-4 h-4 mr-1" /> : isNegative ? <TrendingDown className="w-4 h-4 mr-1" /> : null}
            {Math.abs(trend)}%
          </span>
          <span className="ml-2 text-slate-500 dark:text-slate-400">{trendLabel || 'vs last month'}</span>
        </div>
      )}
    </Card>
  );
}
