"""
Function tools for OpenAI Agents SDK.

Each tool is decorated with @function_tool and can be called by agents.
"""
import json
from typing import Dict, Any, Optional
from datetime import datetime

import pandas as pd

from agents import function_tool

from data_loader.loader import DataLoader
from analyzers.financial_analyzer import FinancialAnalyzer
from analyzers.manufacturing_analyzer import ManufacturingAnalyzer
from analyzers.inventory_analyzer import InventoryAnalyzer
from analyzers.sales_analyzer import SalesAnalyzer
from analyzers.purchase_analyzer import PurchaseAnalyzer


@function_tool
def load_and_validate_data(file_path: str) -> Dict[str, Any]:
    """
    Load data from file and validate quality.
    Returns data summary and quality issues - does not hide problems.

    Args:
        file_path: Path to CSV or Excel file

    Returns:
        Dictionary with data preview, detected type, and quality issues
    """
    loader = DataLoader()
    df = loader.load_file(file_path)
    data_type = loader.data_type
    quality_report = loader.validate_data(df, data_type)

    return {
        "rows": len(df),
        "columns": list(df.columns),
        "detected_type": data_type.value if data_type else "unknown",
        "is_usable": quality_report.is_usable,
        "quality_issues": [issue.model_dump() for issue in quality_report.issues],
        "blocking_issues": quality_report.blocking_issues
    }


@function_tool
def analyze_financials(data_json: str) -> Dict[str, Any]:
    """
    Perform financial analysis on P&L, revenue, expense data.
    Returns insights with specific findings, impacts, and actions.

    Args:
        data_json: JSON string of financial data

    Returns:
        Analysis results with KPIs, insights, and issues
    """
    df = pd.read_json(data_json)
    analyzer = FinancialAnalyzer(df)
    result = analyzer.analyze()
    return result.model_dump()


@function_tool
def analyze_manufacturing(data_json: str) -> Dict[str, Any]:
    """
    Analyze production, wastage, and cost per unit data.

    Args:
        data_json: JSON string of manufacturing data

    Returns:
        Manufacturing analysis with efficiency metrics and issues
    """
    df = pd.read_json(data_json)
    analyzer = ManufacturingAnalyzer(df)
    result = analyzer.analyze()
    return result.model_dump()


@function_tool
def analyze_inventory(data_json: str) -> Dict[str, Any]:
    """
    Analyze stock aging, dead stock, overstock, and turnover.

    Args:
        data_json: JSON string of inventory data

    Returns:
        Inventory analysis with aging breakdown and risk items
    """
    df = pd.read_json(data_json)
    analyzer = InventoryAnalyzer(df)
    result = analyzer.analyze()
    return result.model_dump()


@function_tool
def analyze_sales(data_json: str) -> Dict[str, Any]:
    """
    Analyze sales trends, product performance, customer concentration.

    Args:
        data_json: JSON string of sales data

    Returns:
        Sales analysis with trends, Pareto breakdown, and concentration metrics
    """
    df = pd.read_json(data_json)
    analyzer = SalesAnalyzer(df)
    result = analyzer.analyze()
    return result.model_dump()


@function_tool
def analyze_purchases(data_json: str) -> Dict[str, Any]:
    """
    Analyze purchase patterns and supplier performance.

    Args:
        data_json: JSON string of purchase data

    Returns:
        Purchase analysis with supplier scores and concentration risks
    """
    df = pd.read_json(data_json)
    analyzer = PurchaseAnalyzer(df)
    result = analyzer.analyze()
    return result.model_dump()


@function_tool
def generate_insights(analysis_results: str) -> str:
    """
    Generate actionable insights from analysis results.
    Each insight has: what's wrong, why it matters, exact action.

    Args:
        analysis_results: JSON string of analysis results

    Returns:
        JSON string of structured insights with severity and actions
    """
    from engines.insight_engine import InsightEngine
    import json

    engine = InsightEngine()
    results = json.loads(analysis_results)
    insights = engine.generate_insights(results)

    return json.dumps([i.model_dump() for i in insights])


@function_tool
def generate_recommendations(insights_json: str) -> str:
    """
    Generate prioritized action plan from insights.
    No vague advice - every recommendation is specific.

    Args:
        insights_json: JSON string of insights

    Returns:
        JSON string of recommendations with timeline
    """
    from engines.recommendation_engine import RecommendationEngine
    import json

    engine = RecommendationEngine()
    insights = json.loads(insights_json)

    # Convert to Insight objects if needed
    from models.analysis_output import Insight
    from models.base import InsightCategory, Severity

    insight_objects = []
    for i in insights:
        if isinstance(i, dict):
            insight_objects.append(Insight(**i))

    recommendations = engine.generate_recommendations(insight_objects)
    return json.dumps([r.model_dump() for r in recommendations])


@function_tool
def identify_risks(analysis_results: str) -> str:
    """
    Identify critical risks with 3-6 month outlook.
    Does not hide bad news - surfaces all material risks.

    Args:
        analysis_results: JSON string of all analysis results

    Returns:
        JSON string of risks with probability, impact, and mitigation
    """
    from engines.risk_engine import RiskEngine
    import json

    engine = RiskEngine()
    results = json.loads(analysis_results)

    # Extract insights from results
    all_insights = []
    for domain, result in results.items():
        if isinstance(result, dict) and 'insights' in result:
            all_insights.extend(result['insights'])

    risks = engine.identify_risks(results, all_insights)
    return json.dumps([r.model_dump() for r in risks])


@function_tool
def create_executive_report(
    data_source: str,
    data_type: str,
    executive_summary: str,
    insights_by_category: str,
    critical_risks: str,
    action_plan: str
) -> str:
    """
    Create a complete executive report from analysis components.

    Args:
        data_source: Name of the data source
        data_type: Type of data analyzed
        executive_summary: JSON string of summary points
        insights_by_category: JSON string of categorized insights
        critical_risks: JSON string of risks
        action_plan: JSON string of recommendations

    Returns:
        Complete executive report as JSON string
    """
    from models.analysis_output import ExecutiveReport
    import json

    summary = json.loads(executive_summary)
    insights = json.loads(insights_by_category)
    risks = json.loads(critical_risks)
    actions = json.loads(action_plan)

    report = ExecutiveReport(
        data_source=data_source,
        data_type=data_type,
        data_quality_summary="Analysis completed with all findings reported",
        executive_summary=summary,
        financial_insights=insights.get('financial', []),
        manufacturing_insights=insights.get('manufacturing', []),
        inventory_insights=insights.get('inventory', []),
        sales_insights=insights.get('sales', []),
        critical_risks=risks,
        action_plan=actions
    )

    return report.model_dump_json()
