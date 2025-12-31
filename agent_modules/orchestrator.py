"""
ERP Agent Orchestrator - OpenAI Agents SDK Implementation.

Uses OpenAI Agents SDK with Gemini API via OpenAI-compatible endpoint.
Implements proper agent pattern with tools, handoffs, and Runner.run_sync().
"""
import json
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime

from agents import Agent, Runner, handoff

from config import settings
from config.prompts import (
    GEMINI_SYSTEM_PROMPT,
    FINANCIAL_PROMPT,
    OPERATIONS_PROMPT,
    SALES_PROMPT,
    EXECUTIVE_PROMPT
)
from agent_modules.tools import (
    load_and_validate_data,
    analyze_financials,
    analyze_manufacturing,
    analyze_inventory,
    analyze_sales,
    analyze_purchases,
    generate_insights,
    generate_recommendations,
    identify_risks,
    create_executive_report
)


# ==================== SPECIALIZED AGENTS ====================

# Financial Analysis Agent
financial_agent = Agent(
    name="Financial Analyst",
    instructions=FINANCIAL_PROMPT,
    tools=[
        analyze_financials,
        generate_insights
    ]
)

# Manufacturing Analysis Agent
manufacturing_agent = Agent(
    name="Manufacturing Analyst",
    instructions=OPERATIONS_PROMPT,
    tools=[
        analyze_manufacturing,
        generate_insights
    ]
)

# Inventory Analysis Agent
inventory_agent = Agent(
    name="Inventory Analyst",
    instructions=OPERATIONS_PROMPT,
    tools=[
        analyze_inventory,
        generate_insights
    ]
)

# Sales Analysis Agent
sales_agent = Agent(
    name="Sales Analyst",
    instructions=SALES_PROMPT,
    tools=[
        analyze_sales,
        generate_insights
    ]
)

# Purchase Analysis Agent
purchase_agent = Agent(
    name="Purchase Analyst",
    instructions=SALES_PROMPT,
    tools=[
        analyze_purchases,
        generate_insights
    ]
)

# Executive Summary Agent
executive_agent = Agent(
    name="Executive Advisor",
    instructions=EXECUTIVE_PROMPT,
    tools=[
        generate_recommendations,
        identify_risks,
        create_executive_report
    ]
)


# ==================== MAIN ORCHESTRATOR AGENT ====================

# Main orchestrator with handoffs to specialized agents
orchestrator_agent = Agent(
    name="ERP Intelligence Orchestrator",
    instructions=GEMINI_SYSTEM_PROMPT,
    tools=[
        load_and_validate_data,
        analyze_financials,
        analyze_manufacturing,
        analyze_inventory,
        analyze_sales,
        analyze_purchases,
        generate_insights,
        generate_recommendations,
        identify_risks,
        create_executive_report
    ],
    handoffs=[
        handoff(financial_agent, tool_description_override="Delegate P&L, revenue, margin, and expense analysis"),
        handoff(manufacturing_agent, tool_description_override="Delegate production, wastage, and cost efficiency analysis"),
        handoff(inventory_agent, tool_description_override="Delegate stock aging, dead stock, and turnover analysis"),
        handoff(sales_agent, tool_description_override="Delegate sales trends, product performance, and customer analysis"),
        handoff(purchase_agent, tool_description_override="Delegate supplier performance and purchase analysis"),
        handoff(executive_agent, tool_description_override="Compile executive summary, risks, and action plan")
    ]
)


# ==================== ORCHESTRATOR CLASS ====================

class ERPAgentOrchestrator:
    """
    Main orchestrator for ERP Intelligence Agent.

    Uses OpenAI Agents SDK with Gemini 2.5 Flash.
    Coordinates data loading, analysis, and report generation.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.gemini_api_key
        self.agent = orchestrator_agent

    def analyze(
        self,
        file_path: Optional[str] = None,
        data_frame=None,
        data_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main analysis entry point.

        Args:
            file_path: Path to data file
            data_frame: Pandas DataFrame (if file already loaded)
            data_type: Explicit data type (auto-detected if not provided)

        Returns:
            Complete analysis results with insights and recommendations
        """
        # Build the analysis prompt
        prompt = self._build_analysis_prompt(file_path, data_frame, data_type)

        try:
            # Run the agent with Runner.run_sync()
            result = Runner.run_sync(self.agent, prompt)

            # Parse the result
            return self._parse_result(result.final_output)

        except Exception as e:
            # Fallback to rule-based analysis
            return self._fallback_analysis(file_path, data_frame, data_type)

    def _build_analysis_prompt(
        self,
        file_path: Optional[str],
        data_frame,
        data_type: Optional[str]
    ) -> str:
        """Build the analysis prompt for the agent."""
        prompt = f"""Analyze ERP data and provide comprehensive business intelligence.

Data Source: {file_path or 'Provided DataFrame'}
Data Type: {data_type or 'Auto-detect'}

Requirements:
1. First, load and validate the data file
2. Detect the data type (Financial, Manufacturing, Inventory, Sales, or Purchase)
3. Run appropriate analysis based on data type
4. Generate insights with: What is wrong, Why it matters, Exact action to take
5. Identify critical risks with 3-6 month outlook
6. Create prioritized action plan

Communication Style:
- Be brutally honest - no sugarcoating
- Use specific numbers, percentages, and timeframes
- No vague advice like "improve efficiency"
- Challenge bad decisions directly

Output Structure:
1. Executive Summary (5-7 bullet points)
2. Financial Insights (if applicable)
3. Manufacturing/Operations Insights (if applicable)
4. Inventory/Stock Insights (if applicable)
5. Sales Insights (if applicable)
6. Critical Risks (3-6 month outlook)
7. Action Plan with priorities

Begin analysis now."""

        return prompt

    def _parse_result(self, result: str) -> Dict[str, Any]:
        """Parse agent result into structured output."""
        try:
            # Try to parse as JSON
            return json.loads(result)
        except json.JSONDecodeError:
            # Return as text if not JSON
            return {
                "raw_output": result,
                "generated_at": datetime.now().isoformat(),
                "format": "text"
            }

    def _fallback_analysis(
        self,
        file_path: Optional[str],
        data_frame,
        data_type: Optional[str]
    ) -> Dict[str, Any]:
        """
        Fallback to rule-based analysis if agent fails.
        This ensures the system works even without API access.
        """
        from data_loader.loader import DataLoader
        from models.base import DataType as DT
        from analyzers.financial_analyzer import FinancialAnalyzer
        from analyzers.manufacturing_analyzer import ManufacturingAnalyzer
        from analyzers.inventory_analyzer import InventoryAnalyzer
        from analyzers.sales_analyzer import SalesAnalyzer
        from analyzers.purchase_analyzer import PurchaseAnalyzer

        # Load data
        loader = DataLoader()
        if file_path:
            df = loader.load_file(file_path)
        elif data_frame is not None:
            # data_frame is already a DataFrame, use it directly
            if hasattr(data_frame, 'shape'):  # It's a DataFrame
                df = data_frame.copy()
            else:
                df = loader.load_file(file_obj=data_frame)
        else:
            raise ValueError("Either file_path or data_frame must be provided")

        # Detect type
        detected_type = data_type or loader.data_type.value

        # Run rule-based analysis
        analyzer_map = {
            DT.FINANCIAL: FinancialAnalyzer,
            DT.MANUFACTURING: ManufacturingAnalyzer,
            DT.INVENTORY: InventoryAnalyzer,
            DT.SALES: SalesAnalyzer,
            DT.PURCHASE: PurchaseAnalyzer
        }

        analyzer_class = analyzer_map.get(DT(detected_type))
        if not analyzer_class:
            raise ValueError(f"Unknown data type: {detected_type}")

        analyzer = analyzer_class(df)
        result = analyzer.analyze()

        # Generate insights
        from engines.insight_engine import InsightEngine
        from engines.recommendation_engine import RecommendationEngine
        from engines.risk_engine import RiskEngine
        from models.base import InsightCategory

        insight_engine = InsightEngine()
        insights = insight_engine.generate_insights({detected_type: result.model_dump()})
        categorized = insight_engine.categorize_insights(insights)

        kpis = result.kpis
        exec_summary = insight_engine.generate_executive_summary(insights, kpis)

        rec_engine = RecommendationEngine()
        recommendations = rec_engine.generate_recommendations(insights)

        risk_engine = RiskEngine()
        risks = risk_engine.identify_risks({detected_type: result.model_dump()}, insights)

        return {
            "generated_at": datetime.now().isoformat(),
            "data_source": file_path,
            "data_type": detected_type,
            "data_quality": loader.get_quality_summary(),
            "executive_summary": exec_summary,
            "kpis": kpis,
            "insights_by_category": {
                "financial": [i.model_dump() for i in categorized.get(InsightCategory.FINANCIAL, [])],
                "manufacturing": [i.model_dump() for i in categorized.get(InsightCategory.MANUFACTURING, [])],
                "inventory": [i.model_dump() for i in categorized.get(InsightCategory.INVENTORY, [])],
                "sales": [i.model_dump() for i in categorized.get(InsightCategory.SALES, [])]
            },
            "critical_risks": [r.model_dump() for r in risks],
            "action_plan": [r.model_dump(mode='json') for r in recommendations],
            "charts_data": result.charts_data,
            "total_insights": len(insights),
            "critical_count": len([r for r in risks if r.severity.value == "critical"]),
            "analysis_mode": "rule_based_fallback"
        }

    async def analyze_async(
        self,
        file_path: Optional[str] = None,
        data_frame=None,
        data_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Async version of analyze for advanced use cases.
        """
        prompt = self._build_analysis_prompt(file_path, data_frame, data_type)

        result = await Runner.run(self.agent, prompt)
        return self._parse_result(result.final_output)

    def analyze_multiple(
        self,
        files: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze multiple data files and aggregate results.

        Args:
            files: List of dicts with 'path' or 'data_frame' and optional 'data_type'

        Returns:
            Aggregated analysis across all files
        """
        all_results = {}
        all_insights = []

        for file_info in files:
            result = self.analyze(
                file_path=file_info.get('path'),
                data_frame=file_info.get('data_frame'),
                data_type=file_info.get('data_type')
            )
            all_results[file_info.get('name', 'unknown')] = result

            # Collect insights
            for category, insights in result.get('insights_by_category', {}).items():
                all_insights.extend(insights)

        # Cross-domain analysis
        cross_domain_insights = self._generate_cross_domain_insights(all_results)

        # Aggregate summary
        total_revenue = sum(
            r.get('kpis', {}).get('total_revenue', 0)
            for r in all_results.values()
        )
        total_insights = sum(r.get('total_insights', 0) for r in all_results.values())
        critical_count = sum(r.get('critical_count', 0) for r in all_results.values())

        return {
            "individual_reports": all_results,
            "cross_domain_insights": cross_domain_insights,
            "aggregated_summary": {
                "total_revenue": total_revenue,
                "total_insights": total_insights,
                "critical_issues": critical_count,
                "reports_count": len(all_results)
            },
            "generated_at": datetime.now().isoformat()
        }

    def _generate_cross_domain_insights(self, all_insights: List) -> List[Dict]:
        """Generate insights that span multiple data domains."""
        insights = []

        # Helper to get category from dict or object
        def get_category(item):
            if hasattr(item, 'model_dump'):
                return item.model_dump().get('category', '').lower()
            elif isinstance(item, dict):
                return item.get('category', '').lower()
            return str(item).lower()

        # Example: Check for inventory-sales mismatch
        inventory_issues = [i for i in all_insights if 'inventory' in get_category(i)]
        sales_issues = [i for i in all_insights if 'sales' in get_category(i) or 'revenue' in get_category(i)]

        if len(inventory_issues) > 2 and len(sales_issues) > 0:
            insights.append({
                "finding": "Multiple inventory issues detected alongside sales concerns",
                "impact": "Potential inventory-sales mismatch affecting working capital",
                "action": "Conduct cross-functional review of inventory and sales planning",
                "severity": "medium"
            })

        # Check for financial-manufacturing connection
        financial_issues = [i for i in all_insights if 'financial' in get_category(i)]
        mfg_issues = [i for i in all_insights if 'manufacturing' in get_category(i)]

        if len(financial_issues) > 1 and len(mfg_issues) > 1:
            insights.append({
                "finding": "Financial costs correlated with manufacturing issues",
                "impact": "Production inefficiencies may be driving up costs",
                "action": "Analyze cost drivers in manufacturing process",
                "severity": "medium"
            })

        # Check for purchase-inventory connection
        purchase_issues = [i for i in all_insights if 'purchase' in get_category(i)]

        if len(inventory_issues) > 1 and len(purchase_issues) > 0:
            insights.append({
                "finding": "Inventory issues may relate to purchase/supplier performance",
                "impact": "Supplier delays or quality issues affecting inventory levels",
                "action": "Review supplier performance metrics and lead times",
                "severity": "low"
            })

        return insights

    def analyze_multi_file(
        self,
        data_frames: Dict[str, Any],
        analysis_level: str = "Comprehensive"
    ) -> Dict[str, Any]:
        """
        Analyze multiple data files and generate cross-domain insights.
        ONLY analyzes domains for which data is actually uploaded.

        Args:
            data_frames: Dict mapping data_type (lowercase) to DataFrame
                         e.g., {'financial': df, 'sales': df, 'inventory': df}
            analysis_level: "Summary", "Detailed", or "Comprehensive"

        Returns:
            Complete multi-file analysis with cross-domain insights
        """
        from models.base import DataType as DT
        from analyzers.financial_analyzer import FinancialAnalyzer
        from analyzers.manufacturing_analyzer import ManufacturingAnalyzer
        from analyzers.inventory_analyzer import InventoryAnalyzer
        from analyzers.sales_analyzer import SalesAnalyzer
        from analyzers.purchase_analyzer import PurchaseAnalyzer
        from engines.insight_engine import InsightEngine
        from engines.recommendation_engine import RecommendationEngine
        from engines.risk_engine import RiskEngine
        from models.base import InsightCategory
        from data_loader.schema_detector import SchemaDetector

        all_results = {}
        all_kpis = {}
        all_charts = {}
        all_insights = []
        enabled_domains = []
        schema_detector = SchemaDetector()

        # Analyze each data frame
        analyzer_map = {
            DT.FINANCIAL: FinancialAnalyzer,
            DT.MANUFACTURING: ManufacturingAnalyzer,
            DT.INVENTORY: InventoryAnalyzer,
            DT.SALES: SalesAnalyzer,
            DT.PURCHASE: PurchaseAnalyzer
        }

        for data_type_str, df in data_frames.items():
            try:
                # Map string to DataType enum
                dt_map = {
                    'financial': DT.FINANCIAL,
                    'manufacturing': DT.MANUFACTURING,
                    'inventory': DT.INVENTORY,
                    'sales': DT.SALES,
                    'purchase': DT.PURCHASE
                }
                dt_enum = dt_map.get(data_type_str.lower())

                if not dt_enum or dt_enum not in analyzer_map:
                    continue

                # CRITICAL: Validate schema before running analyzer
                schema_match = schema_detector.create_schema_match(df, dt_enum)

                # Only run analyzer if confidence is high enough and required columns exist
                if schema_match.confidence < 0.5:
                    continue

                # Check for required columns
                required_fields = schema_detector._get_required_fields(dt_enum)
                matched_fields = [m.expected_field for m in schema_match.column_mappings]
                required_matched = [f for f in required_fields if f in matched_fields]

                # Skip if less than 50% of required fields are present
                if len(required_matched) / max(len(required_fields), 1) < 0.5:
                    continue

                # Normalize columns before analysis
                df_normalized = schema_detector.normalize_columns(df, dt_enum)

                # Run analyzer
                analyzer = analyzer_map[dt_enum](df_normalized)
                result = analyzer.analyze()
                all_results[data_type_str] = result.model_dump()
                all_kpis[data_type_str] = result.kpis
                all_charts[data_type_str] = result.charts_data
                enabled_domains.append(data_type_str)

            except Exception as e:
                # Skip problematic data
                continue

        # ONLY generate insights for enabled domains (data-driven)
        if not enabled_domains:
            return {
                "generated_at": datetime.now().isoformat(),
                "data_source": "multi_file",
                "data_types": [],
                "enabled_domains": [],
                "data_quality": {},
                "executive_summary": ["No valid data detected. Please upload files with required columns."],
                "kpis": {},
                "insights_by_category": {},
                "cross_domain_insights": [],
                "critical_risks": [],
                "action_plan": [],
                "charts_data": {},
                "total_insights": 0,
                "critical_count": 0,
                "analysis_mode": f"multi_file_{analysis_level.lower()}",
                "files_analyzed": 0
            }

        # Generate unified insights ONLY from enabled domains
        insight_engine = InsightEngine()
        insights = insight_engine.generate_insights(all_results)
        categorized = insight_engine.categorize_insights(insights)

        # Generate cross-domain insights ONLY if multiple domains enabled
        cross_domain_insights = []
        if len(enabled_domains) > 1:
            cross_domain_insights = self._generate_cross_domain_insights(insights)

        # Generate recommendations ONLY from actual insights
        rec_engine = RecommendationEngine()
        recommendations = rec_engine.generate_recommendations(insights + cross_domain_insights)

        # Generate risks ONLY from actual results
        risk_engine = RiskEngine()
        risks = risk_engine.identify_risks(all_results, insights)

        # Generate executive summary ONLY from actual data
        exec_summary = insight_engine.generate_executive_summary(insights, all_kpis)

        # Calculate totals
        total_insights = len(insights) + len(cross_domain_insights)
        critical_count = len([r for r in risks if r.severity.value == "critical"])

        # Build insights_by_category ONLY for enabled domains
        insights_by_category = {}
        if 'financial' in enabled_domains:
            insights_by_category['financial'] = [i.model_dump() for i in categorized.get(InsightCategory.FINANCIAL, [])]
        if 'manufacturing' in enabled_domains:
            insights_by_category['manufacturing'] = [i.model_dump() for i in categorized.get(InsightCategory.MANUFACTURING, [])]
        if 'inventory' in enabled_domains:
            insights_by_category['inventory'] = [i.model_dump() for i in categorized.get(InsightCategory.INVENTORY, [])]
        if 'sales' in enabled_domains:
            insights_by_category['sales'] = [i.model_dump() for i in categorized.get(InsightCategory.SALES, [])]
        if 'purchase' in enabled_domains:
            insights_by_category['purchase'] = [i.model_dump() for i in categorized.get(InsightCategory.PURCHASE, [])]

        return {
            "generated_at": datetime.now().isoformat(),
            "data_source": "multi_file",
            "data_types": enabled_domains,
            "enabled_domains": enabled_domains,
            "data_quality": {},
            "executive_summary": exec_summary,
            "kpis": all_kpis,
            "insights_by_category": insights_by_category,
            "cross_domain_insights": [i.model_dump() if hasattr(i, 'model_dump') else i for i in cross_domain_insights],
            "critical_risks": [r.model_dump() for r in risks],
            "action_plan": [r.model_dump(mode='json') for r in recommendations],
            "charts_data": all_charts,
            "total_insights": total_insights,
            "critical_count": critical_count,
            "analysis_mode": f"multi_file_{analysis_level.lower()}",
            "files_analyzed": len(enabled_domains)
        }


# ==================== CONVENIENCE FUNCTIONS ====================

def analyze_file(file_path: str) -> Dict[str, Any]:
    """Convenience function to analyze a file."""
    orchestrator = ERPAgentOrchestrator()
    return orchestrator.analyze(file_path=file_path)


def analyze_dataframe(df, data_type: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function to analyze a DataFrame."""
    orchestrator = ERPAgentOrchestrator()
    return orchestrator.analyze(data_frame=df, data_type=data_type)
