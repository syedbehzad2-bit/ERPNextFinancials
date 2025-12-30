"""
Insight Engine - Transforms analysis results into structured, actionable insights.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime

from models.analysis_output import Insight, Recommendation, Risk, ExecutiveReport
from models.base import InsightCategory, Severity, Priority, TimeHorizon


class InsightEngine:
    """
    Converts raw analysis into actionable insights.
    Every insight has: What is wrong, Why it matters, Exact action to take.
    """

    def __init__(self):
        self._insights: List[Insight] = []

    def generate_insights(self, analysis_results: Dict[str, Any]) -> List[Insight]:
        """
        Transform analysis results into structured insights.
        """
        self._insights = []

        # Process each domain
        for domain, result in analysis_results.items():
            if not isinstance(result, dict):
                continue

            # Extract insights from each domain
            insights = result.get('insights', [])
            if insights:
                for insight_data in insights:
                    if isinstance(insight_data, dict):
                        insight = Insight(**insight_data)
                        self._insights.append(insight)
                    elif isinstance(insight_data, Insight):
                        self._insights.append(insight_data)

        # Remove duplicates (same finding)
        self._insights = self._deduplicate_insights(self._insights)

        # Sort by severity
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        self._insights.sort(key=lambda x: (severity_order.get(x.severity.value, 4), x.category.value))

        return self._insights

    def _deduplicate_insights(self, insights: List[Insight]) -> List[Insight]:
        """Remove duplicate insights based on finding text."""
        seen = set()
        unique = []

        for insight in insights:
            # Use first 100 chars of finding as key
            key = insight.finding[:100].lower().strip()
            if key and key not in seen:
                seen.add(key)
                unique.append(insight)

        return unique

    def prioritize_insights(self, insights: List[Insight]) -> List[Insight]:
        """Rank insights by severity and business impact."""
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}

        # Sort by severity first, then by category
        return sorted(insights, key=lambda x: (
            severity_order.get(x.severity.value, 4),
            x.category.value
        ))

    def categorize_insights(self, insights: List[Insight]) -> Dict[InsightCategory, List[Insight]]:
        """Group insights by category."""
        categories = {cat: [] for cat in InsightCategory}

        for insight in insights:
            if insight.category in categories:
                categories[insight.category].append(insight)

        # Remove empty categories
        return {k: v for k, v in categories.items() if v}

    def generate_executive_summary(self, insights: List[Insight], kpis: Dict[str, Any] = None) -> List[str]:
        """
        Generate 5-7 bullet executive summary.
        Lead with biggest problems - brutally honest.
        """
        summary = []

        # Count by severity
        critical = [i for i in insights if i.severity == Severity.CRITICAL]
        high = [i for i in insights if i.severity == Severity.HIGH]

        # Lead with critical issues
        if critical:
            for insight in critical[:2]:
                summary.append(f"CRITICAL: {insight.finding}")
        else:
            # If no critical, lead with most impactful high
            if high:
                summary.append(f"HIGH PRIORITY: {high[0].finding}")

        # Add revenue/margin context from KPIs
        if kpis:
            if 'total_revenue' in kpis:
                summary.append(f"Total Revenue: ${kpis['total_revenue']:,.0f}")
            if 'net_margin_pct' in kpis:
                summary.append(f"Net Margin: {kpis['net_margin_pct']:.1f}%")
            if 'revenue_growth' in kpis:
                growth = kpis['revenue_growth']
                direction = "↑" if growth > 0 else "↓"
                summary.append(f"Revenue Growth: {direction} {abs(growth):.1f}%")

        # Inventory/health summary
        if kpis:
            if 'total_stock_value' in kpis:
                summary.append(f"Inventory Value: ${kpis['total_stock_value']:,.0f}")
            if 'days_inventory_outstanding' in kpis:
                summary.append(f"Days Inventory: {kpis['days_inventory_outstanding']:.0f}")

        # Add key action item
        if insights:
            most_urgent = insights[0]
            summary.append(f"IMMEDIATE ACTION: {most_urgent.action[:100]}...")

        # Limit to 7 bullets
        return summary[:7]

    def assess_severity(self, finding: Dict[str, Any]) -> Severity:
        """Determine severity based on finding characteristics."""
        # Check for financial thresholds
        if 'value' in finding or 'amount' in finding or 'revenue' in finding:
            value = finding.get('value', finding.get('amount', finding.get('revenue', 0)))
            if value > 100000:
                return Severity.CRITICAL
            elif value > 50000:
                return Severity.HIGH
            elif value > 10000:
                return Severity.MEDIUM

        # Check for percentage thresholds
        pct = finding.get('pct', finding.get('percentage', 0))
        if pct > 30:
            return Severity.CRITICAL
        elif pct > 20:
            return Severity.HIGH
        elif pct > 10:
            return Severity.MEDIUM

        # Check for specific keywords
        finding_text = str(finding).lower()
        if any(word in finding_text for word in ['critical', 'catastrophic', 'single point of failure']):
            return Severity.CRITICAL
        if any(word in finding_text for word in ['high', 'significant', 'major']):
            return Severity.HIGH
        if any(word in finding_text for word in ['medium', 'moderate']):
            return Severity.MEDIUM

        return Severity.LOW


class RecommendationEngine:
    """
    Generates actionable recommendations from insights.
    No vague advice - every recommendation is specific and measurable.
    """

    def generate_recommendations(self, insights: List[Insight]) -> List[Recommendation]:
        """Convert insights into prioritized action plan."""
        recommendations = []

        for insight in insights:
            # Generate recommendation based on insight
            rec = self._create_recommendation(insight)
            if rec:
                recommendations.append(rec)

        return recommendations

    def _create_recommendation(self, insight: Insight) -> Optional[Recommendation]:
        """Create a specific recommendation from an insight."""
        # Map severity to priority
        priority_map = {
            Severity.CRITICAL: Priority.IMMEDIATE,
            Severity.HIGH: Priority.SHORT_TERM,
            Severity.MEDIUM: Priority.SHORT_TERM,
            Severity.LOW: Priority.MEDIUM_TERM
        }

        # Map category to timeline
        timeline_map = {
            Severity.CRITICAL: TimeHorizon.IMMEDIATE,
            Severity.HIGH: TimeHorizon.IMMEDIATE,
            Severity.MEDIUM: TimeHorizon.SHORT_TERM,
            Severity.LOW: TimeHorizon.MEDIUM_TERM
        }

        priority = priority_map.get(insight.severity, Priority.MEDIUM_TERM)
        timeline = timeline_map.get(insight.severity, TimeHorizon.SHORT_TERM)

        # Estimate financial impact
        metrics = insight.metrics or {}
        estimated_savings = self._estimate_financial_impact(insight)

        # Generate specific "what", "why", "how"
        what, why, how = self._generate_action_components(insight)

        return Recommendation(
            title=f"{insight.severity.value.upper()}: {insight.finding[:50]}...",
            what=what,
            why=insight.impact,
            how=how,
            impact=f"Expected {insight.action[:100]}...",
            priority=priority,
            timeline=timeline,
            estimated_savings=estimated_savings
        )

    def _estimate_financial_impact(self, insight: Insight) -> Optional[float]:
        """Estimate financial impact from insight metrics."""
        metrics = insight.metrics or {}

        if 'value' in metrics:
            return metrics['value'] * 0.3
        if 'dead_value' in metrics:
            return metrics['dead_value'] * 0.5
        if 'excess_value' in metrics:
            return metrics['excess_value'] * 0.2
        if 'variance' in metrics:
            return abs(metrics['variance']) * 0.5

        return None

    def _generate_action_components(self, insight: Insight) -> tuple:
        """Generate what, why, how from insight."""
        category = insight.category

        if category == InsightCategory.FINANCIAL:
            return self._financial_action(insight)
        elif category == InsightCategory.MANUFACTURING:
            return self._manufacturing_action(insight)
        elif category == InsightCategory.INVENTORY:
            return self._inventory_action(insight)
        elif category == InsightCategory.SALES:
            return self._sales_action(insight)
        else:
            return (
                insight.action,
                insight.impact,
                f"Step 1: Analyze {insight.finding[:30]}\nStep 2: Implement {insight.action[:50]}\nStep 3: Track results"
            )

    def _financial_action(self, insight: Insight) -> tuple:
        finding = insight.finding.lower()
        if 'margin' in finding:
            return (
                "Improve gross margin by 5-10 percentage points",
                insight.impact,
                "1) Renegotiate top 5 supplier contracts within 30 days\n2) Increase prices on bottom 20% margin products\n3) Reduce material waste by 15%\n4) Audit overhead costs"
            )
        elif 'revenue' in finding:
            return (
                "Reverse revenue decline and restore growth",
                insight.impact,
                "1) Contact top 20 customers to identify issues\n2) Analyze lost deals in CRM\n3) Launch customer retention campaign\n4) Review pricing strategy"
            )
        elif 'expense' in finding:
            return (
                "Reduce expenses to budget",
                insight.impact,
                "1) Freeze discretionary spending immediately\n2) Conduct line-item expense review within 2 weeks\n3) Identify top 5 cost reduction opportunities\n4) Implement cost controls"
            )
        return (insight.action, insight.impact, "1) Analyze the issue\n2) Create action plan\n3) Execute with milestones\n4) Track progress weekly")

    def _manufacturing_action(self, insight: Insight) -> tuple:
        finding = insight.finding.lower()
        if 'efficiency' in finding:
            return (
                "Improve production efficiency to 95%",
                insight.impact,
                "1) Root cause analysis on worst performing lines\n2) Address equipment downtime\n3) Optimize material flow\n4) Cross-train operators"
            )
        elif 'wastage' in finding:
            return (
                "Reduce wastage to below 5%",
                insight.impact,
                "1) Quality control audit\n2) Review raw material quality\n3) Retrain operators\n4) Set weekly wastage targets"
            )
        return (insight.action, insight.impact, "1) Diagnose root cause\n2) Implement fix\n3) Monitor results daily\n4) Adjust as needed")

    def _inventory_action(self, insight: Insight) -> tuple:
        finding = insight.finding.lower()
        if 'dead' in finding or 'stagnant' in finding:
            return (
                "Liquidate dead stock and recover capital",
                insight.impact,
                "1) Run flash sale at 40% discount on top SKUs\n2) Liquidate remaining via clearance channels\n3) Stop reordering dead stock items\n4) Improve demand forecasting"
            )
        elif 'overstock' in finding:
            return (
                "Reduce overstock by 50%",
                insight.impact,
                "1) Reduce reorder quantities by 40%\n2) Push slow movers via promotions\n3) Adjust safety stock levels\n4) Improve demand planning"
            )
        return (insight.action, insight.impact, "1) Review inventory levels\n2) Identify excess items\n3) Liquidate or adjust\n4) Improve controls")

    def _sales_action(self, insight: Insight) -> tuple:
        finding = insight.finding.lower()
        if 'concentration' in finding or 'customer' in finding:
            return (
                "Diversify customer base to reduce concentration risk",
                insight.impact,
                "1) Assign dedicated account managers to top customers\n2) Launch customer acquisition program\n3) Develop new market segments\n4) Set concentration reduction targets"
            )
        elif 'margin' in finding:
            return (
                "Improve product margins",
                insight.impact,
                "1) Review pricing for bottom performers\n2) Discontinue low-margin products\n3) Increase prices strategically\n4) Negotiate better terms"
            )
        return (insight.action, insight.impact, "1) Analyze sales data\n2) Identify opportunities\n3) Execute sales initiatives\n4) Track results")

    def create_action_plan(self, recommendations: List[Recommendation]) -> Dict[str, Any]:
        """Structure recommendations into action plan."""
        immediate = [r for r in recommendations if r.priority == Priority.IMMEDIATE]
        short_term = [r for r in recommendations if r.priority == Priority.SHORT_TERM]
        medium_term = [r for r in recommendations if r.priority == Priority.MEDIUM_TERM]

        total_savings = sum(r.estimated_savings or 0 for r in recommendations)

        return {
            'immediate_actions': immediate,
            'short_term_actions': short_term,
            'medium_term_actions': medium_term,
            'total_estimated_impact': total_savings,
            'immediate_count': len(immediate),
            'total_count': len(recommendations)
        }


class RiskEngine:
    """
    Identifies critical risks with 3-6 month outlook.
    """

    def identify_risks(self, analysis_results: Dict[str, Any], insights: List[Insight]) -> List[Risk]:
        """Identify all risks from analysis results."""
        risks = []

        for insight in insights:
            if insight.severity in [Severity.CRITICAL, Severity.HIGH]:
                risk = self._insight_to_risk(insight)
                if risk:
                    risks.append(risk)

        risks.extend(self._identify_kpi_risks(analysis_results))
        return self._deduplicate_risks(risks)

    def _insight_to_risk(self, insight: Insight) -> Optional[Risk]:
        prob = "High" if insight.severity == Severity.CRITICAL else "Medium-High"
        return Risk(
            title=f"Risk: {insight.finding[:80]}",
            category=insight.category,
            description=insight.finding,
            probability=prob,
            financial_impact=insight.impact,
            time_to_impact="3-6 months",
            severity=insight.severity,
            mitigation=insight.action
        )

    def _identify_kpi_risks(self, analysis_results: Dict[str, Any]) -> List[Risk]:
        risks = []
        for domain, result in analysis_results.items():
            if not isinstance(result, dict):
                continue
            kpis = result.get('kpis', {})
            if 'net_margin_pct' in kpis and kpis['net_margin_pct'] < 5:
                risks.append(Risk(
                    title="Margin Erosion Risk",
                    category=InsightCategory.FINANCIAL,
                    description=f"Net margin at {kpis['net_margin_pct']:.1f}% - critically low",
                    probability="High",
                    financial_impact="Business at risk of losses",
                    time_to_impact="1-3 months",
                    severity=Severity.CRITICAL,
                    mitigation="Immediate cost reduction and pricing review"
                ))
        return risks

    def _deduplicate_risks(self, risks: List[Risk]) -> List[Risk]:
        seen = set()
        unique = []
        for risk in risks:
            key = risk.title[:50].lower().strip()
            if key and key not in seen:
                seen.add(key)
                unique.append(risk)
        return unique


class ExecutiveReportGenerator:
    """Generates complete executive report with all sections."""

    def generate(self, analysis_results: Dict[str, Any], data_info: Dict[str, Any]) -> ExecutiveReport:
        from engines.insight_engine import InsightEngine
        from engines.recommendation_engine import RecommendationEngine
        from engines.risk_engine import RiskEngine
        from models.base import InsightCategory

        insight_engine = InsightEngine()
        all_insights = []

        for domain, result in analysis_results.items():
            if isinstance(result, dict) and 'insights' in result:
                all_insights.extend(result['insights'])

        insights = insight_engine.generate_insights({'combined': {'insights': all_insights}})
        categorized = insight_engine.categorize_insights(insights)

        kpis = {}
        for domain, result in analysis_results.items():
            if isinstance(result, dict) and 'kpis' in result:
                kpis.update(result['kpis'])

        exec_summary = insight_engine.generate_executive_summary(insights, kpis)

        rec_engine = RecommendationEngine()
        recommendations = rec_engine.generate_recommendations(insights)

        risk_engine = RiskEngine()
        risks = risk_engine.identify_risks(analysis_results, insights)

        return ExecutiveReport(
            data_source=data_info.get('file_name', 'Unknown'),
            data_type=data_info.get('data_type', 'Unknown'),
            data_quality_summary=data_info.get('quality_summary', 'Unknown'),
            data_quality_issues=data_info.get('issues', []),
            executive_summary=exec_summary,
            financial_insights=categorized.get(InsightCategory.FINANCIAL, []),
            manufacturing_insights=categorized.get(InsightCategory.MANUFACTURING, []),
            inventory_insights=categorized.get(InsightCategory.INVENTORY, []),
            sales_insights=categorized.get(InsightCategory.SALES, []),
            critical_risks=risks,
            action_plan=recommendations,
            analysis_results=analysis_results
        )
