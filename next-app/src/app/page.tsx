'use client';

import React, { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import {
  Upload,
  FileText,
  X,
  Download,
  FileSpreadsheet,
  FileBarChart,
  Package,
  ShoppingCart,
  TrendingUp,
  ChevronRight,
  Plus,
} from 'lucide-react';
import { Button, Card, CardHeader } from '@/components/ui';
import { Sidebar, Header } from '@/components/layout';
import { useAppStore } from '@/store/useAppStore';
import { DataType, UploadedFile } from '@/lib/types';
import { formatNumber } from '@/lib/formatters';

export default function UploadPage() {
  const router = useRouter();
  const {
    uploadedFiles,
    addFile,
    removeFile,
    clearFiles,
    analysisConfig,
    setAnalysisConfig,
  } = useAppStore();

  const [isDragOver, setIsDragOver] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  const getDataTypeIcon = (type: DataType) => {
    const icons = {
      [DataType.FINANCIAL]: <TrendingUp className="w-5 h-5" />,
      [DataType.MANUFACTURING]: <FileBarChart className="w-5 h-5" />,
      [DataType.INVENTORY]: <Package className="w-5 h-5" />,
      [DataType.SALES]: <TrendingUp className="w-5 h-5" />,
      [DataType.PURCHASE]: <ShoppingCart className="w-5 h-5" />,
      [DataType.UNKNOWN]: <FileText className="w-5 h-5" />,
    };
    return icons[type] || icons[DataType.UNKNOWN];
  };

  const getDataTypeColor = (type: DataType) => {
    const colors = {
      [DataType.FINANCIAL]: 'from-green-500 to-emerald-600',
      [DataType.MANUFACTURING]: 'from-blue-500 to-indigo-600',
      [DataType.INVENTORY]: 'from-amber-500 to-orange-600',
      [DataType.SALES]: 'from-purple-500 to-violet-600',
      [DataType.PURCHASE]: 'from-rose-500 to-pink-600',
      [DataType.UNKNOWN]: 'from-gray-500 to-slate-600',
    };
    return colors[type] || colors[DataType.UNKNOWN];
  };

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback(async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);

    const files = Array.from(e.dataTransfer.files);
    await handleFiles(files);
  }, []);

  const handleFileInput = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files ? Array.from(e.target.files) : [];
    await handleFiles(files);
  };

  const handleFiles = async (files: File[]) => {
    setIsUploading(true);

    for (const file of files) {
      // Simulate file processing
      await new Promise((resolve) => setTimeout(resolve, 500));

      // Detect data type based on filename
      const name = file.name.toLowerCase();
      let type = DataType.UNKNOWN;

      if (name.includes('financial') || name.includes('revenue') || name.includes('pl')) {
        type = DataType.FINANCIAL;
      } else if (name.includes('manufacturing') || name.includes('production')) {
        type = DataType.MANUFACTURING;
      } else if (name.includes('inventory') || name.includes('stock')) {
        type = DataType.INVENTORY;
      } else if (name.includes('sales') || name.includes('order')) {
        type = DataType.SALES;
      } else if (name.includes('purchase') || name.includes('supplier')) {
        type = DataType.PURCHASE;
      }

      const uploadedFile: UploadedFile = {
        id: Math.random().toString(36).substr(2, 9),
        name: file.name,
        type,
        size: file.size,
        rows: Math.floor(Math.random() * 1000) + 100,
        columns: ['column1', 'column2', 'column3', 'column4', 'column5'],
        uploadedAt: new Date().toISOString(),
      };

      addFile(uploadedFile);
    }

    setIsUploading(false);
  };

  const handleRunAnalysis = () => {
    router.push('/analysis');
  };

  const templates = [
    { name: 'Financial Template', type: DataType.FINANCIAL, desc: 'P&L, Revenue, Expenses' },
    { name: 'Manufacturing Template', type: DataType.MANUFACTURING, desc: 'Production, Wastage, Efficiency' },
    { name: 'Inventory Template', type: DataType.INVENTORY, desc: 'Stock levels, Aging, Turnover' },
    { name: 'Sales Template', type: DataType.SALES, desc: 'Orders, Revenue, Customers' },
    { name: 'Purchase Template', type: DataType.PURCHASE, desc: 'Suppliers, Lead times' },
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
              Upload Data
            </h1>
            <p className="text-light-textMuted dark:text-dark-textMuted">
              Upload your ERP data files for analysis. We support CSV and Excel formats.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Upload Area */}
            <div className="lg:col-span-2">
              <Card variant="elevated">
                <CardHeader
                  title="Drop Files Here"
                  subtitle="or click to browse"
                />

                <div
                  className={`dropzone ${isDragOver ? 'active' : ''}`}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  onClick={() => document.getElementById('fileInput')?.click()}
                >
                  <input
                    id="fileInput"
                    type="file"
                    multiple
                    accept=".csv,.xlsx,.xls"
                    onChange={handleFileInput}
                    className="hidden"
                  />

                  <div className="flex flex-col items-center">
                    <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${isDragOver ? 'from-primary to-primary-hover' : 'from-gray-100 to-gray-200 dark:from-dark-bg dark:to-dark-surface'} flex items-center justify-center mb-4 transition-all duration-300`}>
                      <Upload className={`w-8 h-8 ${isDragOver ? 'text-white' : 'text-light-textMuted dark:text-dark-textMuted'}`} />
                    </div>
                    <p className="text-lg font-medium text-light-text dark:text-dark-text mb-1">
                      {isUploading ? 'Uploading...' : 'Drag & drop your files here'}
                    </p>
                    <p className="text-sm text-light-textMuted dark:text-dark-textMuted">
                      Supports CSV, Excel files up to 50MB
                    </p>
                  </div>
                </div>

                {/* File List */}
                {uploadedFiles.length > 0 && (
                  <div className="mt-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-semibold text-light-text dark:text-dark-text">
                        Uploaded Files ({uploadedFiles.length})
                      </h3>
                      <button
                        onClick={clearFiles}
                        className="text-sm text-error hover:text-errorLight transition-colors"
                      >
                        Clear All
                      </button>
                    </div>

                    <div className="space-y-3">
                      {uploadedFiles.map((file) => (
                        <div
                          key={file.id}
                          className="flex items-center gap-4 p-4 rounded-xl bg-light-bg dark:bg-dark-bg border border-light-border dark:border-dark-border"
                        >
                          <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${getDataTypeColor(file.type)} flex items-center justify-center`}>
                            {getDataTypeIcon(file.type)}
                          </div>

                          <div className="flex-1 min-w-0">
                            <p className="font-medium text-light-text dark:text-dark-text truncate">
                              {file.name}
                            </p>
                            <p className="text-sm text-light-textMuted dark:text-dark-textMuted">
                              {formatNumber(file.rows)} rows | {file.columns.length} columns | {(file.size / 1024).toFixed(1)} KB
                            </p>
                          </div>

                          <span className={`px-3 py-1 rounded-full text-xs font-medium bg-gradient-to-r ${getDataTypeColor(file.type)} text-white`}>
                            {file.type}
                          </span>

                          <button
                            onClick={() => removeFile(file.id)}
                            className="p-2 rounded-lg hover:bg-light-surface dark:hover:bg-dark-surface transition-colors"
                          >
                            <X className="w-5 h-5 text-light-textMuted dark:text-dark-textMuted" />
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </Card>
            </div>

            {/* Templates Sidebar */}
            <div>
              <Card variant="elevated" padding="lg">
                <CardHeader
                  title="Download Templates"
                  subtitle="Use these templates for your data"
                />

                <div className="space-y-3">
                  {templates.map((template) => (
                    <button
                      key={template.type}
                      className="w-full flex items-center gap-3 p-3 rounded-xl bg-light-bg dark:bg-dark-bg border border-light-border dark:border-dark-border hover:border-primary transition-colors text-left"
                    >
                      <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${getDataTypeColor(template.type)} flex items-center justify-center flex-shrink-0`}>
                        <Download className="w-5 h-5 text-white" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-medium text-light-text dark:text-dark-text text-sm">
                          {template.name}
                        </p>
                        <p className="text-xs text-light-textMuted dark:text-dark-textMuted truncate">
                          {template.desc}
                        </p>
                      </div>
                      <ChevronRight className="w-4 h-4 text-light-textMuted dark:text-dark-textMuted" />
                    </button>
                  ))}
                </div>

                {/* Analysis Options */}
                <div className="mt-6 pt-6 border-t border-light-border dark:border-dark-border">
                  <h4 className="font-semibold text-light-text dark:text-dark-text mb-4">
                    Analysis Options
                  </h4>

                  <div className="space-y-3">
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
                      <span className="text-sm text-light-text dark:text-dark-text">
                        Enable cross-file analysis
                      </span>
                    </label>

                    <label className="flex items-center gap-3 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={analysisConfig.analysis_types.financial}
                        onChange={(e) => setAnalysisConfig({
                          ...analysisConfig,
                          analysis_types: { ...analysisConfig.analysis_types, financial: e.target.checked },
                        })}
                        className="w-5 h-5 rounded border-light-border dark:border-dark-border text-primary focus:ring-primary"
                      />
                      <span className="text-sm text-light-text dark:text-dark-text">
                        Financial Analysis
                      </span>
                    </label>

                    <label className="flex items-center gap-3 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={analysisConfig.analysis_types.manufacturing}
                        onChange={(e) => setAnalysisConfig({
                          ...analysisConfig,
                          analysis_types: { ...analysisConfig.analysis_types, manufacturing: e.target.checked },
                        })}
                        className="w-5 h-5 rounded border-light-border dark:border-dark-border text-primary focus:ring-primary"
                      />
                      <span className="text-sm text-light-text dark:text-dark-text">
                        Manufacturing Analysis
                      </span>
                    </label>

                    <label className="flex items-center gap-3 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={analysisConfig.analysis_types.inventory}
                        onChange={(e) => setAnalysisConfig({
                          ...analysisConfig,
                          analysis_types: { ...analysisConfig.analysis_types, inventory: e.target.checked },
                        })}
                        className="w-5 h-5 rounded border-light-border dark:border-dark-border text-primary focus:ring-primary"
                      />
                      <span className="text-sm text-light-text dark:text-dark-text">
                        Inventory Analysis
                      </span>
                    </label>

                    <label className="flex items-center gap-3 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={analysisConfig.analysis_types.sales}
                        onChange={(e) => setAnalysisConfig({
                          ...analysisConfig,
                          analysis_types: { ...analysisConfig.analysis_types, sales: e.target.checked },
                        })}
                        className="w-5 h-5 rounded border-light-border dark:border-dark-border text-primary focus:ring-primary"
                      />
                      <span className="text-sm text-light-text dark:text-dark-text">
                        Sales Analysis
                      </span>
                    </label>

                    <label className="flex items-center gap-3 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={analysisConfig.analysis_types.purchase}
                        onChange={(e) => setAnalysisConfig({
                          ...analysisConfig,
                          analysis_types: { ...analysisConfig.analysis_types, purchase: e.target.checked },
                        })}
                        className="w-5 h-5 rounded border-light-border dark:border-dark-border text-primary focus:ring-primary"
                      />
                      <span className="text-sm text-light-text dark:text-dark-text">
                        Purchase Analysis
                      </span>
                    </label>
                  </div>
                </div>

                {/* Run Analysis Button */}
                <div className="mt-6">
                  <Button
                    onClick={handleRunAnalysis}
                    disabled={uploadedFiles.length === 0}
                    className="w-full"
                    size="lg"
                  >
                    <span className="flex items-center gap-2">
                      Configure Analysis
                      <ChevronRight className="w-5 h-5" />
                    </span>
                  </Button>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
