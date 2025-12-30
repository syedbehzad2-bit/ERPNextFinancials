import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { UploadedFile, AnalysisConfig, AnalysisResults, DataType, Theme } from '@/lib/types';

interface AppState {
  // Theme
  theme: Theme;

  // Files
  uploadedFiles: UploadedFile[];

  // Analysis
  analysisConfig: AnalysisConfig;
  analysisResults: AnalysisResults | null;
  isAnalyzing: boolean;

  // Actions
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;

  addFile: (file: UploadedFile) => void;
  removeFile: (fileId: string) => void;
  clearFiles: () => void;

  setAnalysisConfig: (config: AnalysisConfig) => void;
  setAnalysisResults: (results: AnalysisResults | null) => void;
  setIsAnalyzing: (isAnalyzing: boolean) => void;
  resetAnalysis: () => void;
}

export const useAppStore = create<AppState>()(
  persist(
    (set, get) => ({
      // Initial state
      theme: 'light',
      uploadedFiles: [],
      analysisConfig: {
        analysis_types: {
          financial: true,
          manufacturing: true,
          inventory: true,
          sales: true,
          purchase: true,
        },
        analysis_depth: 'detailed',
        enable_cross_file_analysis: false,
      },
      analysisResults: null,
      isAnalyzing: false,

      // Theme actions
      setTheme: (theme) => set({ theme }),
      toggleTheme: () => set((state) => ({
        theme: state.theme === 'light' ? 'dark' : 'light'
      })),

      // File actions
      addFile: (file) => set((state) => ({
        uploadedFiles: [...state.uploadedFiles, file]
      })),

      removeFile: (fileId) => set((state) => ({
        uploadedFiles: state.uploadedFiles.filter((f) => f.id !== fileId)
      })),

      clearFiles: () => set({ uploadedFiles: [] }),

      // Analysis actions
      setAnalysisConfig: (config) => set({ analysisConfig: config }),
      setAnalysisResults: (results) => set({ analysisResults: results }),
      setIsAnalyzing: (isAnalyzing) => set({ isAnalyzing }),

      resetAnalysis: () => set({
        analysisResults: null,
        isAnalyzing: false,
      }),
    }),
    {
      name: 'erp-agent-storage',
      partialize: (state) => ({
        theme: state.theme,
        uploadedFiles: state.uploadedFiles,
        analysisConfig: state.analysisConfig,
      }),
    }
  )
);

// Selectors
export const selectHasFiles = (state: AppState) => state.uploadedFiles.length > 0;
export const selectFileCount = (state: AppState) => state.uploadedFiles.length;
export const selectDataTypes = (state: AppState) =>
  [...new Set(state.uploadedFiles.map((f) => f.type))] as DataType[];
export const selectHasResults = (state: AppState) => state.analysisResults !== null;
