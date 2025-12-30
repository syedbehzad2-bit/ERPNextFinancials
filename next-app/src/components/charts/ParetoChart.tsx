'use client';

import React from 'react';
import { Bar, Line } from 'react-chartjs-2';
import { createCommonOptions, chartColors } from './chartConfig';
import { Card, CardHeader } from '@/components/ui';

interface ParetoChartProps {
  data: { category: string; value: number }[];
}

export function ParetoChart({ data }: ParetoChartProps) {
  if (!data || data.length === 0) return null;

  const labels = data.map((d) => d.category);
  const values = data.map((d) => d.value);

  // Calculate cumulative percentage
  const total = values.reduce((sum, v) => sum + v, 0);
  let cumsum = 0;
  const cumulative = values.map((v) => {
    cumsum += v;
    return total > 0 ? (cumsum / total) * 100 : 0;
  });

  const chartData = {
    labels,
    datasets: [
      {
        type: 'bar' as const,
        label: 'Value',
        data: values,
        backgroundColor: chartColors.primary,
        borderRadius: 6,
        yAxisID: 'y',
      },
      {
        type: 'line' as const,
        label: 'Cumulative %',
        data: cumulative,
        borderColor: chartColors.success,
        backgroundColor: 'transparent',
        tension: 0.3,
        yAxisID: 'y1',
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom' as const,
      },
      title: {
        display: true,
        text: 'Pareto Analysis (80/20)',
      },
    },
    scales: {
      x: {
        grid: { display: false },
      },
      y: {
        position: 'left' as const,
        grid: { color: '#e2e8f0' },
        title: {
          display: true,
          text: 'Value',
        },
      },
      y1: {
        position: 'right' as const,
        grid: { display: false },
        title: {
          display: true,
          text: 'Cumulative %',
        },
        max: 100,
      },
    },
  };

  return (
    <Card variant="elevated">
      <CardHeader title="Pareto Analysis (80/20)" />
      <div className="h-80">
        {/* @ts-ignore */}
        <Bar data={chartData} options={options} />
      </div>
    </Card>
  );
}
