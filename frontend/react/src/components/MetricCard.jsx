import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import clsx from 'clsx';

const MetricCard = ({ title, value, subtitle, trend, trendValue, icon: Icon, variant = 'default' }) => {
  const variantStyles = {
    default: 'border-slate-200',
    success: 'border-success-500 bg-success-50',
    warning: 'border-warning-500 bg-warning-50',
    danger: 'border-danger-500 bg-danger-50'
  };

  const TrendIcon = trend === 'up' ? TrendingUp : trend === 'down' ? TrendingDown : Minus;
  const trendColors = {
    up: 'text-success-600',
    down: 'text-danger-600',
    neutral: 'text-slate-400'
  };

  return (
    <div className={clsx('metric-card', variantStyles[variant])}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500 mb-1">{title}</p>
          <p className="text-3xl font-bold text-slate-800">{value}</p>
          {subtitle && <p className="text-sm text-slate-500 mt-1">{subtitle}</p>}
        </div>
        {Icon && (
          <div className="p-2 bg-primary-50 rounded-lg">
            <Icon className="w-6 h-6 text-primary-600" />
          </div>
        )}
      </div>
      {trend && (
        <div className={clsx('flex items-center gap-1 mt-3 text-sm', trendColors[trend])}>
          <TrendIcon className="w-4 h-4" />
          <span>{trendValue}</span>
        </div>
      )}
    </div>
  );
};

export default MetricCard;
