"""
Manufacturing analyzer - Production, Wastage, Cost per Unit analysis.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List

from analyzers.base_analyzer import BaseAnalyzer
from models.analysis_output import AnalysisResult, Insight
from models.base import InsightCategory, Severity


class ManufacturingAnalyzer(BaseAnalyzer):
    """
    Analyzes production efficiency, wastage, and cost per unit.
    Every insight has specific numbers and exact actions.
    """

    def get_category(self) -> InsightCategory:
        return InsightCategory.MANUFACTURING

    def analyze(self) -> AnalysisResult:
        """Run complete manufacturing analysis."""
        kpis = self.calculate_kpis()
        insights = []

        # Production efficiency
        efficiency_insights = self._analyze_production_efficiency()
        insights.extend(efficiency_insights)

        # Wastage analysis
        wastage_insights = self._analyze_wastage()
        insights.extend(wastage_insights)

        # Cost per unit analysis
        cost_insights = self._analyze_cost_per_unit()
        insights.extend(cost_insights)

        # Yield analysis
        yield_insights = self._analyze_yield()
        insights.extend(yield_insights)

        # Production trends
        trend_insights = self._analyze_production_trends()
        insights.extend(trend_insights)

        # Charts data
        charts_data = self._generate_charts_data(kpis)

        return AnalysisResult(
            domain="manufacturing",
            kpis=kpis,
            insights=insights,
            charts_data=charts_data
        )

    def calculate_kpis(self) -> Dict[str, Any]:
        """Calculate manufacturing KPIs."""
        df = self.data.copy()

        # Get or calculate quantities
        planned = df['planned_quantity'].sum() if 'planned_quantity' in df.columns else 0
        actual = df['actual_quantity'].sum() if 'actual_quantity' in df.columns else 0
        good = df['good_quantity'].sum() if 'good_quantity' in df.columns else actual
        rejected = df.get('rejected_quantity', pd.Series([0])).sum()
        wastage = df.get('wastage_quantity', pd.Series([0])).sum()

        # Efficiency
        efficiency = (actual / planned * 100) if planned > 0 else 0

        # Yield
        yield_rate = (good / actual * 100) if actual > 0 else 0

        # Rejection and wastage rates
        rejection_rate = (rejected / actual * 100) if actual > 0 else 0
        wastage_rate = (wastage / actual * 100) if actual > 0 else 0

        # Cost per unit
        if 'total_cost' in df.columns:
            total_cost = df['total_cost'].sum()
            cost_per_unit = total_cost / actual if actual > 0 else 0
        else:
            cost_per_unit = 0
            total_cost = 0

        return {
            'total_planned_quantity': int(planned),
            'total_actual_quantity': int(actual),
            'total_good_quantity': int(good),
            'production_efficiency_pct': round(float(efficiency), 2),
            'yield_rate_pct': round(float(yield_rate), 2),
            'rejection_rate_pct': round(float(rejection_rate), 2),
            'wastage_rate_pct': round(float(wastage_rate), 2),
            'total_production_cost': float(total_cost),
            'cost_per_unit': round(float(cost_per_unit), 2),
            'shortfall_units': int(planned - actual) if planned > actual else 0
        }

    def _analyze_production_efficiency(self) -> List[Insight]:
        """Analyze production efficiency vs planned."""
        insights = []
        df = self.data.copy()

        if 'planned_quantity' not in df.columns or 'actual_quantity' not in df.columns:
            return insights

        # Calculate efficiency
        df['efficiency'] = df['actual_quantity'] / df['planned_quantity'] * 100

        # Overall efficiency
        total_planned = df['planned_quantity'].sum()
        total_actual = df['actual_quantity'].sum()
        overall_efficiency = total_actual / total_planned * 100 if total_planned > 0 else 0

        if overall_efficiency < 85:
            shortfall = total_planned - total_actual
            # Find worst performing products/lines
            if 'product_name' in df.columns:
                by_product = df.groupby('product_name').agg({
                    'planned_quantity': 'sum',
                    'actual_quantity': 'sum',
                    'efficiency': 'mean'
                }).sort_values('efficiency')
                worst_products = by_product.head(3)

                worst_str = ", ".join([f"{name} ({row['efficiency']:.0f}%)"
                                       for name, row in worst_products.iterrows()])

                # Estimate revenue impact
                revenue_impact = shortfall * 50  # Assume $50 avg unit value

                insights.append(self._create_insight(
                    severity=Severity.HIGH,
                    finding=f"Production efficiency at {overall_efficiency:.1f}% (target: 95%). Shortfall: {shortfall:,} units. Worst: {worst_str}",
                    impact=f"Lost production = lost revenue opportunity. Estimated revenue loss: ${revenue_impact:,.0f} (assuming $50 avg unit value)",
                    action=f"IMMEDIATE (Week 1): Root cause analysis on worst 3 products. Check: equipment downtime, material supply issues, staffing. Set 90% efficiency target for next month. Week 2: Implement daily production standups to track and address issues immediately."
                ))

        # By production line
        if 'production_line' in df.columns:
            by_line = df.groupby('production_line').agg({
                'planned_quantity': 'sum',
                'actual_quantity': 'sum',
                'efficiency': 'mean'
            }).sort_values('efficiency')

            low_efficiency_lines = by_line[by_line['efficiency'] < 80]
            if len(low_efficiency_lines) > 0:
                worst_line = low_efficiency_lines.index[0]
                worst_efficiency = low_efficiency_lines.iloc[0]['efficiency']

                insights.append(self._create_insight(
                    severity=Severity.MEDIUM,
                    finding=f"Production line '{worst_line}' operating at only {worst_efficiency:.1f}% efficiency",
                    impact=f"Line underperforming by {(80 - worst_efficiency):.0f} percentage points. Capacity wasted.",
                    action=f"Analyze line '{worst_line}': (1) Check equipment OEE, (2) Review operator training, (3) Audit material flow. Target 15% improvement within 30 days."
                ))

        return insights

    def _analyze_wastage(self) -> List[Insight]:
        """Analyze wastage rates and costs."""
        insights = []
        df = self.data.copy()

        if 'wastage_quantity' not in df.columns and 'rejected_quantity' not in df.columns:
            return insights

        # Calculate total waste
        wastage = df.get('wastage_quantity', pd.Series([0])).sum()
        rejected = df.get('rejected_quantity', pd.Series([0])).sum()
        total_waste = wastage + rejected
        total_actual = df['actual_quantity'].sum() if 'actual_quantity' in df.columns else 1
        waste_rate = total_waste / total_actual * 100

        # Cost impact
        if 'material_cost' in df.columns:
            wastage_cost = df['material_cost'].sum() * (waste_rate / 100)
        else:
            wastage_cost = total_waste * 10  # Assume $10 avg cost per unit

        if waste_rate > 5:
            insights.append(self._create_insight(
                severity=Severity.HIGH if waste_rate > 10 else Severity.MEDIUM,
                finding=f"Wastage rate at {waste_rate:.1f}% ({total_waste:,} units). Cost impact: ~${wastage_cost:,.0f}",
                impact=f"Annual wastage cost projection: ${wastage_cost * 12:,.0f}. Direct hit to gross margin. Each 1% reduction saves ${wastage_cost / waste_rate * 12:,.0f}/year.",
                action=f"IMMEDIATE: (1) Quality control audit for high-wastage products, (2) Check raw material quality from suppliers, (3) Retrain operators on problem lines, (4) Set weekly wastage targets with accountability. Target: reduce wastage to <3% within 90 days."
            ))

        # High wastage products
        if 'product_name' in df.columns:
            df['total_waste'] = df.get('wastage_quantity', 0) + df.get('rejected_quantity', 0)
            by_product = df.groupby('product_name')['total_waste'].sum().sort_values(ascending=False)
            high_waste = by_product[by_product > total_waste * 0.2]

            if len(high_waste) > 0:
                top_waste_product = high_waste.index[0]
                top_waste_value = high_waste.iloc[0]

                insights.append(self._create_insight(
                    severity=Severity.MEDIUM,
                    finding=f"Product '{top_waste_product}' generates {top_waste_value/total_waste*100:.0f}% of all waste",
                    impact=f"Focus improvement efforts here for maximum impact. {top_waste_value:,} units wasted.",
                    action=f"Deep-dive on '{top_waste_product}': (1) Analyze waste type (scrap vs rework), (2) Review BOM for accuracy, (3) Check operator training. Expected savings: $50K by reducing waste 50%."
                ))

        return insights

    def _analyze_cost_per_unit(self) -> List[Insight]:
        """Analyze cost per unit trends."""
        insights = []
        df = self.data.copy()

        if 'total_cost' not in df.columns or 'quantity_produced' not in df.columns:
            return insights

        df['cost_per_unit'] = df['total_cost'] / df['quantity_produced']

        # Trend analysis if we have dates
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')

            # Compare recent vs prior period
            midpoint = len(df) // 2
            if midpoint >= 3:
                prior_avg_cpu = df.iloc[:midpoint]['cost_per_unit'].mean()
                recent_avg_cpu = df.iloc[midpoint:]['cost_per_unit'].mean()
                cpu_change = ((recent_avg_cpu - prior_avg_cpu) / prior_avg_cpu * 100) if prior_avg_cpu > 0 else 0

                if cpu_change > 10:
                    # Breakdown by cost component
                    breakdown_str = ""
                    if 'material_cost' in df.columns and 'labor_cost' in df.columns:
                        prior_material = df.iloc[:midpoint].apply(
                            lambda r: r.get('material_cost', 0) / r['quantity_produced'] if r['quantity_produced'] > 0 else 0, axis=1).mean()
                        recent_material = df.iloc[midpoint:].apply(
                            lambda r: r.get('material_cost', 0) / r['quantity_produced'] if r['quantity_produced'] > 0 else 0, axis=1).mean()
                        material_change = ((recent_material - prior_material) / prior_material * 100) if prior_material > 0 else 0

                        prior_labor = df.iloc[:midpoint].apply(
                            lambda r: r.get('labor_cost', 0) / r['quantity_produced'] if r['quantity_produced'] > 0 else 0, axis=1).mean()
                        recent_labor = df.iloc[midpoint:].apply(
                            lambda r: r.get('labor_cost', 0) / r['quantity_produced'] if r['quantity_produced'] > 0 else 0, axis=1).mean()
                        labor_change = ((recent_labor - prior_labor) / prior_labor * 100) if prior_labor > 0 else 0

                        breakdown_str = f" Material: {material_change:+.1f}%, Labor: {labor_change:+.1f}%"

                    insights.append(self._create_insight(
                        severity=Severity.HIGH,
                        finding=f"Cost per unit increased {cpu_change:.1f}% (from ${prior_avg_cpu:.2f} to ${recent_avg_cpu:.2f}).{breakdown_str}",
                        impact=f"Margin erosion. At current volume, extra cost = ${(recent_avg_cpu - prior_avg_cpu) * df['quantity_produced'].sum():,.0f} annually",
                        action=f"COST BREAKDOWN AUDIT within 2 weeks: Focus on biggest driver. If MATERIAL: renegotiate suppliers or find alternatives. If LABOR: review efficiency, reduce overtime, cross-train. If OVERHEAD: audit fixed cost allocation."
                    ))

        return insights

    def _analyze_yield(self) -> List[Insight]:
        """Analyze yield rates."""
        insights = []
        df = self.data.copy()

        if 'good_quantity' not in df.columns or 'actual_quantity' not in df.columns:
            return insights

        df['yield_pct'] = df['good_quantity'] / df['actual_quantity'] * 100
        avg_yield = df['yield_pct'].mean()

        if avg_yield < 90:
            lost_units = df['actual_quantity'].sum() - df['good_quantity'].sum()

            insights.append(self._create_insight(
                severity=Severity.MEDIUM,
                finding=f"Average yield rate at {avg_yield:.1f}% - {lost_units:,} units lost to non-conformance",
                impact=f"Lost units represent ${lost_units * 50:,.0f} in potential revenue (at $50 avg price). Yield improvement has highest ROI of any manufacturing improvement.",
                action=f"YIELD IMPROVEMENT PROGRAM: (1) Implement first-pass yield tracking by product, (2) Root cause analysis on bottom 5 products, (3) Standardize work instructions. Target: 95% yield within 6 months."
            ))

        return insights

    def _analyze_production_trends(self) -> List[Insight]:
        """Analyze production volume trends."""
        insights = []
        df = self.data.copy()

        trend = self.trend_analysis('actual_quantity')
        if 'error' not in trend:
            if trend['trend'] == 'falling' and trend['mom_change_pct'] < -15:
                insights.append(self._create_insight(
                    severity=Severity.HIGH,
                    finding=f"Production output dropped {abs(trend['mom_change_pct']):.1f}% MoM",
                    impact=f"Capacity underutilization affects fixed cost absorption. At this rate, quarterly output will be {abs(trend['mom_change_pct']) * 3:.0f}% below target.",
                    action=f"PRODUCTION RECOVERY PLAN: (1) Identify bottleneck causing drop, (2) Schedule overtime to catch up, (3) Review workforce availability. Target: restore to baseline within 4 weeks."
                ))

            if trend['trend'] == 'rising' and trend['mom_change_pct'] > 20:
                insights.append(self._create_insight(
                    severity=Severity.LOW,
                    finding=f"Production ramping up +{trend['mom_change_pct']:.1f}% MoM",
                    impact=f"Strong demand signal. Ensure operations can sustain this level.",
                    action=f"CAPACITY CHECK: (1) Verify raw material availability, (2) Assess workforce capacity, (3) Plan for 25% additional volume. Consider temporary staffing or overtime."
                ))

        return insights

    def _generate_charts_data(self, kpis: Dict) -> Dict[str, Any]:
        """Generate data for charts."""
        df = self.data.copy()

        # Production efficiency by product
        if 'product_name' in df.columns and 'planned_quantity' in df.columns and 'actual_quantity' in df.columns:
            df['efficiency'] = df['actual_quantity'] / df['planned_quantity'] * 100
            efficiency_data = df.groupby('product_name')['efficiency'].mean().sort_values()
            efficiency_chart = [
                {'product': name, 'efficiency': round(float(val), 1)}
                for name, val in efficiency_data.items()
            ]
        else:
            efficiency_chart = []

        # Wastage by product
        if 'product_name' in df.columns:
            wastage_col = 'wastage_quantity' if 'wastage_quantity' in df.columns else 'rejected_quantity'
            if wastage_col in df.columns:
                waste_data = df.groupby('product_name')[wastage_col].sum().sort_values(ascending=False).head(10)
                waste_chart = [
                    {'product': name, 'wastage': int(val)}
                    for name, val in waste_data.items()
                ]
            else:
                waste_chart = []
        else:
            waste_chart = []

        # Cost trend
        if 'date' in df.columns and 'cost_per_unit' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            cost_trend = [
                {'date': row['date'].strftime('%Y-%m-%d'), 'cost_per_unit': round(float(row['cost_per_unit']), 2)}
                for _, row in df.iterrows()
            ]
        else:
            cost_trend = []

        return {
            'efficiency_by_product': efficiency_chart,
            'wastage_by_product': waste_chart,
            'cost_per_unit_trend': cost_trend
        }
