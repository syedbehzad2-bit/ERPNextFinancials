'use client';

import React from 'react';
import { ThemeToggle } from '@/components/ui/ThemeToggle';
import { Bell, Search, User } from 'lucide-react';

export function Header() {
  return (
    <header className="h-16 px-6 flex items-center justify-between">
      {/* Search */}
      <div className="flex-1 max-w-md">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-light-textMuted dark:text-dark-textMuted" />
          <input
            type="text"
            placeholder="Search..."
            className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-light-surface dark:bg-dark-surface border border-light-border dark:border-dark-border text-light-text dark:text-dark-text placeholder-light-textMuted dark:placeholder-dark-textMuted focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all"
          />
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-3">
        <button className="relative p-2.5 rounded-xl bg-light-surface dark:bg-dark-surface border border-light-border dark:border-dark-border hover:bg-light-bg dark:hover:bg-dark-bg transition-colors">
          <Bell className="w-5 h-5 text-light-textMuted dark:text-dark-textMuted" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-error" />
        </button>

        <div className="w-px h-8 bg-light-border dark:bg-dark-border" />

        <ThemeToggle />

        <button className="flex items-center gap-3 p-2 rounded-xl bg-light-surface dark:bg-dark-surface border border-light-border dark:border-dark-border hover:bg-light-bg dark:hover:bg-dark-bg transition-colors">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-primary-hover flex items-center justify-center">
            <User className="w-4 h-4 text-white" />
          </div>
          <div className="hidden sm:block text-left">
            <p className="text-sm font-medium text-light-text dark:text-dark-text">
              Admin User
            </p>
            <p className="text-xs text-light-textMuted dark:text-dark-textMuted">
              admin@company.com
            </p>
          </div>
        </button>
      </div>
    </header>
  );
}
