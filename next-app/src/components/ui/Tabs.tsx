'use client';

import React from 'react';
import { clsx } from 'clsx';

interface Tab {
  id: string;
  label: string;
  icon?: React.ReactNode;
  count?: number;
}

interface TabsProps {
  tabs: Tab[];
  activeTab: string;
  onChange: (tabId: string) => void;
  variant?: 'default' | 'pills' | 'underline';
}

export function Tabs({ tabs, activeTab, onChange, variant = 'default' }: TabsProps) {
  const variants = {
    default: {
      container: 'flex gap-1 p-1 bg-light-bg dark:bg-dark-bg rounded-lg',
      tab: 'px-4 py-2 rounded-md font-medium transition-all',
      active: 'bg-light-surface dark:bg-dark-surface text-primary shadow-sm',
      inactive: 'text-light-textMuted dark:text-dark-textMuted hover:text-light-text dark:hover:text-dark-text',
    },
    pills: {
      container: 'flex gap-2',
      tab: 'px-4 py-2 rounded-full font-medium transition-all',
      active: 'bg-primary text-white shadow-lg shadow-primary/30',
      inactive: 'text-light-textMuted dark:text-dark-textMuted hover:bg-light-bg dark:hover:bg-dark-bg',
    },
    underline: {
      container: 'flex gap-6 border-b border-light-border dark:border-dark-border',
      tab: 'px-1 py-3 font-medium transition-all relative',
      active: 'text-primary',
      inactive: 'text-light-textMuted dark:text-dark-textMuted hover:text-light-text dark:hover:text-dark-text',
    },
  };

  const v = variants[variant];

  return (
    <div className={v.container}>
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onChange(tab.id)}
          className={clsx(
            v.tab,
            activeTab === tab.id ? v.active : v.inactive
          )}
        >
          <div className="flex items-center gap-2">
            {tab.icon}
            {tab.label}
            {tab.count !== undefined && (
              <span className={clsx(
                'px-2 py-0.5 rounded-full text-xs',
                activeTab === tab.id
                  ? 'bg-white/20'
                  : 'bg-light-bg dark:bg-dark-bg'
              )}>
                {tab.count}
              </span>
            )}
          </div>
          {variant === 'underline' && activeTab === tab.id && (
            <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary" />
          )}
        </button>
      ))}
    </div>
  );
}
