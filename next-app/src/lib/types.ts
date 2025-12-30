// Data Types
export enum DataType {
  FINANCIAL = 'financial',
  MANUFACTURING = 'manufacturing',
  INVENTORY = 'inventory',
  SALES = 'sales',
  PURCHASE = 'purchase',
  UNKNOWN = 'unknown'
}

// Severity Levels
export enum Severity {
  CRITICAL = 'critical',
  HIGH = 'high',
  MEDIUM = 'medium',
  LOW = 'low'
}

// Priority Levels
export enum Priority {
  IMMEDIATE = 'immediate',      // 0-30 days
  SHORT_TERM = 'short_term',    // 1-3 months
  MEDIUM_TERM = 'medium_term'   // 3-6 months
}

// Insight Categories
export enum InsightCategory {
  FINANCIAL = 'financial',
  MANUFACTURING = 'manufacturing',
  INVENTORY = 'inventory',
  SALES = 'sales',
  PURCHASE = 'purchase',
  CROSS_DOMAIN = 'cross_domain'
}

// Data Quality
export interface DataQualityIssue {
  column: string;
  issue: string;
  severity: 'warning' | 'error';
  recommendation: string;
}

export interface DataQualityReport {
  total_rows: number;
  total_columns: number;
  missing_values: Record<string, number>;
  duplicate_rows: number;
  issues: DataQualityIssue[];
  is_usable: boolean;
  usable_message: string;
}

// Core Models
export interface Insight {
  category: InsightCategory;
  severity: Severity;
  finding: string;        // "What is wrong - specific and factual"
  impact: string;         // "Why it matters - business consequence"
  action: string;         // "Exact action to take - specific, measurable"
  metrics: Record<string, number | string>;
}

export interface Recommendation {
  id: string;
  title: string;
  what: string;          // Specific action
  why: string;           // Root cause and reason
  how: string;           // Step-by-step implementation
  impact: string;        // Quantified expected outcome
  priority: Priority;
  timeline: string;
  estimated_savings?: number;
  estimated_revenue_impact?: number;
  risk_reduction?: string;
  owner?: string;
  resources_needed?: string[];
}

export interface Risk {
  id: string;
  title: string;
  category: InsightCategory;
  description: string;
  probability: 'high' | 'medium' | 'low';
  financial_impact: string;
  time_to_impact: string;
  severity: Severity;
  mitigation: string;
  early_warning_signals: string[];
}

// Analysis Results
export interface AnalysisKPI {
  label: string;
  value: string | number;
  change?: number;
  isPercentage?: boolean;
}

export interface ChartData {
  type: string;
  data: {
    labels: string[];
    datasets: {
      label: string;
      data: number[];
      backgroundColor?: string | string[];
      borderColor?: string;
      fill?: boolean;
    }[];
  };
  options?: Record<string, unknown>;
}

export interface DomainResults {
  kpis: AnalysisKPI[];
  charts_data: Record<string, ChartData>;
  insights: Insight[];
}

export interface AnalysisResults {
  generated_at: string;
  data_source: string;
  data_types: DataType[];
  data_quality: DataQualityReport;
  executive_summary: string[];

  // Domain-specific results
  financial?: DomainResults;
  manufacturing?: DomainResults;
  inventory?: DomainResults;
  sales?: DomainResults;
  purchase?: DomainResults;

  // Cross-domain
  cross_domain_insights?: Insight[];
  critical_risks: Risk[];
  action_plan: Recommendation[];

  // Raw analysis
  analysis_results: Record<string, unknown>;
}

// File Upload
export interface UploadedFile {
  id: string;
  name: string;
  type: DataType;
  size: number;
  rows: number;
  columns: string[];
  uploadedAt: string;
}

// Analysis Configuration
export interface AnalysisConfig {
  analysis_types: {
    financial: boolean;
    manufacturing: boolean;
    inventory: boolean;
    sales: boolean;
    purchase: boolean;
  };
  analysis_depth: 'summary' | 'detailed' | 'comprehensive';
  enable_cross_file_analysis: boolean;
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export interface UploadResponse extends ApiResponse<{
  files: UploadedFile[];
  quality_report: Record<string, DataQualityReport>;
}> {}

export interface AnalyzeResponse extends ApiResponse<AnalysisResults> {}

// Theme
export type Theme = 'light' | 'dark';
