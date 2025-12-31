'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  ChevronRight,
  FileText,
  Settings,
  BarChart3,
  Zap,
  Shield,
  TrendingUp,
  Package,
  ShoppingCart,
  Play,
  Loader2,
} from 'lucide-react';
import { Button, Card, CardHeader, Tabs } from '@/components/ui';
import { Sidebar, Header } from '@/components/layout';
import { useAppStore } from '@/store/useAppStore';
import { DataType } from '@/lib/types';
import { formatNumber } from '@/lib/formatters';

export default function AnalysisPage() {
  const router = useRouter();
  const {
    uploadedFiles,
    analysisConfig,
    setAnalysisConfig,
    isAnalyzing,
    setIsAnalyzing,
    setAnalysisResults,
  } = useAppStore();

  const [activeTab, setActiveTab] = useState('config');
  const [isRunning, setIsRunning] = useState(false);

  const dataTypes = [...new Set(uploadedFiles.map((f) => f.type))] as DataType[];

  const handleRunAnalysis = async () => {
    setIsRunning(true);
    setIsAnalyzing(true);

    try {
      // Call real Python backend via Next.js API
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          files: uploadedFiles,
          config: analysisConfig,
        }),
      });

      const result = await response.json();

      if (result.success && result.data) {
        setAnalysisResults(result.data);
        setIsRunning(false);
        router.push('/results');
        return;
      } else {
        alert('Analysis failed: ' + (result.error || 'Unknown error'));
        setIsRunning(false);
        setIsAnalyzing(false);
        return;
      }
    } catch (error) {
      console.error('Analysis error:', error);
      alert('Analysis failed. Please try again.');
      setIsRunning(false);
      setIsAnalyzing(false);
      return;
    }


  const tabs = [
    { id: 'config', label: 'Configuration', icon: <Settings className="w-4 h-4" /> },
    { id: 'summary', label: 'Data Summary', icon: <FileText className="w-4 h-4" /> },
  ];

  return (
    <div className="flex min-h-screen">
      <Sidebar />

      <main className="flex-1 ml-64">
        <Header />

        <div className="p-8">
          {/* Page Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-light-text dark:text-dark-text mb-2">
              Configure Analysis
            </h1>
            <p className="text-light-textMuted dark:text-dark-textMuted">
              Review your configuration and run the analysis
            </p>
          </div>

          <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} />

          <div className="mt-6">
            {activeTab === 'config' && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Files to Analyze */}
                <Card variant="elevated" padding="lg">
                  <CardHeader
                    title="Files to Analyze"
                    subtitle={`${uploadedFiles.length} file(s) selected`}
                  />

                  <div className="space-y-3">
                    {uploadedFiles.map((file) => (
                      <div
                        key={file.id}
                        className="flex items-center gap-3 p-3 rounded-xl bg-light-bg dark:bg-dark-bg"
                      >
                        <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary to-primary-hover flex items-center justify-center">
                          <FileText className="w-5 h-5 text-white" />
                        </div>
                        <div className="flex-1">
                          <p className="font-medium text-light-text dark:text-dark-text">
                            {file.name}
                          </p>
                          <p className="text-sm text-light-textMuted dark:text-dark-textMuted">
                            {formatNumber(file.rows)} rows | {file.type}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </Card>

                {/* Analysis Settings */}
                <Card variant="elevated" padding="lg">
                  <CardHeader
                    title="Analysis Settings"
                    subtitle="Configure analysis depth and methods"
                  />

                  <div className="space-y-6">
                    <div>
                      <label className="block text-sm font-medium text-light-text dark:text-dark-text mb-2">
                        Analysis Depth
                      </label>
                      <div className="grid grid-cols-3 gap-3">
                        {(['summary', 'detailed', 'comprehensive'] as const).map((depth) => (
                          <button
                            key={depth}
                            onClick={() => setAnalysisConfig({
                              ...analysisConfig,
                              analysis_depth: depth,
                            })}
                            className={`p-3 rounded-xl border transition-all ${
                              analysisConfig.analysis_depth === depth
                                ? 'border-primary bg-primary/5 text-primary'
                                : 'border-light-border dark:border-dark-border hover:border-primary/50'
                            }`}
                          >
                            <p className="font-medium capitalize text-light-text dark:text-dark-text">
                              {depth}
                            </p>
                          </button>
                        ))}
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-light-text dark:text-dark-text mb-2">
                        Analysis Methods
                      </label>
                      <div className="space-y-2">
                        {['Trend Analysis', 'Variance Analysis', 'Pareto Analysis', 'Ratio Analysis'].map((method) => (
                          <label key={method} className="flex items-center gap-3 cursor-pointer">
                            <input
                              type="checkbox"
                              checked
                              className="w-5 h-5 rounded border-light-border dark:border-dark-border text-primary focus:ring-primary"
                            />
                            <span className="text-sm text-light-text dark:text-dark-text">{method}</span>
                          </label>
                        ))}
                      </div>
                    </div>

                    <div>
                      <label className="flex items-center gap-3 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={analysisConfig.enable_cross_file_analysis}
                          onChange={(e) => setAnalysisConfig({
                            ...analysisConfig,
                            enable_cross_file_analysis: e.target.checked,
                          })}
                          className="w-5 h-5 rounded border-light-border dark:border-dark-border text-primary focus:ring-primary"
                        />
                        <div>
                          <span className="text-sm font-medium text-light-text dark:text-dark-text">
                            Enable Cross-File Analysis
                          </span>
                          <p className="text-xs text-light-textMuted dark:text-dark-textMuted">
                            Analyze relationships between different data types
                          </p>
                        </div>
                      </label>
                    </div>
                  </div>
                </Card>

                {/* Domains to Analyze */}
                <Card variant="elevated" padding="lg" className="lg:col-span-2">
                  <CardHeader
                    title="Domains to Analyze"
                    subtitle="Select which business domains to include"
                  />

                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
                    {[
                      { type: 'financial', icon: <TrendingUp />, label: 'Financial', desc: 'P&L, Margins' },
                      { type: 'manufacturing', icon: <BarChart3 />, label: 'Manufacturing', desc: 'Production, Wastage' },
                      { type: 'inventory', icon: <Package />, label: 'Inventory', desc: 'Stock, Aging' },
                      { type: 'sales', icon: <TrendingUp />, label: 'Sales', desc: 'Orders, Customers' },
                      { type: 'purchase', icon: <ShoppingCart />, label: 'Purchase', desc: 'Suppliers, Lead Time' },
                    ].map((domain) => (
                      <button
                        key={domain.type}
                        onClick={() => setAnalysisConfig({
                          ...analysisConfig,
                          analysis_types: {
                            ...analysisConfig.analysis_types,
                            [domain.type]: !analysisConfig.analysis_types[domain.type as keyof typeof analysisConfig.analysis_types],
                          },
                        })}
                        className={`p-4 rounded-xl border transition-all text-left ${
                          analysisConfig.analysis_types[domain.type as keyof typeof analysisConfig.analysis_types]
                            ? 'border-primary bg-primary/5'
                            : 'border-light-border dark:border-dark-border hover:border-primary/50'
                        }`}
                      >
                        <div className={`w-10 h-10 rounded-lg bg-gradient-to-br from-primary to-primary-hover flex items-center justify-center mb-3`}>
                          {domain.icon}
                        </div>
                        <p className="font-medium text-light-text dark:text-dark-text">{domain.label}</p>
                        <p className="text-xs text-light-textMuted dark:text-dark-textMuted">{domain.desc}</p>
                      </button>
                    ))}
                  </div>
                </Card>

                {/* Run Analysis Button */}
                <div className="lg:col-span-2">
                  <Card variant="elevated" padding="lg" className="text-center">
                    <div className="flex flex-col items-center">
                      <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary to-primary-hover flex items-center justify-center mb-4">
                        <Zap className="w-8 h-8 text-white" />
                      </div>
                      <h3 className="text-xl font-bold text-light-text dark:text-dark-text mb-2">
                        Ready to Analyze
                      </h3>
                      <p className="text-light-textMuted dark:text-dark-textMuted mb-6 max-w-md">
                        {uploadedFiles.length} file(s) will be analyzed across {dataTypes.length} domain(s).
                        {analysisConfig.enable_cross_file_analysis && ' Cross-file analysis enabled.'}
                      </p>

                      <Button
                        onClick={handleRunAnalysis}
                        disabled={isRunning}
                        size="lg"
                        className="min-w-[200px]"
                      >
                        {isRunning ? (
                          <>
                            <Loader2 className="w-5 h-5 animate-spin" />
                            Analyzing...
                          </>
                        ) : (
                          <>
                            <Play className="w-5 h-5" />
                            Run Analysis
                          </>
                        )}
                      </Button>
                    </div>
                  </Card>
                </div>
              </div>
            )}

            {activeTab === 'summary' && (
              <Card variant="elevated" padding="lg">
                <CardHeader title="Data Summary" />

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  <div className="p-4 rounded-xl bg-light-bg dark:bg-dark-bg text-center">
                    <p className="text-3xl font-bold text-primary">{uploadedFiles.length}</p>
                    <p className="text-sm text-light-textMuted dark:text-dark-textMuted">Files</p>
                  </div>
                  <div className="p-4 rounded-xl bg-light-bg dark:bg-dark-bg text-center">
                    <p className="text-3xl font-bold text-primary">
                      {formatNumber(uploadedFiles.reduce((sum, f) => sum + f.rows, 0))}
                    </p>
                    <p className="text-sm text-light-textMuted dark:text-dark-textMuted">Total Rows</p>
                  </div>
                  <div className="p-4 rounded-xl bg-light-bg dark:bg-dark-bg text-center">
                    <p className="text-3xl font-bold text-primary">{dataTypes.length}</p>
                    <p className="text-sm text-light-textMuted dark:text-dark-textMuted">Domains</p>
                  </div>
                  <div className="p-4 rounded-xl bg-light-bg dark:bg-dark-bg text-center">
                    <p className="text-3xl font-bold text-primary">
                      {formatNumber(uploadedFiles[0]?.columns.length || 0)}
                    </p>
                    <p className="text-sm text-light-textMuted dark:text-dark-textMuted">Columns</p>
                  </div>
                </div>

                <div className="space-y-4">
                  {dataTypes.map((type) => {
                    const files = uploadedFiles.filter((f) => f.type === type);
                    return (
                      <div
                        key={type}
                        className="p-4 rounded-xl bg-light-bg dark:bg-dark-bg border border-light-border dark:border-dark-border"
                      >
                        <p className="font-medium text-light-text dark:text-dark-text capitalize mb-2">
                          {type} Domain
                        </p>
                        <div className="flex gap-2 flex-wrap">
                          {files.map((file) => (
                            <span
                              key={file.id}
                              className="px-3 py-1 rounded-full text-xs bg-primary/10 text-primary"
                            >
                              {file.name} ({formatNumber(file.rows)} rows)
                            </span>
                          ))}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </Card>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
