"""
Risk Engine - Identifies critical risks with 3-6 month outlook.
"""
from typing import List, Dict, Any
from models.analysis_output import Risk
from models.base import Severity, InsightCategory


class RiskEngine:
    """Identifies critical risks with 3-6 month outlook."""

    def identify_risks(self, analysis_results: Dict[str, Any], insights: List) -> List[Risk]:
        """Identify all risks from analysis results."""
        risks = []
        for insight in insights:
            if insight.severity in [Severity.CRITICAL, Severity.HIGH]:
                risk = self._insight_to_risk(insight)
                if risk:
                    risks.append(risk)
        risks.extend(self._identify_kpi_risks(analysis_results))
        return self._deduplicate_risks(risks)

    def _insight_to_risk(self, insight) -> Risk:
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
            if 'days_inventory_outstanding' in kpis and kpis['days_inventory_outstanding'] > 90:
                risks.append(Risk(
                    title="Inventory Obsolescence Risk",
                    category=InsightCategory.INVENTORY,
                    description=f"Days inventory at {kpis['days_inventory_outstanding']:.0f} - too high",
                    probability="Medium-High",
                    financial_impact=f"${kpis.get('total_stock_value', 0):,.0f} at risk",
                    time_to_impact="3-6 months",
                    severity=Severity.HIGH,
                    mitigation="Accelerate turnover, reduce stock levels"
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

    def create_risk_matrix(self, risks: List[Risk]) -> Dict[str, Any]:
        """Create probability vs impact risk matrix."""
        matrix = {
            'critical_high': [], 'critical_low': [],
            'high_high': [], 'high_low': [],
            'medium_high': [], 'medium_low': [],
            'low_high': [], 'low_low': []
        }
        prob_map = {'high': 'high', 'medium-high': 'high', 'medium': 'medium', 'low': 'low'}
        for risk in risks:
            prob_level = prob_map.get(risk.probability.lower(), 'low')
            sev_level = 'high' if risk.severity in [Severity.CRITICAL, Severity.HIGH] else 'low'
            key = f"{sev_level}_{prob_level}"
            if key in matrix:
                matrix[key].append(risk.model_dump())
        return matrix
