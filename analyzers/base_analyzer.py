"""
Abstract base analyzer - enforces insight format (finding + impact + action).
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from decimal import Decimal

import pandas as pd
import numpy as np

from models.analysis_output import AnalysisResult, Insight, KPI
from models.base import InsightCategory, Severity


class BaseAnalyzer(ABC):
    """
    Abstract base class for all analyzers.

    Every insight MUST have:
    - finding: What is wrong (specific, with numbers)
    - impact: Why it matters (business consequence)
    - action: Exact action to take (specific, measurable)
    """

    def __init__(self, data: pd.DataFrame, config: Optional[Dict] = None):
        self.data = data.copy()
        self.config = config or {}
        self._results: Optional[AnalysisResult] = None

    @abstractmethod
    def analyze(self) -> AnalysisResult:
        """Run full analysis and return structured results."""
        pass

    @abstractmethod
    def calculate_kpis(self) -> Dict[str, Any]:
        """Calculate domain-specific KPIs."""
        pass

    @abstractmethod
    def get_category(self) -> InsightCategory:
        """Get the insight category for this analyzer."""
        pass

    # Shared analysis methods

    def trend_analysis(
        self,
        value_col: str,
        date_col: str = 'date',
        period: str = 'M'
    ) -> Dict[str, Any]:
        """
        Perform MoM/QoQ trend analysis.

        Returns: trend direction, percentage change, anomalies
        """
        if date_col not in self.data.columns or value_col not in self.data.columns:
            return {'error': 'Required columns missing'}

        df = self.data.copy()
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col)

        # Resample by period
        period_map = {'D': 'D', 'W': 'W', 'M': 'ME', 'Q': 'QE', 'Y': 'YE'}
        freq = period_map.get(period, 'ME')

        try:
            time_series = df.groupby(pd.Grouper(key=date_col, freq=freq))[value_col].sum()
            time_series = time_series.dropna()

            if len(time_series) < 2:
                return {'error': 'Insufficient data for trend analysis'}

            # Calculate changes
            latest = time_series.iloc[-1]
            prior = time_series.iloc[-2] if len(time_series) >= 2 else latest
            mom_change = ((latest - prior) / prior * 100) if prior != 0 else 0

            if len(time_series) >= 3:
                recent_avg = time_series.iloc[-3:].mean()
                prior_avg = time_series.iloc[:-3].mean() if len(time_series) > 3 else recent_avg
                qoq_change = ((recent_avg - prior_avg) / prior_avg * 100) if prior_avg != 0 else 0
            else:
                qoq_change = mom_change

            # Calculate trend
            if mom_change > 5:
                trend = 'rising'
            elif mom_change < -5:
                trend = 'falling'
            else:
                trend = 'stable'

            # Detect anomalies (values > 2 std from mean)
            mean_val = time_series.mean()
            std_val = time_series.std()
            anomalies = time_series[abs(time_series - mean_val) > 2 * std_val].to_dict()

            return {
                'current_value': float(latest),
                'prior_value': float(prior),
                'mom_change_pct': round(float(mom_change), 2),
                'qoq_change_pct': round(float(qoq_change), 2),
                'trend': trend,
                'anomalies': anomalies,
                'data_points': len(time_series)
            }
        except Exception as e:
            return {'error': str(e)}

    def variance_analysis(
        self,
        actual_col: str,
        planned_col: str,
        group_by: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compare planned vs actual values.

        Returns: variance amount, variance %, materiality flag
        """
        if actual_col not in self.data.columns or planned_col not in self.data.columns:
            return {'error': 'Required columns missing'}

        df = self.data.copy()

        # Calculate variance
        df['variance'] = df[actual_col] - df[planned_col]
        df['variance_pct'] = (df['variance'] / df[planned_col] * 100).replace([np.inf, -np.inf], 0)

        if group_by and group_by in df.columns:
            # Group analysis
            grouped = df.groupby(group_by).agg({
                actual_col: 'sum',
                planned_col: 'sum',
                'variance': 'sum'
            }).reset_index()
            grouped['variance_pct'] = (grouped['variance'] / grouped[planned_col] * 100)
        else:
            grouped = df

        # Overall variance
        total_actual = df[actual_col].sum()
        total_planned = df[planned_col].sum()
        total_variance = total_actual - total_planned
        total_variance_pct = (total_variance / total_planned * 100) if total_planned != 0 else 0

        # Find biggest overruns
        overruns = df[df['variance'] > 0].nlargest(5, 'variance')

        return {
            'total_actual': float(total_actual),
            'total_planned': float(total_planned),
            'total_variance': float(total_variance),
            'total_variance_pct': round(float(total_variance_pct), 2),
            'is_over_budget': total_variance > 0,
            'material_variance': abs(total_variance_pct) > 10,
            'top_overruns': overruns[[group_by or actual_col, 'variance', 'variance_pct']].to_dict('records') if len(overruns) > 0 else []
        }

    def pareto_analysis(
        self,
        category_col: str,
        value_col: str,
        top_n: int = 10
    ) -> Dict[str, Any]:
        """
        Apply 80/20 Pareto analysis.

        Returns: top contributors, concentration metrics
        """
        if category_col not in self.data.columns or value_col not in self.data.columns:
            return {'error': 'Required columns missing'}

        df = self.data.copy()

        # Aggregate by category
        agg = df.groupby(category_col)[value_col].sum().sort_values(ascending=False)
        total = agg.sum()

        if total == 0:
            return {'error': 'Total value is zero'}

        # Calculate cumulative percentage
        cumulative = agg.cumsum()
        cumulative_pct = (cumulative / total * 100)

        # Find the number of items contributing to 80%
        items_for_80 = (cumulative_pct <= 80).sum() + 1
        items_for_80 = min(items_for_80, len(agg))

        # Calculate concentration
        top_20_pct = agg.head(int(len(agg) * 0.2)).sum() if len(agg) > 5 else agg.head(1).sum()
        top_20_contribution = (top_20_pct / total * 100) if total > 0 else 0

        # Top contributors
        top_contributors = []
        for i, (cat, val) in enumerate(agg.head(top_n).items()):
            top_contributors.append({
                'rank': i + 1,
                'category': cat,
                'value': float(val),
                'contribution_pct': round(float(val / total * 100), 2),
                'cumulative_pct': round(float(cumulative_pct[cat]), 2)
            })

        return {
            'total_value': float(total),
            'items_for_80_pct': items_for_80,
            'items_for_80_contribution': round(float(agg.head(items_for_80).sum() / total * 100), 2),
            'top_20_contribution_pct': round(float(top_20_contribution), 2),
            'concentration': 'HIGH' if top_20_contribution > 80 else 'MEDIUM' if top_20_contribution > 60 else 'LOW',
            'top_contributors': top_contributors,
            'full_pareto': [{'category': str(k), 'value': float(v), 'cumulative_pct': round(float(cumulative_pct[k]), 2)}
                           for k, v in agg.items()]
        }

    def ratio_analysis(
        self,
        numerator_col: str,
        denominator_col: str,
        ratio_name: str
    ) -> Dict[str, Any]:
        """
        Calculate ratio analysis.

        Returns: ratio value, trend, benchmark comparison
        """
        if numerator_col not in self.data.columns or denominator_col not in self.data.columns:
            return {'error': 'Required columns missing'}

        df = self.data.copy()

        # Calculate ratio
        df['ratio'] = df[numerator_col] / df[denominator_col].replace(0, np.nan)
        ratio = df['ratio'].dropna()

        if len(ratio) == 0:
            return {'error': 'Could not calculate ratio'}

        return {
            'ratio_name': ratio_name,
            'current_value': round(float(ratio.iloc[-1]), 4) if len(ratio) > 0 else 0,
            'average_value': round(float(ratio.mean()), 4),
            'min_value': round(float(ratio.min()), 4),
            'max_value': round(float(ratio.max()), 4),
            'data_points': len(ratio)
        }

    def _create_insight(
        self,
        severity: Severity,
        finding: str,
        impact: str,
        action: str,
        metrics: Optional[Dict[str, Any]] = None
    ) -> Insight:
        """Create a properly formatted insight."""
        return Insight(
            category=self.get_category(),
            severity=severity,
            finding=finding,
            impact=impact,
            action=action,
            metrics=metrics
        )

    def _format_currency(self, value: float) -> str:
        """Format number as currency."""
        if abs(value) >= 1_000_000:
            return f"${value / 1_000_000:.1f}M"
        elif abs(value) >= 1_000:
            return f"${value / 1_000:.1f}K"
        else:
            return f"${value:,.0f}"

    def _format_pct(self, value: float) -> str:
        """Format number as percentage."""
        return f"{value:.1f}%"
