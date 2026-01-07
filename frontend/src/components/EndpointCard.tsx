'use client';

import { EndpointStatus, DailyUptime } from '@/types';
import UptimeBar from './UptimeBar';
import { useEffect, useState } from 'react';

interface EndpointCardProps {
  endpointStatus: EndpointStatus;
}

export default function EndpointCard({ endpointStatus }: EndpointCardProps) {
  const [history, setHistory] = useState<DailyUptime[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchHistory() {
      try {
        const res = await fetch(`/api/endpoints/${endpointStatus.endpoint.id}/history`);
        if (res.ok) {
          const data = await res.json();
          setHistory(data.daily_uptimes);
        }
      } catch (error) {
        console.error('Failed to fetch history:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchHistory();
  }, [endpointStatus.endpoint.id]);

  const getStatusBadge = () => {
    if (endpointStatus.current_status) {
      return (
        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-medium bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          Operational
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200">
        <span className="w-2 h-2 rounded-full bg-red-500"></span>
        Down
      </span>
    );
  };

  const formatLastCheck = (lastCheck: string | null) => {
    if (!lastCheck) return 'Never';
    const date = new Date(lastCheck);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} min ago`;
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    const diffDays = Math.floor(diffHours / 24);
    return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow duration-200">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            {endpointStatus.endpoint.name}
          </h3>
          <p className="text-sm text-gray-500 dark:text-gray-400 truncate max-w-xs" title={endpointStatus.endpoint.url}>
            {endpointStatus.endpoint.url}
          </p>
        </div>
        {getStatusBadge()}
      </div>

      <div className="grid grid-cols-3 gap-4 mb-6 text-sm">
        <div>
          <p className="text-gray-500 dark:text-gray-400">Uptime (90d)</p>
          <p className="font-semibold text-gray-900 dark:text-white">
            {endpointStatus.uptime_90d.toFixed(2)}%
          </p>
        </div>
        <div>
          <p className="text-gray-500 dark:text-gray-400">Response Time</p>
          <p className="font-semibold text-gray-900 dark:text-white">
            {endpointStatus.response_time ? `${endpointStatus.response_time.toFixed(0)}ms` : 'N/A'}
          </p>
        </div>
        <div>
          <p className="text-gray-500 dark:text-gray-400">Last Check</p>
          <p className="font-semibold text-gray-900 dark:text-white">
            {formatLastCheck(endpointStatus.last_check)}
          </p>
        </div>
      </div>

      <div>
        <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">90-Day Uptime History</p>
        {loading ? (
          <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
        ) : (
          <UptimeBar dailyUptimes={history} />
        )}
      </div>
    </div>
  );
}
