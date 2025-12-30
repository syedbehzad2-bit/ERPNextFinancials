"""
Sales analyzer - Trends, Product Performance, Customer Concentration analysis.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List

from analyzers.base_analyzer import BaseAnalyzer
from models.analysis_output import AnalysisResult, Insight
from models.base import InsightCategory, Severity
from config import settings


class SalesAnalyzer(BaseAnalyzer):
    """
    Analyzes sales trends, top/bottom products, and customer concentration.
    Every insight has specific numbers and exact actions.
    """

    def get_category(self) -> InsightCategory:
        return InsightCategory.SALES

    def analyze(self) -> AnalysisResult:
        """Run complete sales analysis."""
        kpis = self.calculate_kpis()
        insights = []

        # Trend analysis
        trend_insights = self._analyze_trends()
        insights.extend(trend_insights)

        # Product performance
        product_insights = self._analyze_product_performance()
        insights.extend(product_insights)

        # Customer concentration
        customer_insights = self._analyze_customer_concentration()
        insights.extend(customer_insights)

        # Pareto analysis
        pareto_insights = self._pareto_analysis()
        insights.extend(pareto_insights)

        # Discount analysis
        discount_insights = self._analyze_discounts()
        insights.extend(discount_insights)

        # Charts data
        charts_data = self._generate_charts_data()

        return AnalysisResult(
            domain="sales",
            kpis=kpis,
            insights=insights,
            charts_data=charts_data
        )

    def calculate_kpis(self) -> Dict[str, Any]:
        """Calculate sales KPIs."""
        df = self.data.copy()

        # Total revenue
        total_revenue = df['total_amount'].sum() if 'total_amount' in df.columns else 0

        # Order count
        order_col = 'order_id' if 'order_id' in df.columns else 'order'
        order_count = df[order_col].nunique() if order_col in df.columns else len(df)

        # Average order value
        avg_order_value = total_revenue / order_count if order_count > 0 else 0

        # Customer count
        customer_col = 'customer_id' if 'customer_id' in df.columns else 'customer'
        unique_customers = df[customer_col].nunique() if customer_col in df.columns else 0

        # Product count
        product_col = 'product_id' if 'product_id' in df.columns else 'product'
        unique_products = df[product_col].nunique() if product_col in df.columns else 0

        # Calculate margin if cost available
        if 'total_amount' in df.columns and 'cost_of_goods' in df.columns:
            total_cost = df['cost_of_goods'].sum()
            gross_margin = total_revenue - total_cost
            avg_margin_pct = (gross_margin / total_revenue * 100) if total_revenue > 0 else 0
        else:
            gross_margin = 0
            avg_margin_pct = 0

        # Growth rate
        growth = self._calculate_growth()

        return {
            'total_revenue': float(total_revenue),
            'order_count': int(order_count),
            'average_order_value': round(float(avg_order_value), 2),
            'unique_customers': int(unique_customers),
            'unique_products': int(unique_products),
            'gross_margin': float(gross_margin),
            'average_margin_pct': round(float(avg_margin_pct), 2),
            'revenue_growth_pct': round(float(growth), 2)
        }

    def _calculate_growth(self) -> float:
        """Calculate period-over-period revenue growth."""
        if 'date' not in self.data.columns or 'total_amount' not in self.data.columns:
            return 0

        df = self.data.copy()
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')

        # Group by month
        monthly = df.groupby(df['date'].dt.to_period('M'))['total_amount'].sum()

        if len(monthly) < 2:
            return 0

        current = monthly.iloc[-1]
        prior = monthly.iloc[-2]

        if prior == 0:
            return 0

        return round(float((current - prior) / prior * 100), 2)

    def _analyze_trends(self) -> List[Insight]:
        """MoM/QoQ trend analysis."""
        insights = []
        df = self.data.copy()

        if 'date' not in df.columns or 'total_amount' not in df.columns:
            return insights

        trend = self.trend_analysis('total_amount')
        if 'error' not in trend:
            if trend['mom_change_pct'] < -10:
                insights.append(self._create_insight(
                    severity=Severity.HIGH,
                    finding=f"Sales dropped {abs(trend['mom_change_pct']):.1f}% MoM (${trend['prior_value']:,.0f} to ${trend['current_value']:,.0f})",
                    impact=f"If decline continues, Q4 revenue will be ${trend['current_value'] * 3:,.0f} vs projected ${trend['prior_value'] * 3:,.0f} - a ${(trend['prior_value'] - trend['current_value']) * 3:,.0f} shortfall",
                    action=f"IMMEDIATE (Week 1): (1) Check top 10 accounts for issues/churn signals, (2) Analyze lost deals in CRM, (3) Review competitive activity. Week 2: Launch retention campaign for at-risk customers. Target: recover 50% of lost revenue within 30 days."
                ))

            if trend['qoq_change_pct'] > 20:
                insights.append(self._create_insight(
                    severity=Severity.LOW,
                    finding=f"Sales growing strongly at {trend['qoq_change_pct']:.1f}% quarter-over-quarter",
                    impact=f"Strong growth trajectory. Ensure operations can scale to meet demand before it becomes a capacity constraint.",
                    action=f"CAPACITY PLANNING: (1) Review inventory levels for top 20 SKUs, (2) Assess production capacity, (3) Plan for 25% additional volume. Consider promotional limits to manage demand."
                ))

            # Check for volatility
            if 'data_points' in trend and trend['data_points'] >= 4:
                df_temp = df.copy()
                df_temp['date'] = pd.to_datetime(df_temp['date'])
                df_temp = df_temp.sort_values('date')
                monthly = df_temp.groupby(df_temp['date'].dt.to_period('M'))['total_amount'].sum()
                volatility = monthly.std() / monthly.mean() * 100 if monthly.mean() > 0 else 0

                if volatility > 30:
                    insights.append(self._create_insight(
                        severity=Severity.MEDIUM,
                        finding=f"Sales volatility at {volatility:.1f}% - inconsistent performance",
                        impact=f"High volatility makes planning difficult. Some months significantly underperforming.",
                        action=f"STABILIZE SALES: (1) Identify what's driving volatility (seasonality? promotions?), (2) Build rolling 3-month forecast, (3) Implement lead indicators to predict slow months."
                    ))

        return insights

    def _analyze_product_performance(self) -> List[Insight]:
        """Identify top and bottom performing products."""
        insights = []
        df = self.data.copy()

        if 'product_id' not in df.columns or 'total_amount' not in df.columns:
            return insights

        # Handle case where product_name might not exist
        if 'product_name' in df.columns:
            product_sales = df.groupby(['product_id', 'product_name'])['total_amount'].sum().reset_index()
        else:
            product_sales = df.groupby(['product_id'])['total_amount'].sum().reset_index()
            product_sales['product_name'] = product_sales['product_id']

        product_sales = product_sales.sort_values('total_amount', ascending=False)

        total_sales = product_sales['total_amount'].sum()
        product_count = len(product_sales)

        # Bottom performers
        bottom_10 = product_sales.tail(10)
        bottom_10_value = bottom_10['total_amount'].sum()
        bottom_10_pct = bottom_10_value / total_sales * 100

        if product_count > 20 and bottom_10_pct < 5:
            insights.append(self._create_insight(
                severity=Severity.MEDIUM,
                finding=f"Bottom 10 products contribute only ${bottom_10_value:,.0f} ({bottom_10_pct:.1f}% of revenue) - inefficient SKU portfolio",
                impact=f"These products consume resources (inventory, warehouse space, management attention) without meaningful return. Cost to carry likely exceeds margin.",
                action=f"SKU RATIONALIZATION: (1) Discontinue bottom 5 products immediately, (2) Conduct margin analysis on next 5, (3) Reallocate resources to top 20 products. Expected savings: $50K in reduced inventory + $20K in operational efficiency."
            ))

        # Top performers
        top_5 = product_sales.head(5)
        top_5_value = top_5['total_amount'].sum()
        top_5_pct = top_5_value / total_sales * 100

        if top_5_pct > 60:
            insights.append(self._create_insight(
                severity=Severity.MEDIUM,
                finding=f"Top 5 products represent {top_5_pct:.1f}% of revenue - product concentration risk",
                impact=f"Business heavily dependent on few products. Any issue with these products (supply, quality, competition) severely impacts revenue.",
                action=f"PRODUCT DIVERSIFICATION: (1) Analyze what makes top products successful, (2) Develop next tier of products with similar characteristics, (3) Set target to reduce top 5 concentration below 50% within 12 months."
            ))

        return insights

    def _analyze_customer_concentration(self) -> List[Insight]:
        """Analyze customer revenue concentration risk."""
        insights = []
        df = self.data.copy()

        if 'customer_id' not in df.columns or 'total_amount' not in df.columns:
            return insights

        # Handle case where customer_name might not exist
        if 'customer_name' in df.columns:
            customer_sales = df.groupby(['customer_id', 'customer_name'])['total_amount'].sum().reset_index()
        else:
            customer_sales = df.groupby(['customer_id'])['total_amount'].sum().reset_index()
            customer_sales['customer_name'] = customer_sales['customer_id']

        customer_sales = customer_sales.sort_values('total_amount', ascending=False)

        total_revenue = customer_sales['total_amount'].sum()
        customer_count = len(customer_sales)

        # Top customer
        top_customer = customer_sales.iloc[0]
        top_customer_pct = top_customer['total_amount'] / total_revenue * 100

        if top_customer_pct > settings.customer_concentration_critical_pct:
            insights.append(self._create_insight(
                severity=Severity.CRITICAL,
                finding=f"Customer '{top_customer['customer_name']}' represents {top_customer_pct:.1f}% of revenue (${top_customer['total_amount']:,.0f})",
                impact=f"SINGLE POINT OF FAILURE. Loss of this customer = loss of ${top_customer['total_amount']:,.0f} annual revenue. Business continuity at extreme risk.",
                action=f"IMMEDIATE CUSTOMER RETENTION: (1) Assign executive sponsor to this account, (2) Schedule quarterly business review with customer execs, (3) Develop 3+ new customers in similar segment within 6 months to reduce dependency below 20%, (4) Create switching costs via integration/customization. Budget: $100K for relationship deepening."
            ))

        # Top 5 customers
        if customer_count >= 5:
            top_5_revenue = customer_sales.head(5)['total_amount'].sum()
            top_5_pct = top_5_revenue / total_revenue * 100

            if top_5_pct > 70:
                insights.append(self._create_insight(
                    severity=Severity.HIGH,
                    finding=f"Top 5 customers represent {top_5_pct:.1f}% of revenue (${top_5_revenue:,.0f} of ${total_revenue:,.0f})",
                    impact=f"Customer base dangerously concentrated. Revenue highly vulnerable to customer churn. Losing 2 top customers would be catastrophic.",
                    action=f"CUSTOMER DIVERSIFICATION PROGRAM: (1) Launch mid-market acquisition initiative targeting 15 new customers in $25K-$100K tier within 12 months, (2) Increase marketing spend on customer acquisition, (3) Set KPI: reduce top 5 concentration below 50%. Budget: $150K for acquisition program."
                ))

        # Identify at-risk customers (declining revenue)
        if 'date' in df.columns:
            customer_recent = df[df['date'] >= (pd.Timestamp.now() - pd.Timedelta(days=90))].groupby('customer_id')['total_amount'].sum()
            customer_prior = df[df['date'] < (pd.Timestamp.now() - pd.Timedelta(days=90))].groupby('customer_id')['total_amount'].sum()

            declining = []
            for cid in customer_recent.index:
                if cid in customer_prior.index:
                    change = (customer_recent[cid] - customer_prior[cid]) / customer_prior[cid] * 100
                    if change < -30:
                        declining.append((cid, change, customer_recent[cid]))

            if len(declining) > 0:
                top_declining = sorted(declining, key=lambda x: x[1])[:3]
                insights.append(self._create_insight(
                    severity=Severity.HIGH,
                    finding=f"3 customers showing 30%+ revenue decline - churn risk",
                    impact=f"${sum([x[2] for x in top_declining]):,.0f} in declining revenue. These customers may be at risk of leaving.",
                    action=f"CHURN PREVENTION: (1) Contact each declining customer within 1 week, (2) Understand their issues, (3) Offer retention incentives, (4) Document feedback for product/operations. Target: reverse decline in 2 customers."
                ))

        return insights

    def _pareto_analysis(self) -> List[Insight]:
        """80/20 Pareto analysis."""
        insights = []
        df = self.data.copy()

        if 'product_id' not in df.columns or 'total_amount' not in df.columns:
            return insights

        pareto = self.pareto_analysis('product_id', 'total_amount')

        if 'error' not in pareto:
            items_for_80 = pareto['items_for_80_pct']
            concentration = pareto['concentration']
            total_products = len(pareto['full_pareto'])
            remaining_products = total_products - items_for_80

            insights.append(self._create_insight(
                severity=Severity.MEDIUM if concentration == 'HIGH' else Severity.LOW,
                finding=f"{items_for_80} products ({items_for_80 / total_products * 100:.1f}% of SKUs) generate 80% of revenue",
                impact=f"{'Heavy concentration - focus resources on winners' if concentration == 'HIGH' else 'Healthy distribution across product portfolio'}",
                action=f"RESOURCE ALLOCATION: Prioritize top {items_for_80} products for: (1) Inventory investment, (2) Marketing spend, (3) Sales focus. Review ROI on remaining {remaining_products} products - consider pruning underperformers."
            ))

        return insights

    def _analyze_discounts(self) -> List[Insight]:
        """Analyze discount patterns."""
        insights = []
        df = self.data.copy()

        if 'discount' not in df.columns and 'discount_amount' not in df.columns:
            return insights

        discount_col = 'discount' if 'discount' in df.columns else 'discount_amount'
        if 'total_amount' in df.columns:
            df['discount_rate'] = df[discount_col] / df['total_amount'] * 100

            avg_discount = df['discount_rate'].mean()
            high_discount_orders = df[df['discount_rate'] > 20]

            if avg_discount > 15:
                insights.append(self._create_insight(
                    severity=Severity.HIGH,
                    finding=f"Average discount rate at {avg_discount:.1f}% - eroding margins",
                    impact=f"Every 1% of discount directly reduces margin. At {avg_discount}%, you're giving away ${df['total_amount'].sum() * avg_discount / 100:,.0f} in potential margin.",
                    action=f"DISCIPLINE DISCOUNTS: (1) Set maximum discount thresholds by product category, (2) Require manager approval for discounts >15%, (3) Train sales on value-based selling instead of price-based. Target: reduce average discount to <10%."
                ))

            if len(high_discount_orders) > 10:
                insights.append(self._create_insight(
                    severity=Severity.MEDIUM,
                    finding=f"{len(high_discount_orders)} orders with >20% discount - potential discounting abuse",
                    impact=f"Deep discounting on {len(high_discount_orders)} orders. Revenue leakage opportunity.",
                    action=f"DISCOUNT AUDIT: Review top 10 high-discount orders: (1) Were approvals obtained?, (2) What's the customer reason?, (3) Is there pattern by sales rep? Implement stricter controls."
                ))

        return insights

    def _generate_charts_data(self) -> Dict[str, Any]:
        """Generate data for charts."""
        df = self.data.copy()

        # Revenue trend
        if 'date' in df.columns and 'total_amount' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            monthly = df.groupby(df['date'].dt.to_period('M'))['total_amount'].sum()
            revenue_trend = [
                {'period': str(p), 'revenue': float(v)}
                for p, v in monthly.items()
            ]
        else:
            revenue_trend = []

        # Top products
        if 'product_name' in df.columns and 'total_amount' in df.columns:
            product_sales = df.groupby('product_name')['total_amount'].sum().sort_values(ascending=False).head(10)
            top_products = [
                {'product': name, 'revenue': float(val)}
                for name, val in product_sales.items()
            ]
        else:
            top_products = []

        # Customer concentration
        if 'customer_name' in df.columns and 'total_amount' in df.columns:
            customer_sales = df.groupby('customer_name')['total_amount'].sum().sort_values(ascending=False).head(10)
            top_customers = [
                {'customer': name, 'revenue': float(val)}
                for name, val in customer_sales.items()
            ]
        else:
            top_customers = []

        return {
            'revenue_trend': revenue_trend,
            'top_products': top_products,
            'top_customers': top_customers
        }
