'use client';

import React from 'react';
import { Doughnut } from 'react-chartjs-2';
import { createDoughnutOptions } from './chartConfig';
import { agingChartColors } from './chartConfig';
import { Card, CardHeader } from '@/components/ui';

interface AgingChartProps {
  data: { bucket: string; value: number }[];
}

export function AgingChart({ data }: AgingChartProps) {
  if (!data || data.length === 0) return null;

  const labels = data.map((d) => d.bucket);
  const values = data.map((d) => d.value);

  const chartData = {
    labels,
    datasets: [
      {
        data: values,
        backgroundColor: agingChartColors.slice(0, data.length),
        borderWidth: 0,
      },
    ],
  };

  return (
    <Card variant="elevated">
      <CardHeader title="Stock Aging Distribution" />
      <div className="h-72">
        <Doughnut data={chartData} options={createDoughnutOptions('') as never} />
      </div>
    </Card>
  );
}
