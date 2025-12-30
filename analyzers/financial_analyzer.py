"""
Financial analyzer - P&L, Revenue, Margin, and Expense analysis.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List

from analyzers.base_analyzer import BaseAnalyzer
from models.analysis_output import AnalysisResult, Insight
from models.base import InsightCategory, Severity


class FinancialAnalyzer(BaseAnalyzer):
    """
    Analyzes P&L, Revenue, Expenses, and Margins.
    Every insight has specific numbers and exact actions.
    """

    def get_category(self) -> InsightCategory:
        return InsightCategory.FINANCIAL

    def analyze(self) -> AnalysisResult:
        """Run complete financial analysis."""
        kpis = self.calculate_kpis()
        insights = []

        # Margin analysis
        margin_insights = self._analyze_margins()
        insights.extend(margin_insights)

        # Revenue analysis
        revenue_insights = self._analyze_revenue()
        insights.extend(revenue_insights)

        # Expense analysis
        expense_insights = self._analyze_expenses()
        insights.extend(expense_insights)

        # Customer concentration
        concentration_insights = self._analyze_customer_concentration()
        insights.extend(concentration_insights)

        # Budget variance
        if 'budget' in self.data.columns:
            variance_insights = self._analyze_budget_variance()
            insights.extend(variance_insights)

        # Calculate charts data
        charts_data = self._generate_charts_data(kpis)

        return AnalysisResult(
            domain="financial",
            kpis=kpis,
            insights=insights,
            charts_data=charts_data
        )

    def calculate_kpis(self) -> Dict[str, Any]:
        """Calculate financial KPIs."""
        df = self.data.copy()

        # Total revenue
        total_revenue = df['revenue'].sum() if 'revenue' in df.columns else 0

        # Calculate gross profit
        if 'cost_of_goods_sold' in df.columns:
            cogs = df['cost_of_goods_sold'].sum()
            gross_profit = total_revenue - cogs
            gross_margin_pct = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0
        else:
            cogs = 0
            gross_profit = 0
            gross_margin_pct = 0

        # Calculate net income
        operating_expenses = df['operating_expenses'].sum() if 'operating_expenses' in df.columns else 0
        operating_income = gross_profit - operating_expenses
        net_income = df['net_income'].sum() if 'net_income' in df.columns else operating_income

        net_margin_pct = (net_income / total_revenue * 100) if total_revenue > 0 else 0
        operating_margin_pct = (operating_income / total_revenue * 100) if total_revenue > 0 else 0

        # Expense ratio
        expense_ratio = (operating_expenses / total_revenue * 100) if total_revenue > 0 else 0

        return {
            'total_revenue': float(total_revenue),
            'gross_profit': float(gross_profit),
            'gross_margin_pct': round(float(gross_margin_pct), 2),
            'operating_income': float(operating_income),
            'operating_margin_pct': round(float(operating_margin_pct), 2),
            'net_income': float(net_income),
            'net_margin_pct': round(float(net_margin_pct), 2),
            'total_expenses': float(operating_expenses),
            'expense_ratio': round(float(expense_ratio), 2),
            'revenue_growth': self._calculate_growth('revenue')
        }

    def _calculate_growth(self, col: str) -> float:
        """Calculate period-over-period growth."""
        if col not in self.data.columns or 'period' not in self.data.columns:
            return 0

        df = self.data.copy()
        df['period'] = pd.to_datetime(df['period'])
        df = df.sort_values('period')

        if len(df) < 2:
            return 0

        current = df[col].iloc[-1]
        prior = df[col].iloc[-2]

        if prior == 0:
            return 0

        return round(float((current - prior) / prior * 100), 2)

    def _analyze_margins(self) -> List[Insight]:
        """Analyze margin trends and issues."""
        insights = []
        df = self.data.copy()

        if 'period' not in df.columns:
            return insights

        df['period'] = pd.to_datetime(df['period'])
        df = df.sort_values('period')

        # Calculate margins per period
        if 'revenue' in df.columns and 'cost_of_goods_sold' in df.columns:
            df['gross_margin_pct'] = (df['revenue'] - df['cost_of_goods_sold']) / df['revenue'] * 100

        if len(df) >= 3:
            recent_margin = df['gross_margin_pct'].iloc[-1] if 'gross_margin_pct' in df.columns else 0
            prior_margin = df['gross_margin_pct'].iloc[-3]
            margin_change = recent_margin - prior_margin

            # Critical margin decline
            if margin_change < -5:
                insights.append(self._create_insight(
                    severity=Severity.CRITICAL,
                    finding=f"Gross margin dropped from {prior_margin:.1f}% to {recent_margin:.1f}% ({margin_change:.1f}% decline over 3 periods)",
                    impact=f"At this rate, you will lose ${abs(margin_change) * 2:.1f}% more margin in next 6 months, directly threatening profitability",
                    action=f"IMMEDIATE: (1) Renegotiate top 5 supplier contracts within 30 days targeting 10% cost reduction, (2) Review pricing on bottom 20% margin products, (3) Audit material waste in production",
                    metrics={'current_margin': recent_margin, 'prior_margin': prior_margin, 'change': margin_change}
                ))

            # Margin below threshold
            if recent_margin < 20:
                insights.append(self._create_insight(
                    severity=Severity.HIGH,
                    finding=f"Gross margin is critically low at {recent_margin:.1f}% (industry benchmark: 30-40%)",
                    impact=f"Every $1 of revenue generates only ${recent_margin/100:.2f} gross profit - insufficient to cover operating costs",
                    action=f"Conduct 3-week margin improvement project: (1) Identify products with margin <15%, (2) Increase prices by 8-12% on those products, (3) Switch to lower-cost suppliers for top 10 SKUs by volume"
                ))

        # Net margin analysis
        if 'net_income' in df.columns and 'revenue' in df.columns:
            df['net_margin_pct'] = df['net_income'] / df['revenue'] * 100

            if len(df) >= 2:
                current_net = df['net_margin_pct'].iloc[-1]
                if current_net < 5:
                    insights.append(self._create_insight(
                        severity=Severity.HIGH,
                        finding=f"Net margin at {current_net:.1f}% - barely covering cost of capital",
                        impact=f"Business is operating with razor-thin profitability. Any increase in costs or drop in sales will result in losses.",
                        action=f"Reduce fixed costs by 10% within 60 days through: (1) Renegotiate rent/leases, (2) Consolidate vendors, (3) Automate manual processes"
                    ))

        return insights

    def _analyze_revenue(self) -> List[Insight]:
        """Analyze revenue trends and concentration."""
        insights = []
        df = self.data.copy()

        trend = self.trend_analysis('revenue')
        if 'error' not in trend:
            if trend['mom_change_pct'] < -10:
                insights.append(self._create_insight(
                    severity=Severity.HIGH,
                    finding=f"Revenue dropped {abs(trend['mom_change_pct']):.1f}% MoM (from ${trend['prior_value']:,.0f} to ${trend['current_value']:,.0f})",
                    impact=f"If decline continues, quarterly revenue will be ${trend['current_value'] * 3:,.0f} - ${(trend['prior_value'] - trend['current_value']) * 3:,.0f} below target",
                    action=f"Week 1: (1) Contact top 20 customers to identify issues, (2) Analyze lost deals, (3) Review competitive landscape. Week 2: Launch retention campaign for at-risk accounts."
                ))

            if trend['trend'] == 'rising' and trend['mom_change_pct'] > 15:
                insights.append(self._create_insight(
                    severity=Severity.LOW,
                    finding=f"Revenue growing strongly at {trend['mom_change_pct']:.1f}% MoM",
                    impact=f"Strong momentum - opportunity to capitalize before competitors react",
                    action=f"Double down on winning channels: (1) Increase marketing spend by 20%, (2) Stock up on top-selling SKUs, (3) Expedite hiring for sales team"
                ))

        return insights

    def _analyze_expenses(self) -> List[Insight]:
        """Analyze expense breakdown and overruns."""
        insights = []
        df = self.data.copy()

        # Check for expense categories
        if 'category' in df.columns and 'amount' in df.columns:
            by_category = df.groupby('category')['amount'].sum()

            # Find highest expense categories
            if len(by_category) > 0:
                top_expense = by_category.idxmax()
                top_expense_value = by_category.max()

                # Get total for percentage
                total = by_category.sum()
                top_pct = top_expense_value / total * 100

                if top_pct > 40:
                    insights.append(self._create_insight(
                        severity=Severity.HIGH,
                        finding=f"{top_expense} represents {top_pct:.0f}% of total expenses (${top_expense_value:,.0f})",
                        impact=f"Heavy concentration in {top_expense} creates cost vulnerability - any price increase here directly hurts margins",
                        action=f"Diversify {top_expense} spend: (1) Qualify 2-3 alternative suppliers, (2) Negotiate volume discounts with current supplier, (3) Reduce consumption by 10% through efficiency gains"
                    ))

        # Budget variance for expenses
        if 'actual' in df.columns and 'budget' in df.columns:
            variance = self.variance_analysis('actual', 'budget')
            if 'error' not in variance and variance['is_over_budget']:
                severity = Severity.CRITICAL if variance['total_variance_pct'] > 20 else Severity.HIGH
                insights.append(self._create_insight(
                    severity=severity,
                    finding=f"Expenses are {variance['total_variance_pct']:.1f}% over budget (${variance['total_variance']:,.0f} overspend)",
                    impact=f"At this rate, annual overspend will be ${variance['total_variance'] * 12:,.0f} - equivalent to {variance['total_variance'] * 12 / variance['total_planned'] * 100:.0f}% of annual budget",
                    action=f"IMMEDIATE: Freeze all discretionary spending. Within 2 weeks: conduct line-item expense review. Identify top 5 cost reduction opportunities totaling ${variance['total_variance'] * 2:,.0f} in annual savings."
                ))

        return insights

    def _analyze_customer_concentration(self) -> List[Insight]:
        """Analyze customer revenue concentration."""
        insights = []
        df = self.data.copy()

        if 'customer_id' not in df.columns or 'revenue' not in df.columns:
            return insights

        customer_revenue = df.groupby('customer_id')['revenue'].sum().sort_values(ascending=False)
        total_revenue = customer_revenue.sum()

        if total_revenue == 0:
            return insights

        # Top customer
        top_customer = customer_revenue.index[0]
        top_customer_pct = customer_revenue.iloc[0] / total_revenue * 100

        if top_customer_pct > 25:
            insights.append(self._create_insight(
                severity=Severity.CRITICAL,
                finding=f"Customer '{top_customer}' represents {top_customer_pct:.1f}% of revenue (${customer_revenue.iloc[0]:,.0f})",
                impact=f"LOSS OF THIS CUSTOMER = LOSS OF ${customer_revenue.iloc[0]:,.0f} ANNUAL REVENUE. Business continuity at extreme risk.",
                action=f"IMMEDIATE: (1) Assign dedicated account manager with weekly check-ins, (2) Schedule quarterly business review with executive, (3) Develop 3+ new customers in same segment within 90 days to reduce dependency below 20%"
            ))

        # Top 3 customers
        top_3_pct = customer_revenue.head(3).sum() / total_revenue * 100
        if top_3_pct > 60:
            insights.append(self._create_insight(
                severity=Severity.HIGH,
                finding=f"Top 3 customers represent {top_3_pct:.1f}% of total revenue - dangerously concentrated",
                impact=f"Losing any top customer severely impacts business. Revenue base lacks diversification.",
                action=f"Launch customer diversification program: Target 10 new mid-tier customers ($50K-$200K annual) within 6 months. Focus on: [specific customer profiles]. Budget: $50K for acquisition."
            ))

        return insights

    def _analyze_budget_variance(self) -> List[Insight]:
        """Analyze budget vs actual variance."""
        insights = []
        df = self.data.copy()

        if 'actual' in df.columns and 'budget' in df.columns:
            variance = self.variance_analysis('actual', 'budget')

            if 'error' not in variance:
                if variance['material_variance'] and variance['is_over_budget']:
                    insights.append(self._create_insight(
                        severity=Severity.HIGH,
                        finding=f"Budget variance of {variance['total_variance_pct']:.1f}% (${variance['total_variance']:,.0f} over budget)",
                        impact=f"Variance exceeds materiality threshold of 10%. Management attention required.",
                        action=f"Conduct variance analysis: (1) Categorize variances by driver, (2) Identify one-time vs recurring, (3) Adjust next quarter budget or reduce spending accordingly"
                    ))

        return insights

    def _generate_charts_data(self, kpis: Dict) -> Dict[str, Any]:
        """Generate data for charts."""
        df = self.data.copy()

        if 'period' not in df.columns:
            return {}

        df['period'] = pd.to_datetime(df['period'])
        df = df.sort_values('period')

        # Revenue trend
        revenue_trend = []
        if 'revenue' in df.columns:
            for _, row in df.iterrows():
                period = row['period']
                revenue_trend.append({
                    'period': period.strftime('%Y-%m') if hasattr(period, 'strftime') else str(period),
                    'revenue': float(row['revenue'])
                })

        # Margin trend
        margin_trend = []
        if 'revenue' in df.columns and 'cost_of_goods_sold' in df.columns:
            for _, row in df.iterrows():
                period = row['period']
                margin = ((row['revenue'] - row.get('cost_of_goods_sold', 0)) / row['revenue'] * 100) if row['revenue'] > 0 else 0
                margin_trend.append({
                    'period': period.strftime('%Y-%m') if hasattr(period, 'strftime') else str(period),
                    'margin': round(float(margin), 2)
                })

        return {
            'revenue_trend': revenue_trend,
            'margin_trend': margin_trend
        }
