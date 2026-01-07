'use client';

import { DailyUptime } from '@/types';
import { useState } from 'react';

interface UptimeBarProps {
  dailyUptimes: DailyUptime[];
}

export default function UptimeBar({ dailyUptimes }: UptimeBarProps) {
  const [hoveredDay, setHoveredDay] = useState<DailyUptime | null>(null);
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });

  const getBarColor = (uptime: number) => {
    if (uptime < 0) return 'bg-gray-300 dark:bg-gray-600'; // No data
    if (uptime >= 99) return 'bg-emerald-500';
    if (uptime >= 95) return 'bg-emerald-400';
    if (uptime >= 90) return 'bg-amber-400';
    if (uptime >= 50) return 'bg-amber-500';
    return 'bg-red-500';
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const handleMouseEnter = (day: DailyUptime, event: React.MouseEvent) => {
    setHoveredDay(day);
    const rect = event.currentTarget.getBoundingClientRect();
    setTooltipPosition({
      x: rect.left + rect.width / 2,
      y: rect.top - 10,
    });
  };

  return (
    <div className="relative">
      <div className="flex gap-[2px] items-end justify-start overflow-hidden">
        {dailyUptimes.map((day, index) => (
          <div
            key={day.date}
            className={`uptime-bar ${getBarColor(day.uptime_percentage)} cursor-pointer`}
            style={{ minWidth: '3px', flex: '1 1 3px', maxWidth: '8px' }}
            onMouseEnter={(e) => handleMouseEnter(day, e)}
            onMouseLeave={() => setHoveredDay(null)}
            title={`${formatDate(day.date)}: ${day.uptime_percentage >= 0 ? `${day.uptime_percentage.toFixed(1)}%` : 'No data'}`}
          />
        ))}
      </div>
      
      {hoveredDay && (
        <div
          className="fixed z-50 bg-gray-900 text-white text-xs rounded px-3 py-2 shadow-lg pointer-events-none"
          style={{
            left: tooltipPosition.x,
            top: tooltipPosition.y,
            transform: 'translate(-50%, -100%)',
          }}
        >
          <div className="font-semibold">{formatDate(hoveredDay.date)}</div>
          <div>
            {hoveredDay.uptime_percentage >= 0
              ? `${hoveredDay.uptime_percentage.toFixed(2)}% uptime`
              : 'No data'}
          </div>
          {hoveredDay.total_checks > 0 && (
            <div className="text-gray-400">
              {hoveredDay.successful_checks}/{hoveredDay.total_checks} checks passed
            </div>
          )}
        </div>
      )}
      
      <div className="flex justify-between text-xs text-gray-500 mt-2">
        <span>90 days ago</span>
        <span>Today</span>
      </div>
    </div>
  );
}
