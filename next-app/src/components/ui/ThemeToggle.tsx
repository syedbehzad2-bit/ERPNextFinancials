'use client';

import React from 'react';
import { Sun, Moon } from 'lucide-react';
import { useTheme } from '@/components/theme/ThemeProvider';
import { clsx } from 'clsx';

export function ThemeToggle({ className }: { className?: string }) {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      className={clsx(
        'relative inline-flex items-center justify-center w-12 h-12 rounded-xl',
        'bg-light-surface dark:bg-dark-surface',
        'border border-light-border dark:border-dark-border',
        'hover:bg-light-bg dark:hover:bg-dark-bg',
        'transition-all duration-200',
        className
      )}
      aria-label="Toggle theme"
    >
      <Sun className={clsx(
        'w-5 h-5 absolute transition-all duration-200',
        theme === 'light' ? 'rotate-0 scale-100 opacity-100' : 'rotate-90 scale-0 opacity-0'
      )} />
      <Moon className={clsx(
        'w-5 h-5 absolute transition-all duration-200',
        theme === 'dark' ? 'rotate-0 scale-100 opacity-100' : '-rotate-90 scale-0 opacity-0'
      )} />
    </button>
  );
}
