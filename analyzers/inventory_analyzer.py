"""
Inventory analyzer - Stock aging, Dead stock, Overstock, Turnover analysis.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List

from analyzers.base_analyzer import BaseAnalyzer
from models.analysis_output import AnalysisResult, Insight
from models.base import InsightCategory, Severity
from config import settings


class InventoryAnalyzer(BaseAnalyzer):
    """
    Analyzes stock aging, dead stock, overstock, and turnover.
    Every insight has specific numbers and exact actions.
    """

    def get_category(self) -> InsightCategory:
        return InsightCategory.INVENTORY

    def analyze(self) -> AnalysisResult:
        """Run complete inventory analysis."""
        kpis = self.calculate_kpis()
        insights = []

        # Dead stock analysis
        dead_stock_insights = self._identify_dead_stock()
        insights.extend(dead_stock_insights)

        # Overstock analysis
        overstock_insights = self._identify_overstock()
        insights.extend(overstock_insights)

        # Stock aging analysis
        aging_insights = self._analyze_stock_aging()
        insights.extend(aging_insights)

        # Turnover analysis
        turnover_insights = self._analyze_turnover()
        insights.extend(turnover_insights)

        # Stock-to-sales mismatch
        mismatch_insights = self._analyze_stock_sales_mismatch()
        insights.extend(mismatch_insights)

        # Charts data
        charts_data = self._generate_charts_data()

        return AnalysisResult(
            domain="inventory",
            kpis=kpis,
            insights=insights,
            charts_data=charts_data
        )

    def calculate_kpis(self) -> Dict[str, Any]:
        """Calculate inventory KPIs."""
        df = self.data.copy()

        # Total stock value
        if 'quantity' in df.columns and 'unit_cost' in df.columns:
            df['stock_value'] = df['quantity'] * df['unit_cost']
            total_stock_value = df['stock_value'].sum()
        else:
            total_stock_value = 0

        # Count SKUs
        sku_col = 'sku' if 'sku' in df.columns else 'product_id'
        total_skus = df[sku_col].nunique() if sku_col in df.columns else len(df)

        # Average days since receipt
        if 'receipt_date' in df.columns:
            df['receipt_date'] = pd.to_datetime(df['receipt_date'])
            avg_age = (datetime.now() - df['receipt_date']).dt.days.mean()
        else:
            avg_age = 0

        # Inventory turnover (simplified)
        inventory_turnover = 0
        if 'cogs' in df.columns:
            inventory_turnover = df['cogs'].sum() / total_stock_value if total_stock_value > 0 else 0

        days_inventory = 365 / inventory_turnover if inventory_turnover > 0 else 0

        return {
            'total_stock_value': float(total_stock_value),
            'total_skus': int(total_skus),
            'inventory_turnover': round(float(inventory_turnover), 2),
            'days_inventory_outstanding': round(float(days_inventory), 1),
            'average_stock_age_days': round(float(avg_age), 1)
        }

    def _identify_dead_stock(self) -> List[Insight]:
        """Identify dead stock - no movement for threshold days."""
        insights = []
        df = self.data.copy()

        # Determine date column
        date_col = None
        for col in ['last_movement_date', 'last_movement', 'last_activity', 'last_sale']:
            if col in df.columns:
                date_col = col
                break

        if date_col is None:
            return insights

        # Calculate days since movement
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df['days_since_movement'] = (datetime.now() - df[date_col]).dt.days

        # Dead stock threshold
        threshold = settings.dead_stock_threshold_days

        dead_stock = df[df['days_since_movement'] > threshold].copy()

        if len(dead_stock) > 0:
            # Calculate dead stock value
            if 'stock_value' not in dead_stock.columns and 'quantity' in dead_stock.columns and 'unit_cost' in dead_stock.columns:
                dead_stock['stock_value'] = dead_stock['quantity'] * dead_stock['unit_cost']

            total_dead_value = dead_stock['stock_value'].sum() if 'stock_value' in dead_stock.columns else 0
            dead_sku_count = len(dead_stock)

            # Top offenders
            sku_col = 'sku' if 'sku' in dead_stock.columns else 'product_id'
            top_dead = dead_stock.nlargest(5, 'stock_value') if 'stock_value' in dead_stock.columns else dead_stock.head(5)

            top_items_str = ", ".join([
                f"{row.get(sku_col, 'Unknown')} (${row.get('stock_value', 0):,.0f}, {row['days_since_movement']} days)"
                for _, row in top_dead.iterrows()
            ])

            severity = Severity.CRITICAL if total_dead_value > 100000 else Severity.HIGH
            estimated_recovery = total_dead_value * 0.6  # Assume 60% recovery through clearance

            insights.append(self._create_insight(
                severity=severity,
                finding=f"DEAD STOCK ALERT: {dead_sku_count} SKUs with no movement for {threshold}+ days, total value ${total_dead_value:,.0f}. Top 5: {top_items_str}",
                impact=f"${total_dead_value:,.0f} capital frozen. Warehouse space wasted. Obsolescence risk increases daily. Carrying cost: ${total_dead_value * 0.25:,.0f}/year.",
                action=f"IMMEDIATE ACTION PLAN: Week 1 - Run flash sale at 40% discount on top 5 SKUs (recover ~${total_dead_value * 0.15:,.0f}). Week 2-4 - Liquidate remaining dead stock via: (1) Clearance website, (2) Bulk buyer, (3) Donation for tax benefit. Stop reordering these SKUs immediately.",
                metrics={'dead_sku_count': dead_sku_count, 'dead_value': float(total_dead_value), 'threshold_days': threshold}
            ))

        return insights

    def _identify_overstock(self) -> List[Insight]:
        """Identify items with excess coverage."""
        insights = []
        df = self.data.copy()

        if 'days_of_stock' not in df.columns:
            # Try to calculate from quantity and average daily usage
            if 'quantity' in df.columns and 'average_daily_usage' in df.columns:
                df['days_of_stock'] = df['quantity'] / df['average_daily_usage'].replace(0, np.nan)
            else:
                return insights

        overstock = df[df['days_of_stock'] > settings.overstock_threshold_days].copy()

        if len(overstock) > 0:
            # Calculate excess value
            if 'stock_value' not in overstock.columns and 'quantity' in overstock.columns and 'unit_cost' in overstock.columns:
                overstock['stock_value'] = overstock['quantity'] * overstock['unit_cost']

            excess_value = overstock['stock_value'].sum() if 'stock_value' in overstock.columns else 0
            carrying_cost = excess_value * 0.25  # 25% annual holding cost

            # Top overstock items
            sku_col = 'sku' if 'sku' in overstock.columns else 'product_id'
            top_overstock = overstock.nlargest(5, 'days_of_stock')

            top_items_str = ", ".join([
                f"{row.get(sku_col, 'Unknown')} ({row['days_of_stock']:.0f} days)"
                for _, row in top_overstock.iterrows()
            ])

            insights.append(self._create_insight(
                severity=Severity.MEDIUM,
                finding=f"Overstock: {len(overstock)} SKUs with >{settings.overstock_threshold_days} days coverage, excess value ~${excess_value:,.0f}. Top: {top_items_str}",
                impact=f"Excess capital tied up. Storage costs increasing. Carrying cost: ${carrying_cost:,.0f}/year. Risk of obsolescence.",
                action=f"IMMEDIATE: (1) Reduce reorder quantities by 40% for these SKUs, (2) Work with sales to push slow movers via bundles/promotions, (3) Adjust safety stock levels down 30%. Target: reduce overstock value by 50% within 90 days.",
                metrics={'overstock_sku_count': len(overstock), 'excess_value': float(excess_value)}
            ))

        return insights

    def _analyze_stock_aging(self) -> List[Insight]:
        """Analyze stock by age buckets."""
        insights = []
        df = self.data.copy()

        # Determine date column
        date_col = None
        for col in ['receipt_date', 'received_date', 'doc_date']:
            if col in df.columns:
                date_col = col
                break

        if date_col is None:
            return insights

        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df['age_days'] = (datetime.now() - df[date_col]).dt.days

        # Calculate stock value by age
        if 'stock_value' not in df.columns and 'quantity' in df.columns and 'unit_cost' in df.columns:
            df['stock_value'] = df['quantity'] * df['unit_cost']

        # Age buckets
        buckets = {
            '0-30 days': (0, 30),
            '31-60 days': (31, 60),
            '61-90 days': (61, 90),
            '90+ days': (91, 9999)
        }

        aging_summary = {}
        for bucket_name, (min_days, max_days) in buckets.items():
            bucket_df = df[(df['age_days'] >= min_days) & (df['age_days'] <= max_days)]
            if 'stock_value' in df.columns:
                aging_summary[bucket_name] = float(bucket_df['stock_value'].sum())
            else:
                aging_summary[bucket_name] = len(bucket_df)

        total_value = sum(aging_summary.values())
        if total_value > 0:
            old_stock_pct = aging_summary.get('90+ days', 0) / total_value * 100

            if old_stock_pct > 30:
                insights.append(self._create_insight(
                    severity=Severity.HIGH,
                    finding=f"{old_stock_pct:.1f}% of inventory value is 90+ days old (${aging_summary.get('90+ days', 0):,.0f})",
                    impact=f"Inventory is aging poorly. Obsolescence risk is high. Markdown pressure will increase. Customer preference for newer stock.",
                    action=f"INVENTORY AGING ACTION: (1) Implement FIFO enforcement strictly, (2) Review demand planning accuracy, (3) Reduce lead times with key suppliers, (4) Consider bundling old stock with new sales. Target: reduce 90+ day stock below 15%.",
                    metrics=aging_summary
                ))

        return insights

    def _analyze_turnover(self) -> List[Insight]:
        """Analyze inventory turnover by category."""
        insights = []
        df = self.data.copy()

        if 'category' not in df.columns:
            return insights

        # Calculate turnover by category
        if 'cogs' in df.columns and 'stock_value' in df.columns:
            by_category = df.groupby('category').agg({
                'cogs': 'sum',
                'stock_value': 'mean'
            })
            by_category['turnover'] = by_category['cogs'] / by_category['stock_value']
        elif 'quantity' in df.columns and 'quantity_sold' in df.columns:
            by_category = df.groupby('category').agg({
                'quantity_sold': 'sum',
                'quantity': 'mean'
            })
            by_category['turnover'] = by_category['quantity_sold'] / by_category['quantity']
        else:
            return insights

        # Flag low turnover categories
        low_turnover = by_category[by_category['turnover'] < 4]  # Less than 4x per year

        for category, row in low_turnover.iterrows():
            insights.append(self._create_insight(
                severity=Severity.MEDIUM,
                finding=f"Category '{category}' has low turnover of {row['turnover']:.1f}x annually (industry benchmark: 6-8x)",
                impact=f"Capital inefficiency. Working capital tied up in slow-moving products. Storage and handling costs not justified by sales.",
                action=f"CATEGORY RATIONALIZATION for '{category}': (1) SKU rationalization review - cut bottom 20% performers, (2) Adjust safety stock down 30%, (3) Increase prices 5-10% to improve margin, (4) Consider discontinuation of bottom 10 SKUs. Expected savings: ${row['stock_value'] * 0.15:,.0f} in reduced inventory.",
                metrics={'turnover': round(float(row['turnover']), 2), 'category': category}
            ))

        return insights

    def _analyze_stock_sales_mismatch(self) -> List[Insight]:
        """Identify stock vs sales mismatches."""
        insights = []
        df = self.data.copy()

        # Need sales velocity info
        if 'days_since_movement' not in df.columns or 'quantity' not in df.columns:
            return insights

        # High stock + no movement = problem
        high_stock_no_movement = df[(df['days_since_movement'] > 90) & (df['quantity'] > df['quantity'].median())]

        if len(high_stock_no_movement) > 10:
            sku_col = 'sku' if 'sku' in df.columns else 'product_id'
            value = high_stock_no_movement['quantity'].sum() * high_stock_no_movement['unit_cost'].mean() if 'unit_cost' in df.columns else 0

            insights.append(self._create_insight(
                severity=Severity.MEDIUM,
                finding=f"{len(high_stock_no_movement)} SKUs with high stock but no sales for 90+ days",
                impact=f"${value:,.0f} in stagnant inventory. These items are tying up capital without generating returns.",
                action=f"STAGNANT INVENTORY REVIEW: (1) Analyze why these items aren't selling - pricing? competition? obsolescence?, (2) Create promotional plan for next 30 days, (3) After 30 days, liquidate remaining via clearance channels."
            ))

        return insights

    def _generate_charts_data(self) -> Dict[str, Any]:
        """Generate data for charts."""
        df = self.data.copy()

        # Stock aging distribution
        aging_data = []
        if 'age_days' in df.columns and 'stock_value' in df.columns:
            buckets = [(0, 30, '0-30 days'), (31, 60, '31-60 days'), (61, 90, '61-90 days'), (91, 9999, '90+ days')]

            for min_d, max_d, name in buckets:
                bucket_df = df[(df['age_days'] >= min_d) & (df['age_days'] <= max_d)]
                value = bucket_df['stock_value'].sum()
                aging_data.append({'bucket': name, 'value': float(value)})

        # Top SKUs by value
        if 'stock_value' in df.columns:
            sku_col = 'sku' if 'sku' in df.columns else 'product_id'
            top_skus = df.nlargest(10, 'stock_value')[[sku_col, 'stock_value']]
            top_sku_data = [
                {'sku': str(row[sku_col]), 'value': float(row['stock_value'])}
                for _, row in top_skus.iterrows()
            ]
        else:
            top_sku_data = []

        # Turnover by category
        if 'category' in df.columns and 'cogs' in df.columns and 'stock_value' in df.columns:
            by_cat = df.groupby('category').agg({'cogs': 'sum', 'stock_value': 'mean'})
            by_cat['turnover'] = by_cat['cogs'] / by_cat['stock_value']
            turnover_data = [
                {'category': cat, 'turnover': round(float(row['turnover']), 2)}
                for cat, row in by_cat.iterrows()
            ]
        else:
            turnover_data = []

        return {
            'aging_distribution': aging_data,
            'top_skus_by_value': top_sku_data,
            'turnover_by_category': turnover_data
        }
