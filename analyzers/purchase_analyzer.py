"""
Purchase analyzer - Supplier Performance, Lead Time, Price analysis.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List

from analyzers.base_analyzer import BaseAnalyzer
from models.analysis_output import AnalysisResult, Insight
from models.base import InsightCategory, Severity


class PurchaseAnalyzer(BaseAnalyzer):
    """
    Analyzes purchase patterns and supplier performance.
    Every insight has specific numbers and exact actions.
    """

    def get_category(self) -> InsightCategory:
        return InsightCategory.PURCHASE

    def analyze(self) -> AnalysisResult:
        """Run complete purchase analysis."""
        kpis = self.calculate_kpis()
        insights = []

        # Supplier performance
        supplier_insights = self._analyze_supplier_performance()
        insights.extend(supplier_insights)

        # Supplier concentration
        concentration_insights = self._analyze_supplier_concentration()
        insights.extend(concentration_insights)

        # Lead time analysis
        lead_time_insights = self._analyze_lead_times()
        insights.extend(lead_time_insights)

        # Price trends
        price_insights = self._analyze_price_trends()
        insights.extend(price_insights)

        # Delivery performance
        delivery_insights = self._analyze_delivery_performance()
        insights.extend(delivery_insights)

        # Charts data
        charts_data = self._generate_charts_data()

        return AnalysisResult(
            domain="purchase",
            kpis=kpis,
            insights=insights,
            charts_data=charts_data
        )

    def calculate_kpis(self) -> Dict[str, Any]:
        """Calculate purchase KPIs."""
        df = self.data.copy()

        # Total spend
        total_spend = df['total_amount'].sum() if 'total_amount' in df.columns else 0

        # Order count
        order_count = len(df)

        # Supplier count
        supplier_col = 'supplier_id' if 'supplier_id' in df.columns else 'supplier'
        supplier_count = df[supplier_col].nunique() if supplier_col in df.columns else 0

        # Average order value
        avg_order_value = total_spend / order_count if order_count > 0 else 0

        # Average lead time
        if 'lead_time_days' in df.columns:
            avg_lead_time = df['lead_time_days'].mean()
        elif 'expected_delivery_date' in df.columns and 'order_date' in df.columns:
            df['lead_time_days'] = (pd.to_datetime(df['expected_delivery_date']) - pd.to_datetime(df['order_date'])).dt.days
            avg_lead_time = df['lead_time_days'].mean()
        else:
            avg_lead_time = 0

        # On-time delivery rate
        if 'is_on_time' in df.columns:
            on_time_rate = df['is_on_time'].mean() * 100
        else:
            on_time_rate = 0

        return {
            'total_spend': float(total_spend),
            'order_count': int(order_count),
            'supplier_count': int(supplier_count),
            'average_order_value': round(float(avg_order_value), 2),
            'average_lead_time_days': round(float(avg_lead_time), 1),
            'on_time_delivery_rate': round(float(on_time_rate), 2) if on_time_rate > 0 else None
        }

    def _analyze_supplier_performance(self) -> List[Insight]:
        """Score suppliers on delivery, quality, price."""
        insights = []
        df = self.data.copy()

        supplier_col = 'supplier_name' if 'supplier_name' in df.columns else 'supplier'

        if supplier_col not in df.columns:
            return insights

        # Aggregate by supplier
        supplier_metrics = df.groupby(supplier_col).agg({
            'total_amount': 'sum',
            'is_on_time': 'mean' if 'is_on_time' in df.columns else None,
            'quality_rejection_rate': 'mean' if 'quality_rejection_rate' in df.columns else None,
            'lead_time_days': 'mean' if 'lead_time_days' in df.columns else None
        })

        # Flag poor performers
        if 'is_on_time' in supplier_metrics.columns:
            poor_delivery = supplier_metrics[supplier_metrics['is_on_time'] < 0.8]
            for supplier, row in poor_delivery.iterrows():
                insights.append(self._create_insight(
                    severity=Severity.HIGH,
                    finding=f"Supplier '{supplier}' has only {row['is_on_time']*100:.0f}% on-time delivery rate",
                    impact=f"Supply chain reliability at risk. Late deliveries cause production delays, stockouts, and missed customer commitments.",
                    action=f"SUPPLIER PERFORMANCE MANAGEMENT: (1) Schedule meeting with supplier to address issues, (2) Request corrective action plan, (3) Qualify backup supplier within 30 days, (4) Consider reducing order volume by 50% until performance improves."
                ))

        # Quality issues
        if 'quality_rejection_rate' in supplier_metrics.columns:
            quality_issues = supplier_metrics[supplier_metrics['quality_rejection_rate'] > 0.05]
            for supplier, row in quality_issues.iterrows():
                insights.append(self._create_insight(
                    severity=Severity.MEDIUM,
                    finding=f"Supplier '{supplier}' quality rejection rate at {row['quality_rejection_rate']*100:.1f}%",
                    impact=f"High rejection rate increases costs and causes delays. Each 1% rejection adds ${row['total_amount'] * 0.01:,.0f} in waste.",
                    action=f"QUALITY REVIEW with '{supplier}': (1) Request root cause analysis, (2) Implement incoming inspection for their products, (3) Set quality improvement target of <2% within 60 days."
                ))

        return insights

    def _analyze_supplier_concentration(self) -> List[Insight]:
        """Identify supplier dependency risks."""
        insights = []
        df = self.data.copy()

        supplier_col = 'supplier_name' if 'supplier_name' in df.columns else 'supplier'

        if supplier_col not in df.columns or 'total_amount' not in df.columns:
            return insights

        supplier_spend = df.groupby(supplier_col)['total_amount'].sum().sort_values(ascending=False)
        total_spend = supplier_spend.sum()

        if total_spend == 0:
            return insights

        # Top supplier
        top_supplier = supplier_spend.index[0]
        top_supplier_pct = supplier_spend.iloc[0] / total_spend * 100

        if top_supplier_pct > 30:
            insights.append(self._create_insight(
                severity=Severity.CRITICAL,
                finding=f"Single supplier dependency: '{top_supplier}' represents {top_supplier_pct:.1f}% of spend (${supplier_spend.iloc[0]:,.0f})",
                impact=f"SUPPLY CHAIN SINGLE POINT OF FAILURE. If this supplier has issues, your entire operation stops. No leverage for price negotiations.",
                action=f"SUPPLIER DIVERSIFICATION IMMEDIATELY: (1) Qualify 2-3 alternative suppliers within 60 days, (2) Shift at least 30% volume to new suppliers within 90 days, (3) Negotiate volume flexibility with current supplier. Budget: $30K for supplier qualification."
            ))

        # Top 3 suppliers
        top_3_pct = supplier_spend.head(3).sum() / total_spend * 100
        if top_3_pct > 70:
            insights.append(self._create_insight(
                severity=Severity.HIGH,
                finding=f"Top 3 suppliers represent {top_3_pct:.1f}% of spend - supplier concentration risk",
                impact=f"Over-reliance on few suppliers. Any disruption (natural disaster, quality issue, price increase) severely impacts operations.",
                action=f"STRATEGIC SOURCING: (1) Develop supplier diversification roadmap, (2) Identify categories for new supplier onboarding, (3) Set target: top 3 < 50% within 18 months. Build relationships with secondary suppliers now."
            ))

        return insights

    def _analyze_lead_times(self) -> List[Insight]:
        """Analyze lead time trends and variability."""
        insights = []
        df = self.data.copy()

        if 'lead_time_days' not in df.columns:
            return insights

        avg_lead_time = df['lead_time_days'].mean()
        lead_time_std = df['lead_time_days'].std()
        long_lead_orders = df[df['lead_time_days'] > avg_lead_time * 1.5]

        if lead_time_std > avg_lead_time * 0.5:
            insights.append(self._create_insight(
                severity=Severity.MEDIUM,
                finding=f"Lead time variability at {lead_time_std:.1f} days (avg: {avg_lead_time:.1f}) - unpredictable supply",
                impact=f"High variability makes planning difficult. Some orders taking 50% longer than average, causing stockouts or excess inventory.",
                action=f"STABILIZE LEAD TIMES: (1) Analyze which suppliers have highest variability, (2) Work with them on more consistent scheduling, (3) Build safety stock for high-variability items, (4) Consider expedited shipping for critical items."
            ))

        if len(long_lead_orders) > len(df) * 0.2:
            insights.append(self._create_insight(
                severity=Severity.MEDIUM,
                finding=f"{len(long_lead_orders)} orders ({len(long_lead_orders)/len(df)*100:.0f}%) have lead times >50% above average",
                impact=f"Significant delays affecting {len(long_lead_orders)} orders. Impact on production schedules and customer deliveries.",
                action=f"LEAD TIME ROOT CAUSE: (1) Map order-to-delivery process, (2) Identify delay points, (3) Work with suppliers on improvement. Target: reduce long-lead orders by 50% within 90 days."
            ))

        return insights

    def _analyze_price_trends(self) -> List[Insight]:
        """Track material/component price movements."""
        insights = []
        df = self.data.copy()

        if 'unit_price' not in df.columns or 'date' not in df.columns:
            return insights

        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')

        # Group by month
        monthly_prices = df.groupby(df['date'].dt.to_period('M'))['unit_price'].mean()

        if len(monthly_prices) >= 3:
            recent_price = monthly_prices.iloc[-1]
            prior_price = monthly_prices.iloc[-3]
            price_change = ((recent_price - prior_price) / prior_price * 100) if prior_price > 0 else 0

            if price_change > 10:
                insights.append(self._create_insight(
                    severity=Severity.HIGH,
                    finding=f"Purchase prices increased {price_change:.1f}% over 3 months (${prior_price:.2f} to ${recent_price:.2f})",
                    impact=f"Direct hit to margins. At current volumes, additional cost = ${(recent_price - prior_price) * df['quantity'].sum():,.0f} annually",
                    action=f"PRICE MANAGEMENT: (1) Negotiate with current suppliers for price freeze/reduction, (2) Source alternative suppliers, (3) Evaluate if price increase can be passed to customers, (4) Review product specifications for cost reduction opportunities."
                ))

            if price_change < -10:
                insights.append(self._create_insight(
                    severity=Severity.LOW,
                    finding=f"Prices decreased {abs(price_change):.1f}% - good cost management opportunity",
                    impact=f"Margin improvement opportunity. Consider if prices can stay low or if you renegotiated well.",
                    action=f"CAPTURE SAVINGS: (1) Lock in lower prices with suppliers, (2) Review contracts for price protection clauses, (3) Consider passing savings to customers strategically to gain volume."
                ))

        return insights

    def _analyze_delivery_performance(self) -> List[Insight]:
        """Analyze overall delivery performance."""
        insights = []
        df = self.data.copy()

        if 'is_on_time' not in df.columns:
            return insights

        on_time_rate = df['is_on_time'].mean() * 100

        if on_time_rate < 85:
            insights.append(self._create_insight(
                severity=Severity.HIGH,
                finding=f"On-time delivery rate at {on_time_rate:.1f}% - below 85% threshold",
                impact=f"Supply chain reliability issue. 15%+ of orders arriving late affects production schedules and customer commitments.",
                action=f"DELIVERY IMPROVEMENT PROGRAM: (1) Review supplier scorecards, (2) Identify worst-performing suppliers, (3) Implement supplier scorecards with consequences, (4) Build buffer inventory for critical items. Target: 95% on-time within 6 months."
            ))

        # Late deliveries impact
        late_deliveries = df[df['is_on_time'] == False]
        if len(late_deliveries) > 0:
            if 'days_late' in late_deliveries.columns:
                avg_days_late = late_deliveries['days_late'].mean()
                insights.append(self._create_insight(
                    severity=Severity.MEDIUM,
                    finding=f"Avg delay of {avg_days_late:.1f} days when deliveries are late",
                    impact=f"Production and customer orders delayed by {avg_days_late:.1f} days on average. Cumulative impact significant.",
                    action=f"REDUCE DELAY IMPACT: (1) Negotiate penalty clauses for late deliveries, (2) Build safety stock for items with history of delays, (3) Consider expedited shipping for critical items."
                ))

        return insights

    def _generate_charts_data(self) -> Dict[str, Any]:
        """Generate data for charts."""
        df = self.data.copy()

        # Spend by supplier
        supplier_col = 'supplier_name' if 'supplier_name' in df.columns else 'supplier'
        if supplier_col in df.columns and 'total_amount' in df.columns:
            supplier_spend = df.groupby(supplier_col)['total_amount'].sum().sort_values(ascending=False).head(10)
            spend_by_supplier = [
                {'supplier': name, 'spend': float(val)}
                for name, val in supplier_spend.items()
            ]
        else:
            spend_by_supplier = []

        # Lead time trend
        if 'date' in df.columns and 'lead_time_days' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            monthly_lead = df.groupby(df['date'].dt.to_period('M'))['lead_time_days'].mean()
            lead_time_trend = [
                {'period': str(p), 'lead_time': round(float(v), 1)}
                for p, v in monthly_lead.items()
            ]
        else:
            lead_time_trend = []

        # Delivery performance
        if 'is_on_time' in df.columns:
            on_time = df['is_on_time'].sum()
            late = len(df) - on_time
            delivery_data = [
                {'status': 'On Time', 'count': int(on_time)},
                {'status': 'Late', 'count': int(late)}
            ]
        else:
            delivery_data = []

        return {
            'spend_by_supplier': spend_by_supplier,
            'lead_time_trend': lead_time_trend,
            'delivery_performance': delivery_data
        }
