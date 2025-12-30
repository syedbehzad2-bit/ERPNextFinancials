'use client';

import React from 'react';
import { Line } from 'react-chartjs-2';
import { createLineOptions } from './chartConfig';
import { chartColors } from './chartConfig';
import { Card, CardHeader } from '@/components/ui';

interface LeadTimeChartProps {
  data: { period: string; lead_time: number }[];
}

export function LeadTimeChart({ data }: LeadTimeChartProps) {
  if (!data || data.length === 0) return null;

  const labels = data.map((d) => d.period);
  const values = data.map((d) => d.lead_time);

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Lead Time (days)',
        data: values,
        borderColor: chartColors.warning,
        backgroundColor: 'transparent',
        tension: 0.3,
      },
    ],
  };

  return (
    <Card variant="elevated">
      <CardHeader title="Lead Time Trend" />
      <div className="h-64">
        <Line data={chartData} options={createLineOptions('') as never} />
      </div>
    </Card>
  );
}
