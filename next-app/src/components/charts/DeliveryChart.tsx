'use client';

import React from 'react';
import { Doughnut } from 'react-chartjs-2';
import { createDoughnutOptions } from './chartConfig';
import { deliveryChartColors } from './chartConfig';
import { Card, CardHeader } from '@/components/ui';

interface DeliveryChartProps {
  data: { status: string; count: number }[];
}

export function DeliveryChart({ data }: DeliveryChartProps) {
  if (!data || data.length === 0) return null;

  const labels = data.map((d) => d.status);
  const values = data.map((d) => d.count);

  const chartData = {
    labels,
    datasets: [
      {
        data: values,
        backgroundColor: deliveryChartColors.slice(0, data.length),
        borderWidth: 0,
      },
    ],
  };

  return (
    <Card variant="elevated">
      <CardHeader title="Delivery Performance" />
      <div className="h-64">
        <Doughnut data={chartData} options={createDoughnutOptions('') as never} />
      </div>
    </Card>
  );
}
