'use client';

import { OverallStatus } from '@/types';

interface StatusBannerProps {
  status: OverallStatus;
}

export default function StatusBanner({ status }: StatusBannerProps) {
  const getBannerStyle = () => {
    switch (status.status) {
      case 'operational':
        return 'bg-emerald-500 dark:bg-emerald-600';
      case 'partial_outage':
        return 'bg-amber-500 dark:bg-amber-600';
      case 'major_outage':
        return 'bg-red-500 dark:bg-red-600';
      default:
        return 'bg-gray-500 dark:bg-gray-600';
    }
  };

  const getIcon = () => {
    switch (status.status) {
      case 'operational':
        return (
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
      case 'partial_outage':
        return (
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        );
      case 'major_outage':
        return (
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
      default:
        return null;
    }
  };

  return (
    <div className={`${getBannerStyle()} text-white py-6 px-4 rounded-lg shadow-lg mb-8`}>
      <div className="max-w-4xl mx-auto flex items-center justify-center gap-4">
        {getIcon()}
        <h1 className="text-2xl font-bold">{status.message}</h1>
      </div>
    </div>
  );
}
