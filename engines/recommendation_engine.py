"""
Recommendation Engine - Generates actionable recommendations from insights.
"""
from typing import List, Dict, Any, Optional
from models.analysis_output import Recommendation
from models.base import Severity, Priority, TimeHorizon, InsightCategory


class RecommendationEngine:
    """Generates actionable recommendations from insights."""

    def generate_recommendations(self, insights: List) -> List[Recommendation]:
        """Convert insights into prioritized action plan."""
        recommendations = []
        for insight in insights:
            rec = self._create_recommendation(insight)
            if rec:
                recommendations.append(rec)
        return recommendations

    def _create_recommendation(self, insight) -> Optional[Recommendation]:
        priority_map = {
            Severity.CRITICAL: Priority.IMMEDIATE,
            Severity.HIGH: Priority.SHORT_TERM,
            Severity.MEDIUM: Priority.SHORT_TERM,
            Severity.LOW: Priority.MEDIUM_TERM
        }
        timeline_map = {
            Severity.CRITICAL: TimeHorizon.IMMEDIATE,
            Severity.HIGH: TimeHorizon.IMMEDIATE,
            Severity.MEDIUM: TimeHorizon.SHORT_TERM,
            Severity.LOW: TimeHorizon.MEDIUM_TERM
        }

        priority = priority_map.get(insight.severity, Priority.MEDIUM_TERM)
        timeline = timeline_map.get(insight.severity, TimeHorizon.SHORT_TERM)

        what, why, how = self._generate_action_components(insight)
        estimated_savings = self._estimate_financial_impact(insight)

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

    def _estimate_financial_impact(self, insight) -> Optional[float]:
        metrics = insight.metrics or {}
        if 'value' in metrics:
            return metrics['value'] * 0.3
        if 'dead_value' in metrics:
            return metrics['dead_value'] * 0.5
        if 'excess_value' in metrics:
            return metrics['excess_value'] * 0.2
        return None

    def _generate_action_components(self, insight) -> tuple:
        category = insight.category
        if category == InsightCategory.FINANCIAL:
            return self._financial_action(insight)
        elif category == InsightCategory.MANUFACTURING:
            return self._manufacturing_action(insight)
        elif category == InsightCategory.INVENTORY:
            return self._inventory_action(insight)
        elif category == InsightCategory.SALES:
            return self._sales_action(insight)
        return (insight.action, insight.impact, f"Step 1: Analyze\nStep 2: Implement\nStep 3: Track")

    def _financial_action(self, insight) -> tuple:
        finding = insight.finding.lower()
        if 'margin' in finding:
            return ("Improve gross margin by 5-10pp", insight.impact,
                    "1) Renegotiate top 5 supplier contracts\n2) Increase prices on low-margin products\n3) Reduce material waste")
        elif 'revenue' in finding:
            return ("Reverse revenue decline", insight.impact,
                    "1) Contact top customers\n2) Analyze lost deals\n3) Launch retention campaign")
        return (insight.action, insight.impact, "1) Analyze\n2) Plan\n3) Execute")

    def _manufacturing_action(self, insight) -> tuple:
        finding = insight.finding.lower()
        if 'efficiency' in finding:
            return ("Improve efficiency to 95%", insight.impact,
                    "1) Root cause analysis\n2) Address downtime\n3) Optimize flow")
        elif 'wastage' in finding:
            return ("Reduce wastage below 5%", insight.impact,
                    "1) QC audit\n2) Review material quality\n3) Retrain operators")
        return (insight.action, insight.impact, "1) Diagnose\n2) Implement\n3) Monitor")

    def _inventory_action(self, insight) -> tuple:
        finding = insight.finding.lower()
        if 'dead' in finding:
            return ("Liquidate dead stock", insight.impact,
                    "1) Flash sale at 40% off\n2) Clearance channels\n3) Stop reordering")
        return (insight.action, insight.impact, "1) Review\n2) Liquidate\n3) Improve controls")

    def _sales_action(self, insight) -> tuple:
        finding = insight.finding.lower()
        if 'concentration' in finding:
            return ("Diversify customer base", insight.impact,
                    "1) Dedicated account managers\n2) Customer acquisition\n3) New market segments")
        return (insight.action, insight.impact, "1) Analyze\n2) Execute\n3) Track")

    def create_action_plan(self, recommendations: List[Recommendation]) -> Dict[str, Any]:
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
