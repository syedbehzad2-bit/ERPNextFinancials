"""
Output models for analysis results, insights, recommendations, and risks.
Every insight must have: What is wrong, Why it matters, Exact action to take.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from pydantic import BaseModel, Field

from models.base import (
    Severity,
    Priority,
    TimeHorizon,
    InsightCategory
)


class Insight(BaseModel):
    """
    Single structured insight with required format.

    Every insight MUST have:
    - finding: What is wrong (specific, with numbers)
    - impact: Why it matters (business consequence)
    - action: Exact action to take (specific, measurable)
    """
    category: InsightCategory
    severity: Severity
    finding: str = Field(..., description="What is wrong - specific and factual")
    impact: str = Field(..., description="Why it matters - business consequence")
    action: str = Field(..., description="Exact action to take - specific, measurable")
    metrics: Optional[Dict[str, Any]] = None
    product_sku: Optional[str] = None
    customer_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "category": "INVENTORY",
                "severity": "HIGH",
                "finding": "SKU-1234 has been sitting for 240 days with $45,000 value",
                "impact": "Capital is frozen, warehouse space wasted, product may become obsolete",
                "action": "Run flash sale at 40% discount within 2 weeks to recover $27,000",
                "metrics": {"stock_value": 45000, "days_stagnant": 240}
            }
        }


class Recommendation(BaseModel):
    """
    Actionable recommendation with full context for prioritization.
    """
    title: str
    what: str = Field(..., description="Specific action to take")
    why: str = Field(..., description="Root cause and business reason")
    how: str = Field(..., description="Step-by-step implementation")
    impact: str = Field(..., description="Quantified expected outcome")
    priority: Priority
    timeline: TimeHorizon
    estimated_savings: Optional[float] = None
    estimated_revenue_impact: Optional[float] = None
    risk_reduction: Optional[str] = None
    owner: Optional[str] = None
    resources_needed: Optional[List[str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Liquidate Dead Stock",
                "what": "Run 40% off flash sale on top 5 dead stock SKUs",
                "why": "$156K tied up in dead stock with no movement for 6+ months",
                "how": "1. Select SKUs, 2. Set pricing, 3. Launch campaign, 4. Track results",
                "impact": "Recover $69,000, free warehouse space",
                "priority": "IMMEDIATE",
                "timeline": "0-30 days"
            }
        }


class Risk(BaseModel):
    """
    Identified risk with 3-6 month outlook.
    """
    title: str
    category: InsightCategory
    description: str
    probability: str  # High, Medium, Low
    financial_impact: str  # Specific dollar amount
    time_to_impact: str  # e.g., "3-6 months"
    severity: Severity
    mitigation: str
    early_warning_signals: Optional[List[str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Customer Concentration Risk",
                "category": "SALES",
                "description": "Top customer represents 31% of revenue",
                "probability": "Medium",
                "financial_impact": "$1.95M annual revenue at risk",
                "time_to_impact": "3-6 months if relationship deteriorates",
                "severity": "CRITICAL",
                "mitigation": "Diversify customer base with 5 new $200K+ accounts"
            }
        }


class KPI(BaseModel):
    """
    Key Performance Indicator for display.
    """
    name: str
    value: float
    previous_value: Optional[float] = None
    change_pct: Optional[float] = None
    trend: str  # "up", "down", "stable"
    format: str = "number"  # "number", "currency", "percentage"


class AnalysisResult(BaseModel):
    """
    Complete analysis result for a domain.
    """
    domain: str  # financial, manufacturing, inventory, sales, purchase
    timestamp: datetime = Field(default_factory=datetime.now)
    kpis: Dict[str, Any] = Field(default_factory=dict)
    insights: List[Insight] = Field(default_factory=list)
    data_quality_notes: List[str] = Field(default_factory=list)
    charts_data: Dict[str, Any] = Field(default_factory=dict)

    @property
    def insight_count(self) -> int:
        return len(self.insights)

    @property
    def critical_insights(self) -> List[Insight]:
        return [i for i in self.insights if i.severity == "critical"]

    @property
    def high_insights(self) -> List[Insight]:
        return [i for i in self.insights if i.severity == "high"]


class ExecutiveReport(BaseModel):
    """
    Complete executive report output - the final deliverable.
    """
    generated_at: datetime = Field(default_factory=datetime.now)
    data_source: str
    data_type: str
    data_quality_summary: str
    data_quality_issues: List[str] = Field(default_factory=list)

    # Executive Summary: 5-7 bullet points
    executive_summary: List[str] = Field(..., min_length=5, max_length=7)

    # Insights by category
    financial_insights: List[Insight] = Field(default_factory=list)
    manufacturing_insights: List[Insight] = Field(default_factory=list)
    inventory_insights: List[Insight] = Field(default_factory=list)
    sales_insights: List[Insight] = Field(default_factory=list)

    # Critical Risks
    critical_risks: List[Risk] = Field(default_factory=list)

    # Action Plan
    action_plan: List[Recommendation] = Field(default_factory=list)

    # Raw analysis results for drill-down
    analysis_results: Dict[str, AnalysisResult] = Field(default_factory=dict)

    @property
    def total_insights(self) -> int:
        return (
            len(self.financial_insights) +
            len(self.manufacturing_insights) +
            len(self.inventory_insights) +
            len(self.sales_insights)
        )

    @property
    def critical_count(self) -> int:
        return len([r for r in self.critical_risks if r.severity == "critical"])

    @property
    def immediate_actions(self) -> List[Recommendation]:
        return [r for r in self.action_plan if r.priority == "IMMEDIATE"]

    @property
    def total_estimated_impact(self) -> float:
        total = 0.0
        for rec in self.action_plan:
            if rec.estimated_savings:
                total += rec.estimated_savings
            if rec.estimated_revenue_impact:
                total += rec.estimated_revenue_impact
        return total
