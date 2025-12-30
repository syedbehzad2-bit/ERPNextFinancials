"""
Results page - Display analysis results with charts and insights.
Supports single and multi-file analysis results.
"""
import streamlit as st

from ui.components.charts import (
    render_kpi_cards, render_revenue_trend_chart, render_margin_chart,
    render_aging_chart, render_pareto_chart, render_efficiency_chart,
    render_wastage_chart, render_spend_by_supplier_chart,
    render_delivery_performance_chart, render_lead_time_trend_chart
)
from ui.components.results_display import (
    render_executive_summary, render_insights_section,
    render_risks_section, render_action_plan, render_data_quality_warning,
    render_insight_count_summary
)
from ui.styles import STYLES


def render_results_page() -> None:
    """Render the analysis results page."""
    st.markdown(STYLES, unsafe_allow_html=True)

    st.header("Analysis Results")

    if 'analysis_results' not in st.session_state or st.session_state.analysis_results is None:
        st.warning("No analysis results available. Please run analysis first.")
        if st.button("Go to Analysis"):
            st.session_state.current_page = 'analysis'
            st.rerun()
        return

    results = st.session_state.analysis_results
    config = st.session_state.get('analysis_config', {})
    is_multi_file = config.get('is_multi_file', False)
    files_analyzed = results.get('files_analyzed', 1)

    # Multi-file banner
    if is_multi_file or files_analyzed > 1:
        st.markdown(f"""
        <div class="card-3d" style="background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%); padding: 1rem; border-radius: 16px; margin-bottom: 1rem; border: 1px solid rgba(139, 92, 246, 0.3);">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="font-size: 2rem;">🔗</div>
                <div>
                    <div style="color: #1e293b; font-size: 1.2rem; font-weight: 600;">Cross-File Analysis Complete</div>
                    <div style="color: #64748b;">Analyzed {files_analyzed} data sources with cross-domain insights</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Data quality banner if issues exist
    data_quality = results.get('data_quality', {})
    if data_quality and not data_quality.get('is_usable', True):
        render_data_quality_warning(data_quality.get('critical_issues', []))

    # Executive Summary
    executive_summary = results.get('executive_summary', [])
    if executive_summary:
        render_executive_summary(executive_summary)

    st.markdown("---")

    # KPI Cards - Handle multi-file KPIs
    kpis = results.get('kpis', {})
    if kpis:
        st.subheader("Key Performance Indicators")

        # Check if multi-file KPIs
        if isinstance(kpis, dict) and any(k in kpis for k in ['financial', 'manufacturing', 'inventory', 'sales', 'purchase']):
            # Multi-file KPIs - show tabs
            tab_names = []
            for dtype in ['financial', 'manufacturing', 'inventory', 'sales', 'purchase']:
                if dtype in kpis and kpis[dtype]:
                    type_names = {'financial': '💰 Financial', 'manufacturing': '🏭 Manufacturing',
                                  'inventory': '📦 Inventory', 'sales': '💵 Sales', 'purchase': '🛒 Purchase'}
                    tab_names.append(type_names.get(dtype, dtype.title()))

            if tab_names:
                tabs = st.tabs(tab_names)
                tab_idx = 0
                for dtype in ['financial', 'manufacturing', 'inventory', 'sales', 'purchase']:
                    if dtype in kpis and kpis[dtype]:
                        with tabs[tab_idx]:
                            render_kpi_cards(kpis[dtype])
                        tab_idx += 1
        else:
            # Single file KPIs
            render_kpi_cards(kpis)

    st.markdown("---")

    # Charts based on data type
    charts_data = results.get('charts_data', {})
    data_type = results.get('data_type', '')
    data_types = results.get('data_types', [])

    if charts_data:
        st.subheader("Visualizations")

        # Check if multi-file charts
        if isinstance(charts_data, dict) and any(k in charts_data for k in ['financial', 'manufacturing', 'inventory', 'sales', 'purchase']):
            # Multi-file charts
            chart_tabs = st.tabs([
                f"📊 {dtype.title()}" for dtype in ['financial', 'manufacturing', 'inventory', 'sales', 'purchase']
                if dtype in charts_data and charts_data[dtype]
            ])

            chart_idx = 0
            for dtype in ['financial', 'manufacturing', 'inventory', 'sales', 'purchase']:
                if dtype in charts_data and charts_data[dtype]:
                    with chart_tabs[chart_idx]:
                        render_charts_for_type(charts_data[dtype], dtype)
                    chart_idx += 1
        else:
            # Single file charts
            render_charts_for_type(charts_data, data_type)

    st.markdown("---")

    # Cross-Domain Insights (if multi-file)
    cross_domain = results.get('cross_domain_insights', [])
    if cross_domain:
        st.subheader("🔗 Cross-Domain Insights")
        st.markdown("""
        <div class="card-3d" style="padding: 1.5rem; border-left: 4px solid #8b5cf6;">
        """, unsafe_allow_html=True)

        for insight in cross_domain:
            # Handle both dict and object types
            if hasattr(insight, 'model_dump'):
                insight = insight.model_dump()
            elif not isinstance(insight, dict):
                continue

            severity_colors = {
                'critical': '#ff4b4b',
                'high': '#ffa500',
                'medium': '#ffd700',
                'low': '#4caf50'
            }
            color = severity_colors.get(insight.get('severity', 'medium'), '#4caf50')

            st.markdown(f"""
            <div style="background: rgba(139, 92, 246, 0.1); padding: 1rem; border-radius: 12px; margin-bottom: 1rem; border-left: 4px solid {color};">
                <div style="color: #1e293b; font-weight: 600; margin-bottom: 0.5rem;">{insight.get('finding', 'N/A')}</div>
                <div style="color: #64748b; font-size: 0.9rem; margin-bottom: 0.5rem;">Impact: {insight.get('impact', 'N/A')}</div>
                <div style="color: #8b5cf6; font-size: 0.85rem;">💡 {insight.get('action', 'N/A')}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")

    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📋 Summary",
        "💰 Financial",
        "🏭 Manufacturing",
        "📦 Inventory",
        "📈 Sales",
        "⚠️ Critical Risks",
        "✅ Action Plan"
    ])

    with tab1:
        render_insight_count_summary(results.get('insights_by_category', {}))

        # Show files analyzed
        if is_multi_file or files_analyzed > 1:
            st.markdown("### 📁 Data Sources Analyzed")
            for f in config.get('files', []):
                st.markdown(f"• **{f['file_name']}** ({f['data_type'].title()})")

    with tab2:
        insights = results.get('insights_by_category', {}).get('financial', [])
        render_insights_section("Financial Insights", insights, icon="💰")

    with tab3:
        insights = results.get('insights_by_category', {}).get('manufacturing', [])
        render_insights_section("Manufacturing & Operations Insights", insights, icon="🏭")

    with tab4:
        insights = results.get('insights_by_category', {}).get('inventory', [])
        render_insights_section("Inventory & Stock Insights", insights, icon="📦")

    with tab5:
        insights = results.get('insights_by_category', {}).get('sales', [])
        render_insights_section("Sales Insights", insights, icon="📈")

    with tab6:
        risks = results.get('critical_risks', [])
        render_risks_section(risks)

    with tab7:
        action_plan = results.get('action_plan', {})
        recommendations = []
        recommendations.extend(action_plan.get('immediate', []))
        recommendations.extend(action_plan.get('short_term', []))
        recommendations.extend(action_plan.get('medium_term', []))
        render_action_plan(recommendations)

    # Export options
    st.markdown("---")
    st.subheader("Export Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📄 Export as JSON"):
            import json
            st.download_button(
                label="Download JSON",
                data=json.dumps(results, indent=2, default=str),
                file_name="erp_analysis_results.json",
                mime="application/json"
            )

    with col2:
        if st.button("📊 Export Summary"):
            summary_text = generate_text_summary(results, is_multi_file)
            st.download_button(
                label="Download Summary",
                data=summary_text,
                file_name="erp_analysis_summary.txt",
                mime="text/plain"
            )

    with col3:
        if st.button("🔄 New Analysis"):
            st.session_state.analysis_results = None
            st.session_state.uploaded_files = []
            st.session_state.current_page = 'upload'
            st.rerun()


def render_charts_for_type(charts_data: dict, data_type: str) -> None:
    """Render charts for a specific data type."""
    if not charts_data:
        return

    data_type = data_type.lower()

    # Financial charts
    if data_type == 'financial':
        col1, col2 = st.columns(2)
        with col1:
            revenue_trend = charts_data.get('revenue_trend', [])
            if revenue_trend:
                render_revenue_trend_chart(revenue_trend)
        with col2:
            margin_trend = charts_data.get('margin_trend', [])
            if margin_trend:
                render_margin_chart(margin_trend)

    # Manufacturing charts
    elif data_type == 'manufacturing':
        col1, col2 = st.columns(2)
        efficiency_data = charts_data.get('efficiency_by_product', [])
        if efficiency_data:
            with col1:
                render_efficiency_chart(efficiency_data)
        wastage_data = charts_data.get('wastage_by_product', [])
        if wastage_data:
            with col2:
                render_wastage_chart(wastage_data)

    # Inventory charts
    elif data_type == 'inventory':
        col1, col2 = st.columns(2)
        aging_data = charts_data.get('aging_distribution', [])
        if aging_data:
            with col1:
                render_aging_chart(aging_data)
        turnover_data = charts_data.get('turnover_by_category', [])
        if turnover_data:
            with col2:
                render_pareto_chart(turnover_data)

    # Sales charts
    elif data_type == 'sales':
        col1, col2 = st.columns(2)
        revenue_trend = charts_data.get('revenue_trend', [])
        if revenue_trend:
            with col1:
                render_revenue_trend_chart(revenue_trend)
        pareto_data = charts_data.get('top_products', [])
        if pareto_data:
            with col2:
                render_pareto_chart(pareto_data)

    # Purchase charts
    elif data_type == 'purchase':
        col1, col2 = st.columns(2)
        spend_data = charts_data.get('spend_by_supplier', [])
        if spend_data:
            with col1:
                render_spend_by_supplier_chart(spend_data)
        delivery_data = charts_data.get('delivery_performance', [])
        if delivery_data:
            with col2:
                render_delivery_performance_chart(delivery_data)
        lead_time_data = charts_data.get('lead_time_trend', [])
        if lead_time_data:
            render_lead_time_trend_chart(lead_time_data)


def generate_text_summary(results: dict, is_multi_file: bool = False) -> str:
    """Generate text summary for export."""
    lines = [
        "ERP INTELLIGENCE ANALYSIS REPORT",
        "=" * 50,
        f"Generated: {results.get('generated_at', 'Unknown')}",
        f"Analysis Mode: {results.get('analysis_mode', 'Standard')}",
    ]

    if is_multi_file or results.get('files_analyzed', 0) > 1:
        data_types = results.get('data_types', [])
        lines.append(f"Data Sources: {', '.join(d.title() for d in data_types)}")
    else:
        lines.append(f"Data Type: {results.get('data_type', 'Unknown').title()}")

    lines.extend(["", "=" * 50, "EXECUTIVE SUMMARY", "=" * 50])

    for point in results.get('executive_summary', []):
        lines.append(f"• {point}")

    # Cross-domain insights
    cross_domain = results.get('cross_domain_insights', [])
    if cross_domain:
        lines.extend(["", "=" * 50, "CROSS-DOMAIN INSIGHTS", "=" * 50])
        for i, insight in enumerate(cross_domain, 1):
            lines.append(f"\n{i}. {insight.get('finding', 'N/A')}")
            lines.append(f"   Impact: {insight.get('impact', 'N/A')}")
            lines.append(f"   Action: {insight.get('action', 'N/A')}")

    lines.extend(["", "=" * 50, "KEY INSIGHTS BY CATEGORY", "=" * 50])

    for category, insights in results.get('insights_by_category', {}).items():
        if insights:
            lines.append(f"\n{category.upper()}:")
            for i, insight in enumerate(insights[:5], 1):
                lines.append(f"  {i}. {insight.get('finding', 'N/A')}")

    lines.extend(["", "=" * 50, "CRITICAL RISKS", "=" * 50])
    for risk in results.get('critical_risks', []):
        lines.append(f"• {risk.get('title', 'N/A')}: {risk.get('description', 'N/A')}")

    lines.extend(["", "=" * 50, "ACTION PLAN", "=" * 50])
    action_plan = results.get('action_plan', {})
    for priority, actions in [('Immediate', 'immediate'), ('Short-term', 'short_term'), ('Medium-term', 'medium_term')]:
        if action_plan.get(actions):
            lines.append(f"\n{priority} Actions:")
            for action in action_plan[actions]:
                lines.append(f"  • {action.get('title', 'N/A')}")

    lines.extend(["", "=" * 50, f"Total Insights: {results.get('total_insights', 0)}", "=" * 50])

    return "\n".join(lines)
