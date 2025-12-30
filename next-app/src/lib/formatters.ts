export function formatCurrency(value: number | null | undefined, compact = false): string {
  if (value === null || value === undefined) return 'N/A';

  if (compact) {
    if (value >= 1000000) {
      return `$${(value / 1000000).toFixed(1)}M`;
    } else if (value >= 1000) {
      return `$${(value / 1000).toFixed(1)}K`;
    }
  }

  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
}

export function formatPercentage(value: number | null | undefined, decimals = 1): string {
  if (value === null || value === undefined) return 'N/A';
  return `${value.toFixed(decimals)}%`;
}

export function formatNumber(value: number | null | undefined, compact = false): string {
  if (value === null || value === undefined) return 'N/A';

  if (compact) {
    if (value >= 1000000) {
      return `${(value / 1000000).toFixed(1)}M`;
    } else if (value >= 1000) {
      return `${(value / 1000).toFixed(1)}K`;
    }
  }

  return new Intl.NumberFormat('en-US').format(value);
}

export function formatChange(value: number | null | undefined): string {
  if (value === null || value === undefined) return '';
  const sign = value >= 0 ? '+' : '';
  return `${sign}${value.toFixed(1)}%`;
}

export function getChangeArrow(value: number | null | undefined): string {
  if (value === null || value === undefined) return '';
  if (value > 0) return '↑';
  if (value < 0) return '↓';
  return '';
}
