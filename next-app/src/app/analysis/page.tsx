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

    // Simulate analysis - in production, this would call the Python backend
    await new Promise((resolve) => setTimeout(resolve, 3000));

    // Mock results
    const mockResults = {
      generated_at: new Date().toISOString(),
      data_source: uploadedFiles.map((f) => f.name).join(', '),
      data_types: dataTypes,
      data_quality: {
        total_rows: uploadedFiles.reduce((sum, f) => sum + f.rows, 0),
        total_columns: uploadedFiles[0]?.columns.length || 0,
        missing_values: {},
        duplicate_rows: 0,
        issues: [],
        is_usable: true,
        usable_message: 'Data is ready for analysis',
      },
      executive_summary: [
        'Revenue shows a positive trend with 12% growth over the analysis period',
        'Inventory turnover needs attention - 23% of stock is aged over 90 days',
        'Customer concentration risk identified - top 3 customers represent 45% of revenue',
        'Production efficiency improved by 8% compared to previous period',
        'Supplier delivery performance is stable at 94% on-time rate',
      ],
      financial: {
        kpis: [
          { label: 'Total Revenue', value: '$2.4M', change: 12.5 },
          { label: 'Net Margin', value: '18.2%', isPercentage: true },
          { label: 'Gross Profit', value: '$890K', change: 8.3 },
          { label: 'Operating Expenses', value: '$456K', change: -2.1 },
        ],
        charts_data: {},
        insights: [
          {
            category: DataType.FINANCIAL,
            severity: 'high',
            finding: 'Operating expenses increased by 15% in Q4',
            impact: 'Higher costs are reducing net margin by 2 percentage points',
            action: 'Review Q4 expense reports and identify non-essential spending',
            metrics: { amount: 456000, percentage: 15 },
          },
        ],
      },
      manufacturing: {
        kpis: [
          { label: 'Production Efficiency', value: '87%', change: 5.2 },
          { label: 'Wastage Rate', value: '3.2%', isPercentage: true },
          { label: 'Units Produced', value: 45600 },
          { label: 'Cost per Unit', value: '$24.50', change: -1.5 },
        ],
        charts_data: {},
        insights: [
          {
            category: DataType.MANUFACTURING,
            severity: 'medium',
            finding: 'Wastage on Product Line A exceeded target',
            impact: 'Additional $12,000 in material costs this quarter',
            action: 'Investigate machine calibration and operator training for Line A',
            metrics: { wastage: 3.2, target: 2.0 },
          },
        ],
      },
      inventory: {
        kpis: [
          { label: 'Stock Value', value: '$1.2M' },
          { label: 'Turnover Ratio', value: '4.2x' },
          { label: 'Days Inventory', value: '87 days' },
          { label: 'Dead Stock', value: '$45K', isPercentage: true },
        ],
        charts_data: {},
        insights: [
          {
            category: DataType.INVENTORY,
            severity: 'critical',
            finding: '23% of inventory aged over 90 days',
            impact: 'Tied up capital of $276,000 in slow-moving stock',
            action: 'Implement discount strategy for aged items or consider liquidation',
            metrics: { aged_percentage: 23, amount: 276000 },
          },
        ],
      },
      sales: {
        kpis: [
          { label: 'Total Orders', value: 1250 },
          { label: 'Revenue', value: '$2.4M', change: 12.5 },
          { label: 'Avg Order Value', value: '$1,920' },
          { label: 'Unique Customers', value: 89 },
        ],
        charts_data: {},
        insights: [
          {
            category: DataType.SALES,
            severity: 'high',
            finding: 'Top 3 customers represent 45% of total revenue',
            impact: 'High customer concentration creates significant revenue risk',
            action: 'Develop customer diversification strategy and increase marketing to new segments',
            metrics: { concentration: 45, risk_level: 'high' },
          },
        ],
      },
      purchase: {
        kpis: [
          { label: 'Total Spend', value: '$890K' },
          { label: 'Suppliers', value: 23 },
          { label: 'Avg Lead Time', value: '8.5 days' },
          { label: 'On-Time Delivery', value: '94%', isPercentage: true },
        ],
        charts_data: {},
        insights: [],
      },
      critical_risks: [
        {
          id: '1',
          title: 'Customer Concentration Risk',
          category: DataType.SALES,
          description: 'Top 3 customers account for 45% of revenue',
          probability: 'high',
          financial_impact: '$1.08M',
          time_to_impact: '3-6 months',
          severity: 'critical',
          mitigation: 'Diversify customer base through targeted marketing',
          early_warning_signals: ['Customer satisfaction decline', 'Large contract renewals pending'],
        },
        {
          id: '2',
          title: 'Slow Moving Inventory',
          category: DataType.INVENTORY,
          description: '$276,000 tied up in aged stock',
          probability: 'high',
          financial_impact: '$276K',
          time_to_impact: '1-3 months',
          severity: 'high',
          mitigation: 'Clearance sales and inventory review',
          early_warning_signals: ['No movement for 90+ days', 'Storage costs accumulating'],
        },
      ],
      action_plan: [
        {
          id: '1',
          title: 'Clear Aged Inventory',
          what: 'Implement 15% discount on items aged 90+ days',
          why: 'Capital is tied up in slow-moving stock',
          how: '1. Identify items 2. Calculate discount 3. Update pricing 4. Monitor movement',
          impact: 'Release $150K in working capital',
          priority: 'immediate',
          timeline: '0-30 days',
          estimated_savings: 150000,
        },
        {
          id: '2',
          title: 'Reduce Customer Concentration',
          what: 'Launch customer acquisition campaign',
          why: '45% revenue from top 3 customers is risky',
          how: '1. Budget allocation 2. Channel selection 3. Campaign execution 4. Track new signups',
          impact: 'Reduce top-3 concentration to 30%',
          priority: 'short_term',
          timeline: '1-3 months',
          estimated_revenue_impact: 250000,
        },
        {
          id: '3',
          title: 'Improve Production Efficiency',
          what: 'Operator training program for Line A',
          why: 'Line A wastage exceeds 2% target',
          how: '1. Assess training needs 2. Develop curriculum 3. Schedule sessions 4. Measure results',
          impact: 'Reduce wastage by 50%',
          priority: 'short_term',
          timeline: '1-3 months',
          estimated_savings: 6000,
        },
      ],
      analysis_results: {},
    };

    setAnalysisResults(mockResults as any);
    setIsRunning(false);
    router.push('/results');
  };

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
