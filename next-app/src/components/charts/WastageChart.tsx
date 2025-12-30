'use client';

import React from 'react';
import { Bar } from 'react-chartjs-2';
import { createBarOptions } from './chartConfig';
import { chartColors } from './chartConfig';
import { Card, CardHeader } from '@/components/ui';

interface WastageChartProps {
  data: { product: string; wastage: number }[];
}

export function WastageChart({ data }: WastageChartProps) {
  if (!data || data.length === 0) return null;

  const labels = data.map((d) => d.product);
  const values = data.map((d) => d.wastage);

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Wastage',
        data: values,
        backgroundColor: chartColors.error,
        borderRadius: 6,
      },
    ],
  };

  return (
    <Card variant="elevated">
      <CardHeader title="Wastage by Product" />
      <div className="h-72">
        <Bar data={chartData} options={createBarOptions('', true) as never} />
      </div>
    </Card>
  );
}
