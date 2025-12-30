'use client';

import React from 'react';
import { Bar } from 'react-chartjs-2';
import { createBarOptions } from './chartConfig';
import { chartColors } from './chartConfig';
import { Card, CardHeader } from '@/components/ui';

interface SpendChartProps {
  data: { supplier: string; spend: number }[];
}

export function SpendChart({ data }: SpendChartProps) {
  if (!data || data.length === 0) return null;

  const labels = data.map((d) => d.supplier);
  const values = data.map((d) => d.spend);

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Spend',
        data: values,
        backgroundColor: chartColors.info,
        borderRadius: 6,
      },
    ],
  };

  return (
    <Card variant="elevated">
      <CardHeader title="Spend by Supplier" />
      <div className="h-72">
        <Bar data={chartData} options={createBarOptions('', true) as never} />
      </div>
    </Card>
  );
}
