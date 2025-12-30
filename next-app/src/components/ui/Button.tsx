'use client';

import React from 'react';
import { clsx } from 'clsx';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'success' | 'warning' | 'error';
  size?: 'sm' | 'md' | 'lg';
  is3D?: boolean;
  loading?: boolean;
  children: React.ReactNode;
}

export function Button({
  variant = 'primary',
  size = 'md',
  is3D = true,
  loading = false,
  className,
  disabled,
  children,
  ...props
}: ButtonProps) {
  const baseStyles = 'inline-flex items-center justify-center font-semibold rounded-lg transition-all duration-150 ease-out disabled:opacity-50 disabled:cursor-not-allowed';

  const variants = {
    primary: 'bg-gradient-to-r from-primary to-primary-hover text-white hover:brightness-110',
    secondary: 'bg-light-surface dark:bg-dark-surface text-light-text dark:text-dark-text border border-light-border dark:border-dark-border',
    success: 'bg-gradient-to-r from-success to-success-light text-white hover:brightness-110',
    warning: 'bg-gradient-to-r from-warning to-warning-light text-white hover:brightness-110',
    error: 'bg-gradient-to-r from-error to-error-light text-white hover:brightness-110',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-5 py-2.5 text-base',
    lg: 'px-7 py-3.5 text-lg',
  };

  const shadow3D = is3D ? 'shadow-3d active:shadow-3d-active hover:shadow-3d-hover transform hover:-translate-y-0.5 active:translate-y-0' : '';

  return (
    <button
      className={clsx(baseStyles, variants[variant], sizes[size], shadow3D, className)}
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <svg className="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
      )}
      {children}
    </button>
  );
}
