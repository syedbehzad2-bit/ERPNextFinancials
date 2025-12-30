'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import {
  ChevronRight,
  FileText,
  AlertTriangle,
  CheckCircle,
  Clock,
  TrendingUp,
  TrendingDown,
  Download,
  Share2,
  RefreshCw,
  BarChart3,
  Shield,
  Lightbulb,
  Target,
  ArrowRight,
} from 'lucide-react';
import { Button, Card, CardHeader, Tabs } from '@/components/ui';
import { Sidebar, Header } from '@/components/layout';
import {
  RevenueChart,
  MarginChart,
  AgingChart,
  ParetoChart,
  EfficiencyChart,
  WastageChart,
  DeliveryChart,
  SpendChart,
  LeadTimeChart,
} from '@/components/charts';
import { useAppStore } from '@/store/useAppStore';
import { AnalysisResults, Insight, Risk, Recommendation, DataType, Severity, Priority } from '@/lib/types';
import { formatCurrency, formatPercentage, formatNumber } from '@/lib/formatters';

export default function ResultsPage() {
  const router = useRouter();
  const { analysisResults, isAnalyzing, setIsAnalyzing, uploadedFiles, analysisConfig } = useAppStore();

  const [activeTab, setActiveTab] = useState('summary');
  const [chartTab, setChartTab] = useState('financial');

  // Redirect if no results
  useEffect(() => {
    if (!isAnalyzing && !analysisResults) {
      router.push('/');
    }
  }, [isAnalyzing, analysisResults, router]);

  if (!analysisResults) {
    return (
      <div className="flex min-h-screen">
        <Sidebar />
        <main className="flex-1 ml-64">
          <Header />
          <div className="p-8 flex items-center justify-center h-[calc(100vh-4rem)]">
            <div className="text-center">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary to-primary-hover flex items-center justify-center mx-auto mb-4">
                <RefreshCw className="w-8 h-8 text-white animate-spin" />
              </div>
              <h2 className="text-xl font-bold text-light-text dark:text-dark-text mb-2">
                Loading Results...
              </h2>
            </div>
          </div>
        </main>
      </div>
    );
  }

  const {
    executive_summary,
    data_quality,
    financial,
    manufacturing,
    inventory,
    sales,
    purchase,
    critical_risks,
    action_plan,
  } = analysisResults as AnalysisResults;

  const dataTypes = [...new Set(uploadedFiles.map((f) => f.type))] as DataType[];

  const getSeverityColor = (severity: Severity) => {
    const colors = {
      [Severity.CRITICAL]: 'critical',
      [Severity.HIGH]: 'high',
      [Severity.MEDIUM]: 'medium',
      [Severity.LOW]: 'low',
    };
    return colors[severity];
  };

  const getPriorityColor = (priority: Priority) => {
    const colors = {
      [Priority.IMMEDIATE]: 'critical',
      [Priority.SHORT_TERM]: 'high',
      [Priority.MEDIUM_TERM]: 'medium',
    };
    return colors[priority];
  };

  const renderKPICard = (kpi: { label: string; value: string | number; change?: number; isPercentage?: boolean }) => (
    <div key={kpi.label} className="kpi-card">
      <div className="kpi-value">{kpi.isPercentage ? formatPercentage(Number(kpi.value)) : kpi.value}</div>
      <div className="kpi-label">{kpi.label}</div>
      {kpi.change !== undefined && (
        <div className={`text-sm mt-2 ${kpi.change >= 0 ? 'text-success' : 'text-error'}`}>
          {kpi.change >= 0 ? <TrendingUp className="inline w-4 h-4 mr-1" /> : <TrendingDown className="inline w-4 h-4 mr-1" />}
          {kpi.change >= 0 ? '+' : ''}{kpi.change.toFixed(1)}%
        </div>
      )}
    </div>
  );

  const renderInsightCard = (insight: Insight, index: number) => {
    const colors = {
      [Severity.CRITICAL]: 'border-l-red-500 bg-red-50 dark:bg-red-900/10',
      [Severity.HIGH]: 'border-l-orange-500 bg-orange-50 dark:bg-orange-900/10',
      [Severity.MEDIUM]: 'border-l-yellow-500 bg-yellow-50 dark:bg-yellow-900/10',
      [Severity.LOW]: 'border-l-green-500 bg-green-50 dark:bg-green-900/10',
    };

    return (
      <div key={index} className={`p-4 rounded-xl border-l-4 ${colors[insight.severity]} mb-4`}>
        <div className="flex items-start gap-3">
          <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
            insight.severity === Severity.CRITICAL ? 'bg-red-100 dark:bg-red-900/30' :
            insight.severity === Severity.HIGH ? 'bg-orange-100 dark:bg-orange-900/30' :
            insight.severity === Severity.MEDIUM ? 'bg-yellow-100 dark:bg-yellow-900/30' :
            'bg-green-100 dark:bg-green-900/30'
          }`}>
            <Lightbulb className={`w-4 h-4 ${
              insight.severity === Severity.CRITICAL ? 'text-red-600 dark:text-red-400' :
              insight.severity === Severity.HIGH ? 'text-orange-600 dark:text-orange-400' :
              insight.severity === Severity.MEDIUM ? 'text-yellow-600 dark:text-yellow-400' :
              'text-green-600 dark:text-green-400'
            }`} />
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <span className={`px-2 py-0.5 rounded-full text-xs font-medium uppercase ${
                insight.severity === Severity.CRITICAL ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400' :
                insight.severity === Severity.HIGH ? 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400' :
                insight.severity === Severity.MEDIUM ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400' :
                'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
              }`}>
                {insight.severity}
              </span>
              <span className="text-xs text-light-textMuted dark:text-dark-textMuted capitalize">
                {insight.category.replace('_', ' ')}
              </span>
            </div>
            <p className="font-medium text-light-text dark:text-dark-text mb-2">{insight.finding}</p>
            <p className="text-sm text-light-textMuted dark:text-dark-textMuted mb-2">
              <span className="font-medium">Impact:</span> {insight.impact}
            </p>
            <p className="text-sm text-primary dark:text-primary-light">
              <span className="font-medium">Action:</span> {insight.action}
            </p>
          </div>
        </div>
      </div>
    );
  };

  const renderRiskCard = (risk: Risk, index: number) => (
    <div key={index} className="risk-card mb-4">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <AlertTriangle className={`w-5 h-5 ${
            risk.severity === Severity.CRITICAL ? 'text-red-500' :
            risk.severity === Severity.HIGH ? 'text-orange-500' :
            risk.severity === Severity.MEDIUM ? 'text-yellow-500' :
            'text-green-500'
          }`} />
          <h4 className="font-semibold text-light-text dark:text-dark-text">{risk.title}</h4>
        </div>
        <span className={`risk-badge ${getSeverityColor(risk.severity)}`}>
          {risk.severity}
        </span>
      </div>
      <p className="text-sm text-light-textMuted dark:text-dark-textMuted mb-3">{risk.description}</p>
      <div className="grid grid-cols-3 gap-4 mb-3 text-sm">
        <div>
          <p className="text-light-textMuted dark:text-dark-textMuted">Probability</p>
          <p className={`font-medium capitalize ${
            risk.probability === 'high' ? 'text-red-500' :
            risk.probability === 'medium' ? 'text-yellow-500' :
            'text-green-500'
          }`}>{risk.probability}</p>
        </div>
        <div>
          <p className="text-light-textMuted dark:text-dark-textMuted">Financial Impact</p>
          <p className="font-medium text-light-text dark:text-dark-text">{risk.financial_impact}</p>
        </div>
        <div>
          <p className="text-light-textMuted dark:text-dark-textMuted">Time to Impact</p>
          <p className="font-medium text-light-text dark:text-dark-text">{risk.time_to_impact}</p>
        </div>
      </div>
      <div className="p-3 rounded-lg bg-light-bg dark:bg-dark-bg">
        <p className="text-sm font-medium text-light-text dark:text-dark-text mb-1">Mitigation</p>
        <p className="text-sm text-light-textMuted dark:text-dark-textMuted">{risk.mitigation}</p>
      </div>
    </div>
  );

  const renderActionCard = (action: Recommendation, index: number) => {
    const colors = {
      [Priority.IMMEDIATE]: 'border-t-red-500',
      [Priority.SHORT_TERM]: 'border-t-orange-500',
      [Priority.MEDIUM_TERM]: 'border-t-green-500',
    };

    return (
      <div key={index} className={`action-card mb-4 border-t-4 ${colors[action.priority]}`}>
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Target className="w-5 h-5 text-primary" />
            <h4 className="font-semibold text-light-text dark:text-dark-text">{action.title}</h4>
          </div>
          <span className={`risk-badge ${getPriorityColor(action.priority)}`}>
            {action.priority.replace('_', ' ')}
          </span>
        </div>
        <p className="text-sm text-light-textMuted dark:text-dark-textMuted mb-3">{action.what}</p>

        <div className="grid grid-cols-2 gap-4 mb-3 text-sm">
          <div>
            <p className="text-light-textMuted dark:text-dark-textMuted">Timeline</p>
            <p className="font-medium text-light-text dark:text-dark-text">{action.timeline}</p>
          </div>
          {action.estimated_savings && (
            <div>
              <p className="text-light-textMuted dark:text-dark-textMuted">Est. Savings</p>
              <p className="font-medium text-success">{formatCurrency(action.estimated_savings)}</p>
            </div>
          )}
        </div>

        <div className="p-3 rounded-lg bg-light-bg dark:bg-dark-bg">
          <p className="text-sm font-medium text-light-text dark:text-dark-text mb-1">Expected Impact</p>
          <p className="text-sm text-light-textMuted dark:text-dark-textMuted">{action.impact}</p>
        </div>
      </div>
    );
  };

  const mainTabs = [
    { id: 'summary', label: 'Summary', icon: <BarChart3 className="w-4 h-4" /> },
    { id: 'insights', label: 'Insights', icon: <Lightbulb className="w-4 h-4" />, count: (
      (financial?.insights?.length || 0) +
      (manufacturing?.insights?.length || 0) +
      (inventory?.insights?.length || 0) +
      (sales?.insights?.length || 0) +
      (purchase?.insights?.length || 0)
    )},
    { id: 'risks', label: 'Risks', icon: <Shield className="w-4 h-4" />, count: critical_risks?.length || 0 },
    { id: 'actions', label: 'Action Plan', icon: <Target className="w-4 h-4" />, count: action_plan?.length || 0 },
  ];

  const chartTabs = [
    { id: 'financial', label: 'Financial', icon: <TrendingUp className="w-4 h-4" /> },
    { id: 'manufacturing', label: 'Manufacturing', icon: <BarChart3 className="w-4 h-4" /> },
    { id: 'inventory', label: 'Inventory', icon: <FileText className="w-4 h-4" /> },
    { id: 'sales', label: 'Sales', icon: <TrendingUp className="w-4 h-4" /> },
    { id: 'purchase', label: 'Purchase', icon: <FileText className="w-4 h-4" /> },
  ];

  // Mock chart data
  const revenueTrendData = [
    { period: 'Jan', revenue: 180000 },
    { period: 'Feb', revenue: 195000 },
    { period: 'Mar', revenue: 210000 },
    { period: 'Apr', revenue: 205000 },
    { period: 'May', revenue: 230000 },
    { period: 'Jun', revenue: 245000 },
  ];

  const marginTrendData = [
    { period: 'Jan', margin: 15.2 },
    { period: 'Feb', margin: 16.5 },
    { period: 'Mar', margin: 17.8 },
    { period: 'Apr', margin: 16.9 },
    { period: 'May', margin: 18.2 },
    { period: 'Jun', margin: 19.1 },
  ];

  const agingData = [
    { bucket: '0-30 days', value: 450000 },
    { bucket: '31-60 days', value: 280000 },
    { bucket: '61-90 days', value: 150000 },
    { bucket: '90+ days', value: 320000 },
  ];

  const efficiencyData = [
    { product: 'Product A', efficiency: 92 },
    { product: 'Product B', efficiency: 78 },
    { product: 'Product C', efficiency: 88 },
    { product: 'Product D', efficiency: 95 },
    { product: 'Product E', efficiency: 65 },
  ];

  const deliveryData = [
    { status: 'On-Time', count: 850 },
    { status: 'Late', count: 50 },
  ];

  const spendData = [
    { supplier: 'Supplier A', spend: 250000 },
    { supplier: 'Supplier B', spend: 180000 },
    { supplier: 'Supplier C', spend: 150000 },
    { supplier: 'Supplier D', spend: 120000 },
    { supplier: 'Supplier E', spend: 90000 },
  ];

  const leadTimeData = [
    { period: 'Jan', lead_time: 9.2 },
    { period: 'Feb', lead_time: 8.8 },
    { period: 'Mar', lead_time: 8.5 },
    { period: 'Apr', lead_time: 9.0 },
    { period: 'May', lead_time: 8.2 },
    { period: 'Jun', lead_time: 8.5 },
  ];

  return (
    <div className="flex min-h-screen">
      <Sidebar />

      <main className="flex-1 ml-64">
        <Header />

        <div className="p-8">
          {/* Page Header */}
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-3xl font-bold text-light-text dark:text-dark-text mb-2">
                Analysis Results
              </h1>
              <p className="text-light-textMuted dark:text-dark-textMuted">
                Generated on {new Date(analysisResults.generated_at).toLocaleDateString()}
              </p>
            </div>
            <div className="flex gap-3">
              <Button variant="secondary">
                <Download className="w-4 h-4 mr-2" />
                Export
              </Button>
              <Link href="/">
                <Button variant="secondary">
                  <RefreshCw className="w-4 h-4 mr-2" />
                  New Analysis
                </Button>
              </Link>
            </div>
          </div>

          {/* Tabs */}
          <Tabs tabs={mainTabs} activeTab={activeTab} onChange={setActiveTab} />

          <div className="mt-6">
            {activeTab === 'summary' && (
              <div className="space-y-6">
                {/* Executive Summary */}
                <Card variant="elevated" padding="lg">
                  <CardHeader title="Executive Summary" />

                  <div className="executive-summary">
                    {executive_summary.map((point, index) => (
                      <div key={index} className="flex items-start gap-3 mb-3 last:mb-0">
                        <CheckCircle className="w-5 h-5 mt-0.5 flex-shrink-0" />
                        <p className="text-white">{point}</p>
                      </div>
                    ))}
                  </div>
                </Card>

                {/* KPI Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {financial?.kpis?.map(renderKPICard)}
                </div>

                {/* Chart Tabs */}
                <Card variant="elevated" padding="lg">
                  <CardHeader title="Visualizations" />

                  <div className="mb-4">
                    <Tabs tabs={chartTabs} activeTab={chartTab} onChange={setChartTab} variant="pills" />
                  </div>

                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {chartTab === 'financial' && (
                      <>
                        <RevenueChart data={revenueTrendData} />
                        <MarginChart data={marginTrendData} />
                      </>
                    )}
                    {chartTab === 'manufacturing' && (
                      <>
                        <EfficiencyChart data={efficiencyData} />
                        <WastageChart data={efficiencyData.map(d => ({ product: d.product, wastage: 100 - d.efficiency }))} />
                      </>
                    )}
                    {chartTab === 'inventory' && (
                      <>
                        <AgingChart data={agingData} />
                        <ParetoChart data={agingData.map(d => ({ category: d.bucket, value: d.value }))} />
                      </>
                    )}
                    {chartTab === 'sales' && (
                      <>
                        <RevenueChart data={revenueTrendData} />
                        <ParetoChart data={[
                          { category: 'Product A', value: 450000 },
                          { category: 'Product B', value: 280000 },
                          { category: 'Product C', value: 180000 },
                          { category: 'Product D', value: 120000 },
                          { category: 'Others', value: 70000 },
                        ]} />
                      </>
                    )}
                    {chartTab === 'purchase' && (
                      <>
                        <SpendChart data={spendData} />
                        <DeliveryChart data={deliveryData} />
                        <LeadTimeChart data={leadTimeData} />
                      </>
                    )}
                  </div>
                </Card>
              </div>
            )}

            {activeTab === 'insights' && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Financial Insights */}
                <Card variant="elevated" padding="lg">
                  <CardHeader
                    title="Financial Insights"
                    subtitle={`${financial?.insights?.length || 0} findings`}
                  />
                  {financial?.insights?.map(renderInsightCard)}
                </Card>

                {/* Manufacturing Insights */}
                <Card variant="elevated" padding="lg">
                  <CardHeader
                    title="Manufacturing Insights"
                    subtitle={`${manufacturing?.insights?.length || 0} findings`}
                  />
                  {manufacturing?.insights?.map(renderInsightCard)}
                </Card>

                {/* Inventory Insights */}
                <Card variant="elevated" padding="lg">
                  <CardHeader
                    title="Inventory Insights"
                    subtitle={`${inventory?.insights?.length || 0} findings`}
                  />
                  {inventory?.insights?.map(renderInsightCard)}
                </Card>

                {/* Sales Insights */}
                <Card variant="elevated" padding="lg">
                  <CardHeader
                    title="Sales Insights"
                    subtitle={`${sales?.insights?.length || 0} findings`}
                  />
                  {sales?.insights?.map(renderInsightCard)}
                </Card>
              </div>
            )}

            {activeTab === 'risks' && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card variant="elevated" padding="lg">
                  <CardHeader
                    title="Critical Risks"
                    subtitle={`${critical_risks?.length || 0} identified risks`}
                  />
                  {critical_risks?.map(renderRiskCard)}
                </Card>

                <Card variant="elevated" padding="lg">
                  <CardHeader title="Risk Overview" />

                  <div className="space-y-4">
                    <div className="p-4 rounded-xl bg-light-bg dark:bg-dark-bg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-light-textMuted dark:text-dark-textMuted">Critical Risks</span>
                        <span className="text-2xl font-bold text-red-500">
                          {critical_risks?.filter(r => r.severity === Severity.CRITICAL).length || 0}
                        </span>
                      </div>
                      <div className="w-full h-2 rounded-full bg-red-100 dark:bg-red-900/30">
                        <div
                          className="h-2 rounded-full bg-red-500"
                          style={{ width: `${((critical_risks?.filter(r => r.severity === Severity.CRITICAL).length || 0) / (critical_risks?.length || 1)) * 100}%` }}
                        />
                      </div>
                    </div>

                    <div className="p-4 rounded-xl bg-light-bg dark:bg-dark-bg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-light-textMuted dark:text-dark-textMuted">High Risks</span>
                        <span className="text-2xl font-bold text-orange-500">
                          {critical_risks?.filter(r => r.severity === Severity.HIGH).length || 0}
                        </span>
                      </div>
                      <div className="w-full h-2 rounded-full bg-orange-100 dark:bg-orange-900/30">
                        <div
                          className="h-2 rounded-full bg-orange-500"
                          style={{ width: `${((critical_risks?.filter(r => r.severity === Severity.HIGH).length || 0) / (critical_risks?.length || 1)) * 100}%` }}
                        />
                      </div>
                    </div>

                    <div className="p-4 rounded-xl bg-light-bg dark:bg-dark-bg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-light-textMuted dark:text-dark-textMuted">Total Financial Exposure</span>
                      </div>
                      <p className="text-3xl font-bold text-light-text dark:text-dark-text">
                        {formatCurrency(
                          critical_risks?.reduce((sum, r) => sum + parseFloat(r.financial_impact.replace(/[^0-9.-]/g, '')), 0) || 0
                        )}
                      </p>
                    </div>
                  </div>
                </Card>
              </div>
            )}

            {activeTab === 'actions' && (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Immediate Actions */}
                <div>
                  <div className="flex items-center gap-2 mb-4">
                    <div className="w-3 h-3 rounded-full bg-red-500" />
                    <h3 className="text-lg font-semibold text-light-text dark:text-dark-text">
                      Immediate (0-30 days)
                    </h3>
                  </div>
                  {action_plan
                    ?.filter(a => a.priority === Priority.IMMEDIATE)
                    .map(renderActionCard)}
                </div>

                {/* Short-term Actions */}
                <div>
                  <div className="flex items-center gap-2 mb-4">
                    <div className="w-3 h-3 rounded-full bg-orange-500" />
                    <h3 className="text-lg font-semibold text-light-text dark:text-dark-text">
                      Short-term (1-3 months)
                    </h3>
                  </div>
                  {action_plan
                    ?.filter(a => a.priority === Priority.SHORT_TERM)
                    .map(renderActionCard)}
                </div>

                {/* Medium-term Actions */}
                <div>
                  <div className="flex items-center gap-2 mb-4">
                    <div className="w-3 h-3 rounded-full bg-green-500" />
                    <h3 className="text-lg font-semibold text-light-text dark:text-dark-text">
                      Medium-term (3-6 months)
                    </h3>
                  </div>
                  {action_plan
                    ?.filter(a => a.priority === Priority.MEDIUM_TERM)
                    .map(renderActionCard)}
                </div>

                {/* Total Impact */}
                <div className="lg:col-span-3">
                  <Card variant="elevated" padding="lg" className="bg-gradient-to-r from-primary to-primary-hover text-white">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-xl font-bold mb-2">Total Expected Impact</h3>
                        <p className="text-white/80">
                          {action_plan?.length || 0} prioritized actions across all timeframes
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="text-4xl font-bold">
                          {formatCurrency(
                            action_plan?.reduce((sum, a) => sum + (a.estimated_savings || 0), 0) || 0
                          )}
                        </p>
                        <p className="text-white/80">Estimated Savings</p>
                      </div>
                    </div>
                  </Card>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
