'use client';

import React from 'react';
import { clsx } from 'clsx';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'elevated' | 'bordered';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export function Card({
  variant = 'elevated',
  padding = 'md',
  className,
  children,
  ...props
}: CardProps) {
  const variants = {
    default: 'bg-light-surface dark:bg-dark-surface',
    elevated: 'card-3d',
    bordered: 'bg-light-surface dark:bg-dark-surface border border-light-border dark:border-dark-border',
  };

  const paddings = {
    none: '',
    sm: 'p-3',
    md: 'p-5',
    lg: 'p-7',
  };

  return (
    <div
      className={clsx(
        'rounded-xl transition-all duration-300',
        variants[variant],
        paddings[padding],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  title: string;
  subtitle?: string;
  action?: React.ReactNode;
}

export function CardHeader({ title, subtitle, action, className, ...props }: CardHeaderProps) {
  return (
    <div className={clsx('flex items-start justify-between mb-4', className)} {...props}>
      <div>
        <h3 className="text-lg font-semibold text-light-text dark:text-dark-text">{title}</h3>
        {subtitle && (
          <p className="text-sm text-light-textMuted dark:text-dark-textMuted">{subtitle}</p>
        )}
      </div>
      {action && <div>{action}</div>}
    </div>
  );
}
