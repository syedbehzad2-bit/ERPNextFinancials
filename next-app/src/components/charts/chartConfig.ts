'use client';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  ChartOptions,
} from 'chart.js';
import { useTheme } from '@/components/theme/ThemeProvider';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

// Theme-aware colors
export function getChartColors() {
  const { theme } = useTheme();
  const isDark = theme === 'dark';

  return {
    text: isDark ? '#94a3b8' : '#64748b',
    grid: isDark ? '#334155' : '#e2e8f0',
    primary: '#6366f1',
    primaryLight: '#818cf8',
    success: '#10b981',
    successLight: '#34d399',
    warning: '#f59e0b',
    warningLight: '#fbbf24',
    error: '#ef4444',
    errorLight: '#f87171',
    background: isDark ? '#1e293b' : '#ffffff',
  };
}

// Common chart options factory
export function createCommonOptions(
  title: string,
  options: Partial<ChartOptions<'line' | 'bar' | 'pie' | 'doughnut'>> = {}
): ChartOptions {
  const colors = getChartColors();

  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          color: colors.text,
          usePointStyle: true,
          padding: 20,
        },
      },
      title: {
        display: true,
        text: title,
        color: colors.text,
        font: {
          size: 16,
          weight: '600' as const,
        },
      },
    },
    scales: {
      x: {
        grid: {
          color: colors.grid,
        },
        ticks: {
          color: colors.text,
        },
      },
      y: {
        grid: {
          color: colors.grid,
        },
        ticks: {
          color: colors.text,
        },
      },
    },
    ...options,
  };
}

// Line chart options
export function createLineOptions(title: string): ChartOptions<'line'> {
  const colors = getChartColors();

  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          color: colors.text,
          usePointStyle: true,
        },
      },
      title: {
        display: true,
        text: title,
        color: colors.text,
        font: { size: 16, weight: '600' as const },
      },
    },
    scales: {
      x: {
        grid: { color: colors.grid },
        ticks: { color: colors.text },
      },
      y: {
        grid: { color: colors.grid },
        ticks: { color: colors.text },
      },
    },
    elements: {
      line: {
        tension: 0.4,
      },
      point: {
        radius: 4,
        hoverRadius: 6,
      },
    },
  };
}

// Bar chart options
export function createBarOptions(title: string, horizontal = false): ChartOptions<'bar'> {
  const colors = getChartColors();

  return {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: horizontal ? 'y' as const : 'x' as const,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: title,
        color: colors.text,
        font: { size: 16, weight: '600' as const },
      },
    },
    scales: {
      x: {
        grid: { display: horizontal },
        ticks: { color: colors.text },
      },
      y: {
        grid: { color: colors.grid },
        ticks: { color: colors.text },
      },
    },
  };
}

// Doughnut/Pie chart options
export function createDoughnutOptions(title: string): ChartOptions<'doughnut'> {
  const colors = getChartColors();

  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right' as const,
        labels: {
          color: colors.text,
          usePointStyle: true,
          padding: 15,
        },
      },
      title: {
        display: true,
        text: title,
        color: colors.text,
        font: { size: 16, weight: '600' as const },
      },
    },
    cutout: '60%',
  };
}

// Chart colors palette
export const chartColors = {
  primary: '#6366f1',
  primaryLight: '#818cf8',
  success: '#10b981',
  successLight: '#34d399',
  warning: '#f59e0b',
  warningLight: '#fbbf24',
  error: '#ef4444',
  errorLight: '#f87171',
  info: '#3b82f6',
  infoLight: '#60a5fa',
  purple: '#8b5cf6',
  teal: '#14b8a6',
  pink: '#ec4899',
  gray: '#6b7280',
};

export const agingChartColors = ['#00c896', '#4ecdc4', '#45b7d1', '#e94560'];
export const deliveryChartColors = ['#00c896', '#e94560'];
