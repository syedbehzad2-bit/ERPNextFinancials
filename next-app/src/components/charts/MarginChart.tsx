'use client';

import React from 'react';
import { Line } from 'react-chartjs-2';
import { createLineOptions } from './chartConfig';
import { chartColors } from './chartConfig';
import { Card, CardHeader } from '@/components/ui';

interface MarginChartProps {
  data: { period: string; margin: number }[];
}

export function MarginChart({ data }: MarginChartProps) {
  if (!data || data.length === 0) return null;

  const labels = data.map((d) => d.period);
  const values = data.map((d) => d.margin);

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Margin %',
        data: values,
        borderColor: chartColors.success,
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        fill: true,
      },
    ],
  };

  return (
    <Card variant="elevated">
      <CardHeader title="Margin Trend (%)" />
      <div className="h-72">
        <Line data={chartData} options={createLineOptions('') as never} />
      </div>
    </Card>
  );
}
