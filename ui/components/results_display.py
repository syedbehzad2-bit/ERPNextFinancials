"""
Results display components for insights, risks, and action plans.
"""
import streamlit as st
from typing import List, Dict, Any


def render_executive_summary(summary_points: List[str]) -> None:
    """Render the 5-7 bullet executive summary."""
    st.markdown("### Executive Summary")
    st.markdown("*Brutally honest assessment - no sugarcoating*")

    st.markdown('<div class="executive-summary">', unsafe_allow_html=True)
    for i, point in enumerate(summary_points, 1):
        # Highlight critical points
        if 'CRITICAL' in point or 'HIGH PRIORITY' in point:
            st.markdown(f"**{i}.** 🔴 {point}")
        else:
            st.markdown(f"**{i}.** {point}")
    st.markdown('</div>', unsafe_allow_html=True)


def render_insights_section(title: str, insights: List[Dict], icon: str = "💡") -> None:
    """Render an insights section with structured format."""
    st.markdown(f"### {icon} {title}")

    if not insights:
        st.info("No insights available for this category")
        return

    severity_colors = {
        'critical': '#FF4B4B',
        'high': '#FFA500',
        'medium': '#FFD700',
        'low': '#90EE90'
    }

    for i, insight in enumerate(insights, 1):
        # Handle both dict and object types
        if hasattr(insight, 'model_dump'):
            insight = insight.model_dump()
        elif not isinstance(insight, dict):
            continue

        severity = insight.get('severity', 'medium')
        color = severity_colors.get(severity, '#888')

        st.markdown(f"""
        <div class="insight-card insight-{severity}" style="margin-top: 1rem;">
            <p class="insight-finding">
                <span style="color: {color};">●</span>
                Finding {i}: {insight.get('finding', 'N/A')}
            </p>
            <p class="insight-impact"><strong>Impact:</strong> {insight.get('impact', 'N/A')}</p>
            <div class="insight-action">
                <strong>ACTION:</strong> {insight.get('action', 'N/A')}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_risks_section(risks: List[Dict]) -> None:
    """Render critical risks with 3-6 month outlook."""
    st.markdown("### ⚠️ Critical Risks (3-6 Month Outlook)")

    if not risks:
        st.success("No critical risks identified")
        return

    st.markdown('<div class="risk-section">', unsafe_allow_html=True)

    for i, risk in enumerate(risks, 1):
        # Handle both dict and object types
        if hasattr(risk, 'model_dump'):
            risk = risk.model_dump()
        elif not isinstance(risk, dict):
            continue

        severity = risk.get('severity', 'medium')
        severity_colors = {
            'critical': '🔴 CRITICAL',
            'high': '🟠 HIGH',
            'medium': '🟡 MEDIUM',
            'low': '🟢 LOW'
        }

        with st.expander(f"{severity_colors.get(severity, '⚪')} Risk {i}: {risk.get('title', 'Unnamed Risk')}", expanded=True):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**Probability:** {risk.get('probability', 'Unknown')}")
                st.markdown(f"**Financial Impact:** {risk.get('financial_impact', 'Unknown')}")
                st.markdown(f"**Time to Impact:** {risk.get('time_to_impact', 'Unknown')}")

            with col2:
                st.markdown(f"**Category:** {risk.get('category', 'Unknown')}")

            st.markdown(f"**Description:** {risk.get('description', 'N/A')}")
            st.markdown(f"**Mitigation:** {risk.get('mitigation', 'N/A')}")

    st.markdown('</div>', unsafe_allow_html=True)


def render_action_plan(recommendations: List[Dict]) -> None:
    """Render prioritized action plan."""
    st.markdown("### Action Plan")

    if not recommendations:
        st.info("No recommendations generated")
        return

    # Group by priority - handle both dict and object types
    def get_priority(r):
        if hasattr(r, 'priority'):
            return r.priority if isinstance(r.priority, str) else r.priority.value
        return r.get('priority', 'medium') if isinstance(r, dict) else 'medium'

    immediate = [r for r in recommendations if get_priority(r) == 'immediate']
    short_term = [r for r in recommendations if get_priority(r) == 'short_term']
    medium_term = [r for r in recommendations if get_priority(r) == 'medium_term']

    # Immediate actions
    if immediate:
        st.markdown("#### 🔴 Immediate (0-30 days)")
        for rec in immediate:
            render_recommendation_card(rec, 'immediate')

    # Short-term actions
    if short_term:
        st.markdown("#### 🟠 Short-term (1-3 months)")
        for rec in short_term:
            render_recommendation_card(rec, 'short-term')

    # Medium-term actions
    if medium_term:
        st.markdown("#### 🟢 Medium-term (3-6 months)")
        for rec in medium_term:
            render_recommendation_card(rec, 'medium-term')


def render_recommendation_card(rec: Dict, priority: str) -> None:
    """Render a single recommendation card."""
    # Handle both dict and object types
    if hasattr(rec, 'model_dump'):
        rec = rec.model_dump()
    elif not isinstance(rec, dict):
        return

    priority_classes = {
        'immediate': 'action-immediate',
        'short-term': 'action-short-term',
        'medium-term': 'action-medium-term'
    }

    priority_labels = {
        'immediate': '🔴 IMMEDIATE',
        'short-term': '🟠 SHORT-TERM',
        'medium-term': '🟢 MEDIUM-TERM'
    }

    st.markdown(f"""
    <div class="action-plan {priority_classes.get(priority, '')}" style="margin: 0.5rem 0;">
        <p style="margin: 0 0 0.5rem 0;">
            <span class="priority-badge priority-{priority}">{priority_labels.get(priority, priority)}</span>
        </p>
        <p style="margin: 0 0 0.25rem 0;"><strong>{rec.get('title', 'Untitled')}</strong></p>
        <p style="margin: 0 0 0.25rem 0; color: #888;">What: {rec.get('what', rec.get('action', 'N/A'))[:150]}</p>
        <p style="margin: 0 0 0.25rem 0; color: #888;">Why: {rec.get('why', rec.get('impact', 'N/A'))[:150]}</p>
        <p style="margin: 0 0 0.25rem 0; color: #888;">How: {rec.get('how', 'N/A')[:150]}</p>
        <p style="margin: 0; color: #00c896;">
            Expected Impact: {rec.get('impact', 'N/A')[:100]}
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_data_quality_warning(issues: List[Dict]) -> None:
    """Render data quality warning section."""
    if not issues:
        return

    st.markdown('<div class="data-quality-warning">', unsafe_allow_html=True)
    st.markdown("### ⚠️ Data Quality Issues Found")

    critical = [i for i in issues if i.get('severity') == 'critical']
    high = [i for i in issues if i.get('severity') == 'high']

    if critical:
        st.error(f"**{len(critical)} CRITICAL issues** may affect analysis reliability")

    if high:
        st.warning(f"**{len(high)} HIGH severity issues** to review")

    for issue in issues[:10]:  # Show top 10
        st.markdown(f"- **{issue.get('column', 'General')}**: {issue.get('description', '')}")

    if len(issues) > 10:
        st.markdown(f"_... and {len(issues) - 10} more issues_")

    st.markdown('</div>', unsafe_allow_html=True)


def render_insight_count_summary(insights: Dict[str, List]) -> None:
    """Render summary of insight counts by category."""
    st.markdown("### Insight Summary")

    col1, col2, col3, col4 = st.columns(4)

    counts = {
        'Financial': len(insights.get('financial', [])),
        'Manufacturing': len(insights.get('manufacturing', [])),
        'Inventory': len(insights.get('inventory', [])),
        'Sales': len(insights.get('sales', []))
    }

    with col1:
        render_count_badge(counts['Financial'], 'Financial', '#e94560')
    with col2:
        render_count_badge(counts['Manufacturing'], 'Manufacturing', '#45b7d1')
    with col3:
        render_count_badge(counts['Inventory'], 'Inventory', '#00c896')
    with col4:
        render_count_badge(counts['Sales'], 'Sales', '#ffa500')


def render_count_badge(count: int, label: str, color: str) -> None:
    """Render a count badge."""
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; background: #1a1a2e; border-radius: 8px;">
        <div style="font-size: 2rem; font-weight: bold; color: {color};">{count}</div>
        <div style="color: #888; font-size: 0.85rem;">{label} Insights</div>
    </div>
    """, unsafe_allow_html=True)


def render_quality_summary_banner(quality_summary: Dict) -> None:
    """Render data quality summary banner."""
    if not quality_summary:
        return

    is_usable = quality_summary.get('is_usable', True)
    issue_count = quality_summary.get('issue_count', 0)
    critical_count = len(quality_summary.get('critical_issues', []))

    if is_usable:
        if issue_count > 0:
            st.info(f"Data loaded with {issue_count} quality issues ({critical_count} critical)")
        else:
            st.success("Data loaded - no significant quality issues detected")
    else:
        st.error("Data has critical quality issues that may affect analysis reliability")
