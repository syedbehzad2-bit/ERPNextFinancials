'use client';

import React from 'react';
import { BarChart3 } from 'lucide-react';
import { SidebarNav } from './SidebarNav';
import { useAppStore } from '@/store/useAppStore';

export function Sidebar() {
  const { uploadedFiles, analysisResults } = useAppStore();

  const fileCount = uploadedFiles.length;
  const hasResults = analysisResults !== null;

  return (
    <aside className="sidebar">
      <div className="flex flex-col h-full">
        {/* Logo */}
        <div className="flex items-center gap-3 p-5 border-b border-light-border dark:border-dark-border">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-primary-hover flex items-center justify-center">
            <BarChart3 className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-light-text dark:text-dark-text">
              ERP Agent
            </h1>
            <p className="text-xs text-light-textMuted dark:text-dark-textMuted">
              Intelligence Platform
            </p>
          </div>
        </div>

        {/* Navigation */}
        <SidebarNav />

        {/* Spacer */}
        <div className="flex-1" />

        {/* Status */}
        <div className="p-4 m-3 rounded-xl bg-light-bg dark:bg-dark-bg border border-light-border dark:border-dark-border">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-light-textMuted dark:text-dark-textMuted">
              Data Status
            </span>
            {fileCount > 0 ? (
              <span className="w-2 h-2 rounded-full bg-success" />
            ) : (
              <span className="w-2 h-2 rounded-full bg-warning" />
            )}
          </div>
          <div className="text-sm">
            <span className="font-medium text-light-text dark:text-dark-text">
              {fileCount}
            </span>
            <span className="text-light-textMuted dark:text-dark-textMuted"> files loaded</span>
          </div>
          <div className="text-sm">
            <span className="font-medium text-light-text dark:text-dark-text">
              {hasResults ? 'Analyzed' : 'Pending'}
            </span>
          </div>
        </div>

        {/* Version */}
        <div className="p-3 text-center text-xs text-light-textMuted dark:text-dark-textMuted">
          v1.0.0
        </div>
      </div>
    </aside>
  );
}
