'use client';

import React from 'react';
import { Bar } from 'react-chartjs-2';
import { createBarOptions } from './chartConfig';
import { chartColors } from './chartConfig';
import { Card, CardHeader } from '@/components/ui';

interface EfficiencyChartProps {
  data: { product: string; efficiency: number }[];
}

export function EfficiencyChart({ data }: EfficiencyChartProps) {
  if (!data || data.length === 0) return null;

  const labels = data.map((d) => d.product);
  const values = data.map((d) => d.efficiency);

  // Color based on efficiency threshold
  const backgroundColor = values.map((v) =>
    v < 70 ? chartColors.error :
    v < 85 ? chartColors.warning :
    chartColors.success
  );

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Efficiency %',
        data: values,
        backgroundColor,
        borderRadius: 6,
      },
    ],
  };

  return (
    <Card variant="elevated">
      <CardHeader title="Production Efficiency by Product" />
      <div className="h-72">
        <Bar data={chartData} options={createBarOptions('') as never} />
      </div>
    </Card>
  );
}
