'use client';

import React from 'react';
import { Line } from 'react-chartjs-2';
import { createLineOptions } from './chartConfig';
import { chartColors } from './chartConfig';
import { Card, CardHeader } from '@/components/ui';

interface RevenueChartProps {
  data: { period: string; revenue: number }[];
}

export function RevenueChart({ data }: RevenueChartProps) {
  if (!data || data.length === 0) return null;

  const labels = data.map((d) => d.period);
  const values = data.map((d) => d.revenue);

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Revenue',
        data: values,
        borderColor: chartColors.primary,
        backgroundColor: 'rgba(99, 102, 241, 0.1)',
        fill: true,
      },
    ],
  };

  return (
    <Card variant="elevated">
      <CardHeader title="Revenue Trend" />
      <div className="h-72">
        <Line data={chartData} options={createLineOptions('') as never} />
      </div>
    </Card>
  );
}
